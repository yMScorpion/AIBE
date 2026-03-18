"""Escalator — Upsell & Renewal Agent. Tier: 9 (Sales)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Escalator(BaseAgent):
    """Upsell and renewals — expansion revenue, upgrade proposals."""

    def get_system_prompt(self) -> str:
        return """You are Escalator, the Upsell & Renewal Specialist of AIBE.
ROLE: You identify upsell opportunities, manage renewals, and drive expansion revenue.
OUTPUT: JSON with opportunities, renewal_timeline, upsell_proposals, and revenue_impact."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Upsell/renewal: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"upsell": response}

__all__ = ["Escalator"]
