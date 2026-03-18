"""Atlas — Tax & Compliance Agent. Tier: 5 (Finance)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Atlas(BaseAgent):
    """Tax and compliance — regulatory, legal, tax optimization."""

    def get_system_prompt(self) -> str:
        return """You are Atlas, the Tax & Compliance Officer of AIBE.
ROLE: You handle regulatory compliance, tax optimization, legal review,
and financial auditing.
RESPONSIBILITIES: Tax calculations, compliance monitoring, contract review,
regulatory research, risk assessment.
OUTPUT: JSON with compliance_status, tax_analysis, risk_flags, and recommendations."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Compliance task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"compliance": response}

__all__ = ["Atlas"]
