"""Orator — Demo & Presentation Agent. Tier: 9 (Sales)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Orator(BaseAgent):
    """Demo specialist — presentations, product demos, pitch decks."""

    def get_system_prompt(self) -> str:
        return """You are Orator, the Demo & Presentation Specialist of AIBE.
ROLE: You create compelling product demos, pitch decks, and presentations.
OUTPUT: JSON with presentation_outline, demo_script, talking_points, and Q&A_prep."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Demo/presentation: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_GENERATION,
        )
        return {"presentation": response}

__all__ = ["Orator"]
