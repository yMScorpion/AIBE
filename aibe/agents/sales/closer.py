"""Closer — Deal Closing Agent. Tier: 9 (Sales)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Closer(BaseAgent):
    """Deal closer — proposals, negotiations, contract preparation."""

    def get_system_prompt(self) -> str:
        return """You are Closer, the Deal Closing Specialist of AIBE.
ROLE: You close deals — proposals, negotiation, objection handling, contracts.
OUTPUT: JSON with deal_status, proposal_draft, negotiation_strategy, and next_steps."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Deal closing: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"deal": response}

__all__ = ["Closer"]
