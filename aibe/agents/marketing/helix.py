"""Helix — CMO Agent.

Marketing strategy, campaign planning, brand management,
and coordination of marketing sub-agents.

Tier: 3 (Growth & Marketing)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType, TaskPriority

logger = get_logger(__name__)


class Helix(BaseAgent):
    """CMO agent — marketing strategy and team coordination."""

    def get_system_prompt(self) -> str:
        return """You are Helix, the CMO of AIBE.

ROLE: You own the marketing strategy, brand, and growth.

MARKETING TEAM:
- Quill: Content writer (blog, copy, landing pages)
- Lumen: Visual/video creator (images, videos, thumbnails)
- Volt: Paid ads manager (Meta/Google Ads)
- Prism: Analytics analyst (attribution, ROI, dashboards)

You delegate content, creative, and ads work to your team.

OUTPUT: Structured JSON with marketing strategies, campaign plans, and delegations."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Marketing task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )

        # Delegate to sub-agents based on task content
        delegated = []
        task_lower = task.title.lower()
        if "content" in task_lower or "blog" in task_lower:
            await self.assign_task("quill", f"[From Helix] {task.title}", task_type="standard_generation")
            delegated.append("quill")
        if "visual" in task_lower or "image" in task_lower or "video" in task_lower:
            await self.assign_task("lumen", f"[From Helix] {task.title}", task_type="standard_generation")
            delegated.append("lumen")
        if "ad" in task_lower or "campaign" in task_lower:
            await self.assign_task("volt", f"[From Helix] {task.title}", task_type="standard_reasoning")
            delegated.append("volt")

        return {"marketing": response, "delegated_to": delegated}


__all__ = ["Helix"]
