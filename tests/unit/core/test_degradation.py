# tests/unit/core/test_degradation.py
"""Unit tests for degradation manager."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from aibe.agents.registry import AgentRegistry
from aibe.core.orchestrator.degradation import (
    DegradationManager,
    DegradationMode,
    DegradationRestrictions,
)


class TestDegradationManager:
    """Tests for DegradationManager."""

    @pytest.fixture
    def manager(self) -> DegradationManager:
        """Create degradation manager."""
        return DegradationManager()

    @pytest.fixture
    def registry(self) -> AgentRegistry:
        """Create agent registry."""
        return AgentRegistry()

    def test_initial_mode_is_normal(self, manager: DegradationManager):
        """Test initial mode is NORMAL."""
        assert manager.mode == DegradationMode.NORMAL

    def test_force_mode(self, manager: DegradationManager):
        """Test forcing a mode."""
        manager.force_mode(DegradationMode.MAINTENANCE)
        assert manager.mode == DegradationMode.MAINTENANCE
        
        manager.clear_forced_mode()
        assert manager.mode == DegradationMode.NORMAL

    def test_assess_empty_registry_is_emergency(
        self, manager: DegradationManager, registry: AgentRegistry
    ):
        """Test that empty registry triggers EMERGENCY."""
        mode = manager.assess(registry)
        assert mode == DegradationMode.EMERGENCY

    def test_assess_healthy_agents_is_normal(
        self, manager: DegradationManager, registry: AgentRegistry
    ):
        """Test that healthy agents result in NORMAL mode."""
        # Add healthy agents
        for i in range(10):
            agent = MagicMock()
            agent.agent_id = f"agent_{i}"
            agent.status = "ready"
            registry.register(agent)
        
        mode = manager.assess(registry)
        assert mode == DegradationMode.NORMAL

    def test_assess_many_errors_is_degraded(
        self, manager: DegradationManager, registry: AgentRegistry
    ):
        """Test that many errors trigger DEGRADED mode."""
        # Add agents with 40% error rate
        for i in range(6):
            agent = MagicMock()
            agent.agent_id = f"healthy_{i}"
            agent.status = "ready"
            registry.register(agent)
        
        for i in range(4):
            agent = MagicMock()
            agent.agent_id = f"error_{i}"
            agent.status = "error"
            registry.register(agent)
        
        mode = manager.assess(registry)
        assert mode == DegradationMode.DEGRADED

    def test_assess_critical_agent_down_is_emergency(
        self, manager: DegradationManager, registry: AgentRegistry
    ):
        """Test that critical agent down triggers EMERGENCY."""
        # Add Oracle in error state
        oracle = MagicMock()
        oracle.agent_id = "oracle"
        oracle.status = "error"
        registry.register(oracle)
        
        # Add other healthy agents
        for i in range(9):
            agent = MagicMock()
            agent.agent_id = f"agent_{i}"
            agent.status = "ready"
            registry.register(agent)
        
        mode = manager.assess(registry)
        assert mode == DegradationMode.EMERGENCY


class TestDegradationRestrictions:
    """Tests for DegradationRestrictions."""

    def test_normal_restrictions(self):
        """Test NORMAL mode restrictions."""
        restrictions = DegradationRestrictions(DegradationMode.NORMAL)
        assert restrictions.autonomous_loops_enabled is True
        assert restrictions.new_tasks_allowed is True
        assert restrictions.meetings_allowed is True

    def test_degraded_restrictions(self):
        """Test DEGRADED mode restrictions."""
        restrictions = DegradationRestrictions(DegradationMode.DEGRADED)
        assert restrictions.autonomous_loops_enabled is False
        assert restrictions.new_tasks_allowed is True
        assert restrictions.meetings_allowed is False

    def test_emergency_restrictions(self):
        """Test EMERGENCY mode restrictions."""
        restrictions = DegradationRestrictions(DegradationMode.EMERGENCY)
        assert restrictions.autonomous_loops_enabled is False
        assert restrictions.new_tasks_allowed is False
        assert restrictions.meetings_allowed is False
        assert "sentinel" in restrictions.essential_agents_only

    def test_maintenance_restrictions(self):
        """Test MAINTENANCE mode restrictions."""
        restrictions = DegradationRestrictions(DegradationMode.MAINTENANCE)
        assert restrictions.autonomous_loops_enabled is False
        assert restrictions.new_tasks_allowed is False
        assert restrictions.drain_existing_tasks is True