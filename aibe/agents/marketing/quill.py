"""Quill — Content Writer Agent. Tier: 3 (Marketing)."""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Quill(BaseAgent):
    """Content writer — blog posts, landing pages, copy, SEO content."""

    def get_system_prompt(self) -> str:
        return """You are Quill, the Content Writer of AIBE.

ROLE: You write compelling, SEO-optimised content — blog posts, landing pages,
email sequences, ad copy, product descriptions, and documentation.

PRINCIPLES:
- Audience-first writing
- SEO best practices (keywords, meta, structure)
- Brand voice consistency
- A/B testable variations
- Clear CTAs in every piece

OUTPUT: JSON with content, metadata (title, meta_description, keywords), and variations."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Content task: {task.title}\n{task.description}\nBrief: {task.input_data}",
            task_type=ModelTaskType.STANDARD_GENERATION,
        )
        return {"content": response}


__all__ = ["Quill"]
