# tests/unit/core/test_budget_enforcer.py
"""Unit tests for budget enforcement."""

from __future__ import annotations

import pytest

from aibe.core.router.budget import BudgetEnforcer


class TestBudgetEnforcer:
    """Tests for BudgetEnforcer."""

    @pytest.fixture
    def enforcer(self) -> BudgetEnforcer:
        """Create budget enforcer instance."""
        return BudgetEnforcer()

    @pytest.mark.asyncio
    async def test_reserve_within_budget(self, enforcer: BudgetEnforcer):
        """Test reservation within budget limits."""
        result = await enforcer.check_and_reserve(
            agent_id="oracle",
            estimated_cost=1.0,
            daily_budget=5.0,
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_reserve_exceeds_budget(self, enforcer: BudgetEnforcer):
        """Test reservation that exceeds budget."""
        # First, use up the budget
        await enforcer.check_and_reserve("oracle", 4.0, 5.0)
        await enforcer.record_actual("oracle", 4.0, 4.0)
        
        # Try to reserve more than available
        result = await enforcer.check_and_reserve("oracle", 2.0, 5.0)
        assert result is False

    @pytest.mark.asyncio
    async def test_release_reservation(self, enforcer: BudgetEnforcer):
        """Test releasing a reservation."""
        await enforcer.check_and_reserve("oracle", 3.0, 5.0)
        await enforcer.release_reservation("oracle", 3.0)
        
        # Should be able to reserve again
        result = await enforcer.check_and_reserve("oracle", 3.0, 5.0)
        assert result is True

    @pytest.mark.asyncio
    async def test_record_actual_adjusts_reservation(self, enforcer: BudgetEnforcer):
        """Test that recording actual cost adjusts reservation."""
        await enforcer.check_and_reserve("oracle", 2.0, 5.0)
        await enforcer.record_actual("oracle", 1.5, 2.0)
        
        status = enforcer.get_budget_status("oracle")
        assert status["spent_usd"] == 1.5
        assert status["reserved_usd"] == 0.0

    def test_get_budget_status_unknown_agent(self, enforcer: BudgetEnforcer):
        """Test getting status for unknown agent."""
        status = enforcer.get_budget_status("unknown")
        assert status["agent_id"] == "unknown"
        assert status["spent_usd"] == 0
        assert status["budget_usd"] == 0

    @pytest.mark.asyncio
    async def test_utilization_percentage(self, enforcer: BudgetEnforcer):
        """Test utilization percentage calculation."""
        await enforcer.check_and_reserve("oracle", 2.5, 5.0)
        await enforcer.record_actual("oracle", 2.5, 2.5)
        
        status = enforcer.get_budget_status("oracle")
        assert status["utilization_pct"] == 50.0

    @pytest.mark.asyncio
    async def test_get_all_budgets(self, enforcer: BudgetEnforcer):
        """Test getting all budget statuses."""
        await enforcer.check_and_reserve("oracle", 1.0, 5.0)
        await enforcer.check_and_reserve("minerva", 0.5, 3.0)
        
        all_budgets = enforcer.get_all_budgets()
        assert len(all_budgets) == 2
        agent_ids = [b["agent_id"] for b in all_budgets]
        assert "oracle" in agent_ids
        assert "minerva" in agent_ids