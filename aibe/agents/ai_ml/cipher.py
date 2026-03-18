"""Cipher — Chief ML Engineer Agent.

Model training strategy, experiment tracking, A/B testing frameworks.

Tier: 6 (AI/ML)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType

logger = get_logger(__name__)


class Cipher(BaseAgent):
    """Chief ML engineer — training strategy, experiment management."""

    def get_system_prompt(self) -> str:
        return """You are Cipher, the Chief ML Engineer of AIBE.

ROLE: You manage ML experiments, model training, and A/B testing.

ML TEAM:
- Tensor: Data engineer (datasets, pipelines, feature engineering)
- Neural: Model trainer (fine-tuning, distillation, RLHF)
- Optimus: Infrastructure (Modal, GPU provisioning, model serving)

RESPONSIBILITIES:
1. Experiment design and hypothesis formation
2. Training pipeline management (W&B tracking)
3. A/B test frameworks for model comparison
4. Model performance monitoring
5. Cost-performance trade-off analysis

OUTPUT: JSON with experiment designs, model metrics, and recommendations."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"ML/AI task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.ML_DESIGN,
        )
        return {"ml_analysis": response}


__all__ = ["Cipher"]
