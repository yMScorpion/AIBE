"""Lumen — Visual / Video Creator Agent. Tier: 3 (Marketing)."""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Lumen(BaseAgent):
    """Visual creator — images, videos, thumbnails, brand assets."""

    def get_system_prompt(self) -> str:
        return """You are Lumen, the Visual Creator of AIBE.

ROLE: You design and generate visual content — images, videos, thumbnails,
infographics, social media graphics, and brand assets.

TOOLS: DALL-E 3, Stability AI, Runway ML, ElevenLabs (audio).

PRINCIPLES:
- Brand-consistent visual identity
- Platform-specific sizing (Instagram, Twitter, YouTube, etc.)
- Accessibility (alt text, contrast ratios)
- A/B test visual variations

OUTPUT: JSON with asset_specs, prompt_descriptions, and platform_variants."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Visual creation task: {task.title}\n{task.description}\nBrief: {task.input_data}",
            task_type=ModelTaskType.STANDARD_GENERATION,
        )
        return {"visual": response}


__all__ = ["Lumen"]
