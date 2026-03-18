"""Guardian — Customer Success Agent. Tier: 9 (Sales)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Guardian(BaseAgent):
    """Customer success — onboarding, health scores, churn prevention."""

    def get_system_prompt(self) -> str:
        return """You are Guardian, the Customer Success Manager of AIBE.
ROLE: You ensure customer satisfaction, manage onboarding, track health scores,
and prevent churn.
OUTPUT: JSON with customer_health, onboarding_status, risk_flags, and action_plans."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Customer success: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"customer_success": response}

__all__ = ["Guardian"]
