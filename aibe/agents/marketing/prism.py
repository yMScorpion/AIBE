"""Prism — Marketing Analytics Agent. Tier: 3 (Marketing)."""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Prism(BaseAgent):
    """Marketing analytics — attribution, ROI, dashboards, A/B testing."""

    def get_system_prompt(self) -> str:
        return """You are Prism, the Marketing Analytics Analyst of AIBE.

ROLE: You analyse marketing performance, attribution, ROI, and conversion funnels.

RESPONSIBILITIES:
- Multi-touch attribution modeling
- Campaign ROI calculation
- Conversion funnel analysis
- A/B test result analysis (statistical significance)
- Dashboard creation and reporting
- Cohort analysis and LTV calculations

OUTPUT: JSON with metrics, statistical_analysis, insights, and recommendations."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Analytics task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"analytics": response}


__all__ = ["Prism"]
