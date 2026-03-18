# aibe/core/router/budget.py
"""Budget enforcement for agent LLM calls."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class BudgetRecord:
    """Track budget usage for an agent."""

    agent_id: str
    daily_budget_usd: float
    spent_usd: float = 0.0
    reserved_usd: float = 0.0
    last_reset: float = field(default_factory=time.time)
    call_count: int = 0


class BudgetEnforcer:
    """Enforce per-agent daily budget limits with reservation system.
    
    Flow:
    1. Before LLM call: check_and_reserve() - reserves estimated cost
    2. After LLM call: record_actual() - adjusts to actual cost
    3. If call fails: release_reservation() - releases reserved amount
    
    Budget resets daily at midnight UTC.
    """

    def __init__(self, redis_client: Any = None) -> None:
        self._redis = redis_client
        self._budgets: dict[str, BudgetRecord] = {}
        self._lock = asyncio.Lock()

    def _get_or_create_record(self, agent_id: str, daily_budget: float) -> BudgetRecord:
        """Get existing record or create new one."""
        if agent_id not in self._budgets:
            self._budgets[agent_id] = BudgetRecord(
                agent_id=agent_id,
                daily_budget_usd=daily_budget,
            )
        return self._budgets[agent_id]

    def _check_and_reset_daily(self, record: BudgetRecord) -> None:
        """Reset budget if it's a new day."""
        now = datetime.now(timezone.utc)
        last_reset = datetime.fromtimestamp(record.last_reset, tz=timezone.utc)
        
        if now.date() > last_reset.date():
            record.spent_usd = 0.0
            record.reserved_usd = 0.0
            record.call_count = 0
            record.last_reset = now.timestamp()

    async def check_and_reserve(
        self,
        agent_id: str,
        estimated_cost: float,
        daily_budget: float = 1.0,
    ) -> bool:
        """Check if agent has budget and reserve the estimated amount.
        
        Args:
            agent_id: Agent requesting the budget
            estimated_cost: Estimated cost of the operation
            daily_budget: Agent's daily budget limit
            
        Returns:
            True if budget available and reserved, False otherwise
        """
        async with self._lock:
            record = self._get_or_create_record(agent_id, daily_budget)
            self._check_and_reset_daily(record)

            # Calculate available budget
            committed = record.spent_usd + record.reserved_usd
            available = record.daily_budget_usd - committed

            if estimated_cost > available:
                return False

            # Reserve the amount
            record.reserved_usd += estimated_cost
            return True

    async def release_reservation(self, agent_id: str, amount: float) -> None:
        """Release a reservation (e.g., if call failed before consuming tokens).
        
        Args:
            agent_id: Agent to release reservation for
            amount: Amount to release
        """
        async with self._lock:
            if agent_id in self._budgets:
                self._budgets[agent_id].reserved_usd = max(
                    0, self._budgets[agent_id].reserved_usd - amount
                )

    async def record_actual(
        self,
        agent_id: str,
        actual_cost: float,
        estimated_cost: float,
    ) -> None:
        """Record the actual cost and adjust reservation.
        
        Args:
            agent_id: Agent that made the call
            actual_cost: Actual cost of the operation
            estimated_cost: Originally estimated cost (to release from reservation)
        """
        async with self._lock:
            if agent_id not in self._budgets:
                return

            record = self._budgets[agent_id]
            
            # Release the reservation
            record.reserved_usd = max(0, record.reserved_usd - estimated_cost)
            
            # Record actual spend
            record.spent_usd += actual_cost
            record.call_count += 1

    def get_budget_status(self, agent_id: str) -> dict:
        """Get current budget status for an agent."""
        if agent_id not in self._budgets:
            return {
                "agent_id": agent_id,
                "budget_usd": 0,
                "spent_usd": 0,
                "reserved_usd": 0,
                "available_usd": 0,
                "utilization_pct": 0,
                "call_count": 0,
            }

        record = self._budgets[agent_id]
        self._check_and_reset_daily(record)
        
        available = record.daily_budget_usd - record.spent_usd - record.reserved_usd
        utilization = (record.spent_usd / record.daily_budget_usd * 100) if record.daily_budget_usd > 0 else 0

        return {
            "agent_id": agent_id,
            "budget_usd": record.daily_budget_usd,
            "spent_usd": round(record.spent_usd, 4),
            "reserved_usd": round(record.reserved_usd, 4),
            "available_usd": round(available, 4),
            "utilization_pct": round(utilization, 2),
            "call_count": record.call_count,
        }

    def get_all_budgets(self) -> list[dict]:
        """Get budget status for all tracked agents."""
        return [self.get_budget_status(aid) for aid in self._budgets]