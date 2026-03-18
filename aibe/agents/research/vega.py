"""Vega — Strategic Analyst Agent.

Deep SWOT analysis, market positioning, and strategy recommendations.

Tier: 1 (Research)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Vega(BaseAgent):
    """Strategic analyst — SWOT, competitive positioning, trend forecasting."""

    def get_system_prompt(self) -> str:
        return """You are Vega, the Strategic Analyst of AIBE.

ROLE: You perform SWOT analyses, competitive positioning, market trend
forecasting, and strategic recommendations.

FRAMEWORKS: SWOT, Porter's Five Forces, Blue Ocean Strategy, BCG Matrix.

OUTPUT: JSON with analysis, insights, confidence_scores, and recommendations."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Strategic analysis: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.DEEP_RESEARCH,
        )
        return {"analysis": response}


__all__ = ["Vega"]
