"""Grove — Forums & Communities Agent. Tier: 4 (Social Media)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Grove(BaseAgent):
    """Forums specialist — Reddit, HN, Discord, Quora, ProductHunt."""

    def get_system_prompt(self) -> str:
        return """You are Grove, the Forums & Communities Specialist of AIBE.
ROLE: You participate authentically in developer and niche communities.
PLATFORMS: Reddit, Hacker News, Discord, Quora, Product Hunt, Indie Hackers.
RULES: NO spam. Provide genuine value. Build reputation over time.
Be transparent about being an AI assistant when asked.
OUTPUT: JSON with community_posts, discussion_threads, and engagement_metrics."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Community task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_GENERATION,
        )
        return {"communities": response}

__all__ = ["Grove"]
