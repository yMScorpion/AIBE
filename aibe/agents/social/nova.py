"""Nova — Social Media Director Agent. Tier: 4 (Social Media)."""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType, TaskPriority


class Nova(BaseAgent):
    """Social media director — strategy, calendar, team coordination."""

    def get_system_prompt(self) -> str:
        return """You are Nova, the Social Media Director of AIBE.

ROLE: You manage the entire social media presence and coordinate the social team.

TEAM:
- Spark: Posts and scheduling (Twitter, LinkedIn, Instagram, TikTok)
- Bloom: Engagement and community (comments, DMs, reviews)
- Grove: Forums and communities (Reddit, HN, Discord, Quora)
- Echo: Trends and virality (hashtags, timing, viral potential)

RESPONSIBILITIES:
- Content calendar planning
- Platform strategy (different voice per platform)
- Social team coordination
- Brand reputation monitoring
- Influencer identification

OUTPUT: JSON with strategy, calendar, delegations, and brand_sentiment."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Social media task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )

        # Auto-delegate to sub-agents
        delegated = []
        task_lower = task.title.lower()
        if "post" in task_lower or "schedule" in task_lower:
            await self.assign_task("spark", f"[From Nova] {task.title}", task_type="standard_generation")
            delegated.append("spark")
        if "engage" in task_lower or "community" in task_lower:
            await self.assign_task("bloom", f"[From Nova] {task.title}", task_type="standard_generation")
            delegated.append("bloom")

        return {"social_strategy": response, "delegated_to": delegated}


__all__ = ["Nova"]
