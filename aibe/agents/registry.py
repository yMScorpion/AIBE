"""Agent registry — discovers, registers, and tracks all agents."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from aibe.core.logging import get_logger
from aibe.core.types import AgentStatus

if TYPE_CHECKING:
    from aibe.agents.base.agent import BaseAgent

logger = get_logger(__name__)


class AgentRegistry:
    """Central registry for all agent instances.

    Provides lookup by ID, tier, capability, and status tracking.
    """

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Register an agent instance.

        Args:
            agent: The agent to register.
        """
        self._agents[agent.agent_id] = agent
        logger.info(
            "Agent registered",
            agent_id=agent.agent_id,
            agent_name=agent.agent_name,
            tier=agent.ctx.tier,
        )

    def unregister(self, agent_id: str) -> None:
        """Remove an agent from the registry.

        Args:
            agent_id: ID of the agent to remove.
        """
        self._agents.pop(agent_id, None)
        logger.info("Agent unregistered", agent_id=agent_id)

    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID.

        Args:
            agent_id: Agent identifier.

        Returns:
            The agent instance or None.
        """
        return self._agents.get(agent_id)

    def get_by_tier(self, tier: int) -> list[BaseAgent]:
        """Get all agents of a specific tier.

        Args:
            tier: Tier number (0-9).

        Returns:
            List of agents in that tier.
        """
        return [a for a in self._agents.values() if a.ctx.tier == tier]

    def get_active(self) -> list[BaseAgent]:
        """Get all agents in an active state."""
        return [a for a in self._agents.values() if a.status in {AgentStatus.READY, AgentStatus.RUNNING}]

    def get_all(self) -> list[BaseAgent]:
        """Get all registered agents."""
        return list(self._agents.values())

    @property
    def count(self) -> int:
        """Total number of registered agents."""
        return len(self._agents)

    @property
    def active_count(self) -> int:
        """Number of active agents."""
        return len(self.get_active())

    def get_status_summary(self) -> dict[str, int]:
        """Get a count of agents by status.

        Returns:
            Dict mapping status name to count.
        """
        summary: dict[str, int] = {}
        for agent in self._agents.values():
            status = agent.status.value
            summary[status] = summary.get(status, 0) + 1
        return summary


__all__ = ["AgentRegistry"]
