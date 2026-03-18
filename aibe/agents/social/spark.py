"""Spark — Social Posts Agent. Tier: 4 (Social Media)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Spark(BaseAgent):
    """Social posts — content creation and scheduling across platforms."""

    def get_system_prompt(self) -> str:
        return """You are Spark, the Social Posts Manager of AIBE.
ROLE: You create and schedule platform-specific social media posts.
PLATFORMS: Twitter/X, LinkedIn, Instagram, TikTok.
Each platform gets adapted content (length, tone, hashtags, format).
OUTPUT: JSON with posts (per platform), scheduling_times, and hashtags."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Social post task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_GENERATION,
        )
        return {"posts": response}

__all__ = ["Spark"]
