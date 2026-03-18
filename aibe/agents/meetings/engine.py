"""Meeting engine — orchestrates multi-agent structured debates.

Implements the Structured Debate Protocol:
1. Briefing → each participant receives the agenda and context
2. Rounds → each participant contributes (position / rebuttal / data)
3. Consensus → collect votes, determine outcome
4. Minutes → generate and store meeting minutes with action items
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any, Optional, TYPE_CHECKING
from uuid import uuid4

from aibe.agents.meetings.types import ALL_MEETING_TEMPLATES, MeetingTemplate
from aibe.core.exceptions import MeetingError, MeetingQuorumError
from aibe.core.logging import get_logger
from aibe.core.memory.namespaces import NS_MEETINGS_DECISIONS, NS_MEETINGS_TRANSCRIPTS

if TYPE_CHECKING:
    from aibe.agents.base.agent import BaseAgent
    from aibe.agents.registry import AgentRegistry
    from aibe.core.memory.client import OpenVikingClient
    from aibe.core.message_bus.client import NATSBus

logger = get_logger(__name__)


class MeetingState:
    """Tracks the state of a single meeting."""

    def __init__(self, meeting_id: str, template: MeetingTemplate) -> None:
        self.meeting_id = meeting_id
        self.template = template
        self.title = ""
        self.status = "scheduled"  # scheduled | in_progress | completed | cancelled
        self.participants: list[str] = []
        self.contributions: list[dict[str, Any]] = []
        self.decisions: list[str] = []
        self.action_items: list[dict[str, Any]] = []
        self.current_round = 0
        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize meeting state to a dict."""
        return {
            "meeting_id": self.meeting_id,
            "meeting_type": self.template.meeting_type,
            "title": self.title,
            "status": self.status,
            "participants": self.participants,
            "contributions": self.contributions,
            "decisions": self.decisions,
            "action_items": self.action_items,
            "current_round": self.current_round,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
        }


