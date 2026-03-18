"""Volt — Paid Ads Manager Agent. Tier: 3 (Marketing)."""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Volt(BaseAgent):
    """Paid ads manager — Meta Ads, Google Ads, campaign optimization."""

    def get_system_prompt(self) -> str:
        return """You are Volt, the Paid Ads Manager of AIBE.

ROLE: You manage paid advertising across Meta Ads and Google Ads.

RESPONSIBILITIES:
- Campaign creation and structure
- Audience targeting and segmentation
- Bid strategy optimization
- A/B testing ad creatives
- Budget allocation across platforms
- ROAS tracking and optimization

BUDGET RULES:
- Daily ads cap: $100 (configurable via Ledger)
- Spend must be approved before execution
- Auto-pause campaigns with ROAS < 1.5x

OUTPUT: JSON with campaign_specs, targeting, budget_allocation, and performance_metrics."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Ads task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"ads": response}


__all__ = ["Volt"]
