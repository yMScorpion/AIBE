"""Tests for the base agent framework — lifecycle, context, BaseAgent."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aibe.agents.base.agent import BaseAgent
from aibe.agents.base.context import AgentContext
from aibe.agents.base.lifecycle import LifecycleManager, VALID_TRANSITIONS
from aibe.agents.registry import AgentRegistry
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import AgentStatus


# ── Concrete test agent ──────────────────────────────────────


class MockAgent(BaseAgent):
    """Concrete BaseAgent for testing."""

    def get_system_prompt(self) -> str:
        return "You are a test agent."

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        return {"result": f"Processed: {task.title}"}


def _make_context(agent_id: str = "test-agent") -> AgentContext:
    """Create a mock AgentContext."""
    return AgentContext(
        bus=AsyncMock(),
        memory=AsyncMock(),
        router=MagicMock(),
        agent_id=agent_id,
        agent_name="Test Agent",
        tier=2,
        daily_budget_usd=5.0,
    )


# ── Lifecycle tests ──────────────────────────────────────────


class TestLifecycleManager:
    def test_initial_state(self) -> None:
        lm = LifecycleManager("test")
        assert lm.status == AgentStatus.INITIALIZING

    def test_valid_transition(self) -> None:
        lm = LifecycleManager("test")
        lm.transition(AgentStatus.READY)
        assert lm.status == AgentStatus.READY

    def test_invalid_transition_raises(self) -> None:
        lm = LifecycleManager("test")
        with pytest.raises(ValueError, match="Invalid transition"):
            lm.transition(AgentStatus.RUNNING)  # Can't go INIT → RUNNING

    def test_full_lifecycle(self) -> None:
        lm = LifecycleManager("test")
        lm.transition(AgentStatus.READY)
        lm.transition(AgentStatus.RUNNING)
        lm.transition(AgentStatus.PAUSED)
        lm.transition(AgentStatus.READY)
        lm.transition(AgentStatus.STOPPED)
        assert lm.status == AgentStatus.STOPPED

    def test_error_recovery(self) -> None:
        lm = LifecycleManager("test")
        lm.transition(AgentStatus.READY)
        lm.transition(AgentStatus.RUNNING)
        lm.transition(AgentStatus.ERROR)
        lm.transition(AgentStatus.READY)  # Recovery
        assert lm.is_active

    def test_error_to_degraded(self) -> None:
        lm = LifecycleManager("test")
        lm.transition(AgentStatus.READY)
        lm.transition(AgentStatus.RUNNING)
        lm.transition(AgentStatus.ERROR)
        lm.transition(AgentStatus.DEGRADED)
        assert lm.status == AgentStatus.DEGRADED
        assert not lm.is_active

    def test_is_active(self) -> None:
        lm = LifecycleManager("test")
        assert not lm.is_active  # INITIALIZING is not active
        lm.transition(AgentStatus.READY)
        assert lm.is_active
        lm.transition(AgentStatus.RUNNING)
        assert lm.is_active

    def test_can_transition(self) -> None:
        lm = LifecycleManager("test")
        assert lm.can_transition(AgentStatus.READY)
        assert not lm.can_transition(AgentStatus.RUNNING)

    def test_all_states_have_transitions(self) -> None:
        """Every status should have at least one valid transition."""
        for status in AgentStatus:
            assert status in VALID_TRANSITIONS


# ── BaseAgent tests ──────────────────────────────────────────


class TestBaseAgent:
    def test_agent_creation(self) -> None:
        ctx = _make_context()
        agent = MockAgent(ctx)
        assert agent.agent_id == "test-agent"
        assert agent.status == AgentStatus.INITIALIZING

    def test_system_prompt(self) -> None:
        agent = MockAgent(_make_context())
        assert "test agent" in agent.get_system_prompt().lower()

    @pytest.mark.asyncio
    async def test_start_transitions_to_ready(self) -> None:
        agent = MockAgent(_make_context())
        await agent.start()
        assert agent.status == AgentStatus.READY
        assert agent.uptime_seconds >= 0

    @pytest.mark.asyncio
    async def test_stop_transitions_to_stopped(self) -> None:
        agent = MockAgent(_make_context())
        await agent.start()
        await agent.stop()
        assert agent.status == AgentStatus.STOPPED

    @pytest.mark.asyncio
    async def test_assign_task_publishes(self) -> None:
        ctx = _make_context()
        agent = MockAgent(ctx)
        await agent.start()
        task_id = await agent.assign_task("scout", "Research market")
        assert task_id  # non-empty UUID string
        ctx.bus.publish.assert_called()

    @pytest.mark.asyncio
    async def test_remember_and_recall(self) -> None:
        ctx = _make_context()
        agent = MockAgent(ctx)
        await agent.remember("test-key", {"data": "value"})
        ctx.memory.store.assert_called_once()

        await agent.recall("test-key")
        ctx.memory.recall.assert_called_once()

    @pytest.mark.asyncio
    async def test_escalate(self) -> None:
        ctx = _make_context()
        agent = MockAgent(ctx)
        await agent.start()
        await agent.escalate("Cannot process task", severity="high")
        ctx.bus.publish.assert_called()


# ── Registry tests ───────────────────────────────────────────


class TestAgentRegistry:
    def test_register_and_get(self) -> None:
        registry = AgentRegistry()
        agent = MockAgent(_make_context("oracle"))
        registry.register(agent)
        assert registry.get("oracle") is agent
        assert registry.count == 1

    def test_get_by_tier(self) -> None:
        registry = AgentRegistry()
        registry.register(MockAgent(_make_context("agent-a")))

        ctx_b = _make_context("agent-b")
        ctx_b.tier = 5
        registry.register(MockAgent(ctx_b))

        tier_2 = registry.get_by_tier(2)
        assert len(tier_2) == 1
        assert tier_2[0].agent_id == "agent-a"

    def test_unregister(self) -> None:
        registry = AgentRegistry()
        agent = MockAgent(_make_context("oracle"))
        registry.register(agent)
        registry.unregister("oracle")
        assert registry.get("oracle") is None
        assert registry.count == 0

    def test_status_summary(self) -> None:
        registry = AgentRegistry()
        registry.register(MockAgent(_make_context("a")))
        registry.register(MockAgent(_make_context("b")))
        summary = registry.get_status_summary()
        assert summary["initializing"] == 2
