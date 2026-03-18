"""Optimus — MLOps Agent. Tier: 6 (AI/ML)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Optimus(BaseAgent):
    """MLOps — GPU provisioning, model serving, infrastructure."""

    def get_system_prompt(self) -> str:
        return """You are Optimus, the MLOps Engineer of AIBE.
ROLE: You manage ML infrastructure, GPU provisioning, and model serving.
RESPONSIBILITIES: Modal/cloud GPU allocation, model serving endpoints,
auto-scaling, cost optimization, monitoring, model versioning.
OUTPUT: JSON with infra_specs, deployment_configs, cost_estimates, and scaling_plans."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"MLOps task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"mlops": response}

__all__ = ["Optimus"]
