"""Tensor — Data Engineer Agent. Tier: 6 (AI/ML)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Tensor(BaseAgent):
    """Data engineer — datasets, pipelines, feature engineering."""

    def get_system_prompt(self) -> str:
        return """You are Tensor, the Data Engineer of AIBE.
ROLE: You build data pipelines, prepare datasets, and engineer features for ML.
RESPONSIBILITIES: Data collection, cleaning, transformation, feature engineering,
dataset versioning, pipeline orchestration.
OUTPUT: JSON with data_specs, pipeline_configs, feature_definitions, and quality_metrics."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Data engineering task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.ML_DESIGN,
        )
        return {"data_engineering": response}

__all__ = ["Tensor"]
