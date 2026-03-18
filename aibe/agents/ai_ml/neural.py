# aibe/agents/ai_ml/neural.py
"""Neural — Model Training Agent (Tier 7).

Handles model training, evaluation, and experiment tracking.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class NeuralAgent(BaseAgent):
    """Model training and evaluation agent."""

    agent_id = "neural"
    name = "Neural"
    tier = 7
    escalation_target = "cipher"
    daily_budget_usd = 4.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._training_jobs: list[dict] = []

    def get_system_prompt(self) -> str:
        return """You are Neural, the Model Training Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Execute model training runs based on experiment specifications
- Perform hyperparameter optimization
- Evaluate model performance against baselines
- Track experiments and maintain model registry
- Ensure reproducibility and proper versioning

TRAINING BEST PRACTICES:

1. Experiment Tracking:
   - Log all hyperparameters
   - Track metrics at each epoch/step
   - Save model checkpoints
   - Document data versions used

2. Evaluation:
   - Hold-out test sets
   - Cross-validation when appropriate
   - Multiple metric tracking
   - Statistical significance testing

3. Reproducibility:
   - Fixed random seeds
   - Environment capture
   - Data versioning
   - Configuration as code

OUTPUT FORMAT for training run reports:
{
  "run_id": "unique identifier",
  "experiment_id": "parent experiment",
  "model": {
    "architecture": "model type",
    "parameters": {"param": "value"},
    "size_mb": 100
  },
  "training": {
    "epochs": 10,
    "batch_size": 32,
    "learning_rate": 0.001,
    "optimizer": "adam",
    "duration_seconds": 3600
  },
  "metrics": {
    "train": {"loss": 0.1, "accuracy": 0.95},
    "validation": {"loss": 0.15, "accuracy": 0.92},
    "test": {"loss": 0.18, "accuracy": 0.90}
  },
  "artifacts": {
    "model_path": "path/to/model",
    "logs_path": "path/to/logs",
    "checkpoints": ["checkpoint_1", "checkpoint_2"]
  },
  "status": "completed|failed|stopped",
  "notes": "any observations or issues"
}

Train models rigorously and document thoroughly."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._training_job_monitoring, 900),
            (self._model_evaluation_cycle, 3600),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process model training tasks."""
        self._status = "running"
        try:
            result = await self.on_task_receive(data)
            bus = self._get_bus()
            if bus:
                await bus.publish(
                    f"tasks.result.{data.get('source', 'unknown')}",
                    {"task_id": data.get("task_id"), "status": "completed", "output": result},
                )
            self._tasks_completed += 1
        except Exception as exc:
            self._error_count += 1
            self._logger.error("Training task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _training_job_monitoring(self) -> None:
        """Monitor active training jobs every 15 minutes."""
        active_jobs = [j for j in self._training_jobs if j.get("status") == "running"]

        job_report = {
            "timestamp": time.time(),
            "active_jobs": len(active_jobs),
            "completed_jobs": len([j for j in self._training_jobs if j.get("status") == "completed"]),
            "failed_jobs": len([j for j in self._training_jobs if j.get("status") == "failed"]),
        }

        await self.memory_store("neural.jobs", "summary", job_report)
        self._logger.info("Training jobs: %d active", job_report["active_jobs"])

    async def _model_evaluation_cycle(self) -> None:
        """Run model evaluation cycle every hour."""
        evaluation_report = {
            "timestamp": time.time(),
            "models_evaluated": 0,
            "improvements": [],
            "regressions": [],
        }

        await self.memory_store("neural.evaluation", "latest", evaluation_report)
        self._logger.debug("Model evaluation cycle complete")