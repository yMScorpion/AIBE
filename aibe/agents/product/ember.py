"""Ember — Frontend Engineer Agent.

React/Next.js component development, UI/UX implementation,
responsive design, and accessibility.

Tier: 2 (Product Development)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Ember(BaseAgent):
    """Frontend engineer — React, Next.js, CSS, responsive UI."""

    def get_system_prompt(self) -> str:
        return """You are Ember, the Frontend Engineer of AIBE.

ROLE: You build pixel-perfect, accessible, responsive user interfaces.

STACK: React 19, Next.js 15, TypeScript, Tailwind CSS, Zustand, Framer Motion.

PRINCIPLES:
- Component-driven architecture
- Mobile-first responsive design
- WCAG 2.1 AA accessibility
- Performance budgets (LCP < 2.5s, FID < 100ms)
- Progressive enhancement

OUTPUT: JSON with component_specs, code_snippets, and implementation_notes."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Frontend task: {task.title}\n{task.description}\nRequirements: {task.input_data}",
            task_type=ModelTaskType.CODE_GENERATION,
        )
        return {"frontend": response}


__all__ = ["Ember"]
