"""Tests for meeting engine — types, state, and engine orchestration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from aibe.agents.meetings.engine import MeetingEngine, MeetingState
from aibe.agents.meetings.types import (
    ALL_MEETING_TEMPLATES,
    STRATEGY_SUMMIT,
    SPRINT_PLANNING,
    SECURITY_REVIEW,
    MeetingTemplate,
)


class TestMeetingTemplate:
    def test_all_eight_templates_defined(self) -> None:
        assert len(ALL_MEETING_TEMPLATES) == 8

    def test_strategy_summit(self) -> None:
        assert "oracle" in STRATEGY_SUMMIT.required_participants
        assert "minerva" in STRATEGY_SUMMIT.required_participants
        assert STRATEGY_SUMMIT.min_quorum == 4
        assert STRATEGY_SUMMIT.max_rounds == 4

    def test_sprint_planning(self) -> None:
        assert "forge" in SPRINT_PLANNING.required_participants
        assert len(SPRINT_PLANNING.agenda_items) == 4

    def test_security_review(self) -> None:
        assert "sentinel" in SECURITY_REVIEW.required_participants
        assert "auditor" in SECURITY_REVIEW.required_participants

    def test_all_templates_have_agenda(self) -> None:
        for name, template in ALL_MEETING_TEMPLATES.items():
            assert len(template.agenda_items) > 0, f"{name} has no agenda items"


class TestMeetingState:
    def test_initial_state(self) -> None:
        state = MeetingState("test-id", STRATEGY_SUMMIT)
        assert state.status == "scheduled"
        assert state.current_round == 0

    def test_to_dict(self) -> None:
        state = MeetingState("test-id", STRATEGY_SUMMIT)
        state.title = "Test Summit"
        data = state.to_dict()
        assert data["meeting_id"] == "test-id"
        assert data["meeting_type"] == "strategy_summit"
        assert data["title"] == "Test Summit"


class TestMeetingEngine:
    def test_init(self) -> None:
        engine = MeetingEngine()
        assert engine.active_meeting_count == 0

    @pytest.mark.asyncio
    async def test_convene_unknown_type_raises(self) -> None:
        engine = MeetingEngine()
        with pytest.raises(Exception, match="Unknown"):
            await engine.convene("nonexistent_meeting")

    @pytest.mark.asyncio
    async def test_convene_runs_meeting(self) -> None:
        """Convene a meeting with no registry (accepts all participants)."""
        memory = AsyncMock()
        engine = MeetingEngine(memory=memory)

        state = await engine.convene(
            "strategy_summit",
            title_vars={"topic": "Q1 Strategy"},
        )

        assert state.status == "completed"
        assert state.started_at is not None
        assert state.ended_at is not None
        assert len(state.participants) >= STRATEGY_SUMMIT.min_quorum
        assert len(state.contributions) > 0
        assert "Q1 Strategy" in state.title

        # Minutes should be stored
        memory.store.assert_called_once()

    @pytest.mark.asyncio
    async def test_quorum_check(self) -> None:
        """Meeting should fail if quorum not met."""
        # Create a registry with only 1 available agent
        registry = MagicMock()
        registry.get = MagicMock(return_value=None)  # All agents unavailable

        engine = MeetingEngine(registry=registry)

        with pytest.raises(Exception, match="[Qq]uorum"):
            await engine.convene("strategy_summit")