class MeetingEngine:
    """Orchestrates multi-agent meetings with the Structured Debate Protocol."""

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        memory: Optional[OpenVikingClient] = None,
        bus: Optional[NATSBus] = None,
    ) -> None:
        self._registry = registry
        self._memory = memory
        self._bus = bus
        self._active_meetings: dict[str, MeetingState] = {}

    def set_dependencies(
        self,
        registry: AgentRegistry,
        memory: OpenVikingClient,
        bus: NATSBus,
    ) -> None:
        """Set dependencies (may be set post-init)."""
        self._registry = registry
        self._memory = memory
        self._bus = bus

    async def convene(
        self,
        meeting_type: str,
        *,
        title_vars: Optional[dict[str, str]] = None,
        extra_agenda: Optional[list[str]] = None,
        extra_participants: Optional[list[str]] = None,
    ) -> MeetingState:
        """Convene a new meeting.

        Args:
            meeting_type: One of the defined meeting types.
            title_vars: Variables for the title template.
            extra_agenda: Additional agenda items beyond template defaults.
            extra_participants: Additional required participants.

        Returns:
            The MeetingState tracking the meeting.

        Raises:
            MeetingError: If meeting type is unknown.
            MeetingQuorumError: If not enough participants available.
        """
        template = ALL_MEETING_TEMPLATES.get(meeting_type)
        if template is None:
            raise MeetingError(
                f"Unknown meeting type: {meeting_type}",
                details={"available": list(ALL_MEETING_TEMPLATES.keys())},
            )

        # Create meeting state
        meeting_id = str(uuid4())
        state = MeetingState(meeting_id, template)
        state.title = template.title_template.format(**(title_vars or {"topic": "General"}))

        # Determine participants
        available = self._get_available_participants(
            template.required_participants,
            template.optional_participants + (extra_participants or []),
        )

        if len(available) < template.min_quorum:
            raise MeetingQuorumError(
                f"Quorum not met: {len(available)}/{template.min_quorum} available",
                details={
                    "meeting_type": meeting_type,
                    "available": available,
                    "required_quorum": template.min_quorum,
                },
            )

        state.participants = available
        state.status = "in_progress"
        state.started_at = datetime.now(tz=timezone.utc)

        self._active_meetings[meeting_id] = state

        logger.info(
            "Meeting convened",
            meeting_id=meeting_id,
            meeting_type=meeting_type,
            participants=available,
        )

        # Run the meeting rounds
        agenda = list(template.agenda_items) + (extra_agenda or [])
        await self._run_rounds(state, agenda)

        return state

    async def _run_rounds(self, state: MeetingState, agenda: list[str]) -> None:
        """Execute the structured debate rounds.

        Each round asks every participant to contribute their position
        on the current agenda items. Up to max_rounds.
        """
        for round_num in range(1, state.template.max_rounds + 1):
            state.current_round = round_num
            logger.info(
                "Meeting round starting",
                meeting_id=state.meeting_id,
                round=round_num,
            )

            round_contributions: list[dict[str, Any]] = []

            for agent_id in state.participants:
                contribution = await self._get_contribution(
                    agent_id=agent_id,
                    meeting_id=state.meeting_id,
                    round_num=round_num,
                    agenda=agenda,
                    previous_contributions=round_contributions,
                )
                round_contributions.append(contribution)
                state.contributions.append(contribution)

            # Check for consensus after each round
            if round_num >= 2:
                consensus = self._check_consensus(round_contributions)
                if consensus:
                    logger.info("Consensus reached", meeting_id=state.meeting_id, round=round_num)
                    break

        # Finalize
        state.status = "completed"
        state.ended_at = datetime.now(tz=timezone.utc)
        self._active_meetings.pop(state.meeting_id, None)

        # Store meeting minutes in memory
        await self._store_minutes(state)

        logger.info(
            "Meeting completed",
            meeting_id=state.meeting_id,
            total_contributions=len(state.contributions),
            decisions=len(state.decisions),
        )

    async def _get_contribution(
        self,
        agent_id: str,
        meeting_id: str,
        round_num: int,
        agenda: list[str],
        previous_contributions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Get a contribution from a single agent.

        In production, this calls the agent's `think()` method.
        For now, returns a structured placeholder.
        """
        agent = self._registry.get(agent_id) if self._registry else None

        if agent is not None:
            try:
                prompt = self._build_contribution_prompt(
                    agent_id, round_num, agenda, previous_contributions,
                )
                content = await agent.think(prompt, task_type="standard_reasoning")
            except Exception as exc:
                logger.warning(
                    "Agent contribution failed",
                    agent_id=agent_id,
                    error=str(exc),
                )
                content = f"[{agent_id} was unable to contribute: {exc}]"
        else:
            content = f"[{agent_id} contribution placeholder — agent not connected]"

        return {
            "agent_id": agent_id,
            "round": round_num,
            "meeting_id": meeting_id,
            "content": content,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }

    def _build_contribution_prompt(
        self,
        agent_id: str,
        round_num: int,
        agenda: list[str],
        previous: list[dict[str, Any]],
    ) -> str:
        """Build the prompt for an agent's meeting contribution."""
        agenda_str = "\n".join(f"  {i+1}. {item}" for i, item in enumerate(agenda))
        prev_str = ""
        if previous:
            prev_str = "\n\nPrevious contributions this round:\n"
            for c in previous:
                prev_str += f"  [{c['agent_id']}]: {c['content'][:500]}\n"

        return (
            f"You are participating in a meeting.\n"
            f"Round {round_num}.\n\n"
            f"Agenda:\n{agenda_str}\n"
            f"{prev_str}\n\n"
            f"Provide your analysis, position, or recommendations on the agenda items. "
            f"Be concise and actionable. If you disagree with a previous contribution, "
            f"explain why with data/evidence."
        )

    def _check_consensus(self, contributions: list[dict[str, Any]]) -> bool:
        """Heuristic consensus check based on contribution similarity.

        A proper implementation would use semantic similarity scoring
        or explicit vote collection. For now, always returns False
        to ensure all rounds run.
        """
        # TODO: Implement semantic consensus scoring using embeddings
        return False

    async def _store_minutes(self, state: MeetingState) -> None:
        """Store meeting minutes in OpenViking memory."""
        if self._memory is None:
            logger.debug("No memory client — skipping minutes storage")
            return

        minutes_data = state.to_dict()
        await self._memory.store(
            NS_MEETINGS_TRANSCRIPTS,
            state.meeting_id,
            minutes_data,
            agent_id="meeting_engine",
        )
        logger.info("Meeting minutes stored", meeting_id=state.meeting_id)

    def _get_available_participants(
        self,
        required: list[str],
        optional: list[str],
    ) -> list[str]:
        """Filter participants to those currently available."""
        available: list[str] = []

        for agent_id in required:
            if self._registry is None:
                available.append(agent_id)
                continue
            agent = self._registry.get(agent_id)
            if agent is not None and agent.status.value in {"ready", "running"}:
                available.append(agent_id)

        for agent_id in optional:
            if agent_id in available:
                continue
            if self._registry is None:
                available.append(agent_id)
                continue
            agent = self._registry.get(agent_id)
            if agent is not None and agent.status.value in {"ready", "running"}:
                available.append(agent_id)

        return available

    @property
    def active_meeting_count(self) -> int:
        """Number of currently active meetings."""
        return len(self._active_meetings)

    def get_meeting(self, meeting_id: str) -> Optional[MeetingState]:
        """Get state of an active meeting."""
        return self._active_meetings.get(meeting_id)


__all__ = ["MeetingEngine", "MeetingState"]
