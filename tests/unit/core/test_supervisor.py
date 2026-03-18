# tests/unit/core/test_supervisor.py
"""Unit tests for agent supervisor."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from aibe.agents.registry import AgentRegistry
from aibe.core.orchestrator.supervisor import AgentSupervisor


class TestAgentSupervisor:
    """Tests for AgentSupervisor."""

    @pytest.fixture
    def registry(self) -> AgentRegistry:
        """Create agent registry."""
        return AgentRegistry()

    @pytest.fixture
    def orchestrator(self) -> MagicMock:
        """Create mock orchestrator."""
        return MagicMock()

    @pytest.fixture
    def supervisor(self, registry: AgentRegistry, orchestrator: MagicMock) -> AgentSupervisor:
        """Create supervisor instance."""
        return AgentSupervisor(registry, orchestrator)

    def test_initial_state(self, supervisor: AgentSupervisor):
        """Test supervisor initial state."""
        assert supervisor._running is False
        assert len(supervisor._restart_counts) == 0
        assert len(supervisor._cooldown_until) == 0

    @pytest.mark.asyncio
    async def test_start_stop(self, supervisor: AgentSupervisor):
        """Test supervisor start and stop."""
        await supervisor.start()
        assert supervisor._running is True
        assert supervisor._task is not None
        
        await supervisor.stop()
        assert supervisor._running is False

    def test_max_restarts_constant(self, supervisor: AgentSupervisor):
        """Test max restarts is properly set."""
        assert supervisor.MAX_RESTARTS == 3

    def test_check_interval_constant(self, supervisor: AgentSupervisor):
        """Test check interval is properly set."""
        assert supervisor.CHECK_INTERVAL == 30