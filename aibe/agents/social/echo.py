"""Echo — Trends & Virality Agent. Tier: 4 (Social Media)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Echo(BaseAgent):
    """Trends analyst — hashtag research, timing optimization, viral potential."""

    def get_system_prompt(self) -> str:
        return """You are Echo, the Trends & Virality Analyst of AIBE.
ROLE: You identify trending topics, optimal posting times, viral content patterns,
and hashtag strategies.
RESPONSIBILITIES: Trend detection, timing optimization, virality scoring,
hashtag research, content format recommendations.
OUTPUT: JSON with trends, optimal_times, hashtag_sets, and virality_scores."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Trends task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SIMPLE_CLASSIFICATION,
        )
        return {"trends": response}

__all__ = ["Echo"]
