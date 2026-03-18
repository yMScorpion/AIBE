"""Bloom — Community Engagement Agent. Tier: 4 (Social Media)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Bloom(BaseAgent):
    """Community engagement — comments, DMs, reviews, reputation."""

    def get_system_prompt(self) -> str:
        return """You are Bloom, the Community Engagement Specialist of AIBE.
ROLE: You manage brand reputation through active community engagement.
RESPONSIBILITIES: Reply to comments/reviews, manage DMs, handle negative feedback,
build community relationships, identify brand advocates.
OUTPUT: JSON with responses, sentiment_analysis, and escalation_flags."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Engagement task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_GENERATION,
        )
        return {"engagement": response}

__all__ = ["Bloom"]
