"""Neural — Model Trainer Agent. Tier: 6 (AI/ML)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Neural(BaseAgent):
    """Model trainer — fine-tuning, distillation, RLHF, evaluation."""

    def get_system_prompt(self) -> str:
        return """You are Neural, the Model Trainer of AIBE.
ROLE: You train, fine-tune, and evaluate ML models.
RESPONSIBILITIES: Model selection, fine-tuning, distillation, RLHF,
hyperparameter optimization, evaluation benchmarks, model comparison.
TOOLS: W&B, Modal, HuggingFace, PyTorch.
OUTPUT: JSON with training_configs, metrics, model_comparisons, and deployment_readiness."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Model training task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.ML_DESIGN,
        )
        return {"training": response}

__all__ = ["Neural"]
