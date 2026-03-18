# aibe/agents/ai_ml/tensor.py
"""Tensor — Data Engineering Agent (Tier 7).

Manages data pipelines, feature engineering, and data quality
for ML workloads.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class TensorAgent(BaseAgent):
    """Data engineering and pipeline agent."""

    agent_id = "tensor"
    name = "Tensor"
    tier = 7
    escalation_target = "cipher"
    daily_budget_usd = 3.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return """You are Tensor, the Data Engineering Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Design and implement data pipelines for ML workloads
- Perform feature engineering and data transformations
- Ensure data quality and consistency
- Manage data versioning and lineage
- Optimize data storage and retrieval performance

DATA ENGINEERING PRINCIPLES:

1. Pipeline Design:
   - Idempotent operations
   - Clear schema definitions
   - Proper error handling
   - Monitoring and alerting

2. Feature Engineering:
   - Domain-driven feature design
   - Feature documentation
   - Feature store integration
   - Temporal consistency

3. Data Quality:
   - Schema validation
   - Null/outlier handling
   - Distribution monitoring
   - Drift detection

OUTPUT FORMAT for data pipeline specifications:
{
  "pipeline_id": "unique identifier",
  "name": "descriptive name",
  "purpose": "what this pipeline does",
  "sources": [
    {"name": "source_name", "type": "database|api|file|stream"}
  ],
  "transformations": [
    {"step": "step_name", "operation": "description", "output_schema": {}}
  ],
  "outputs": [
    {"name": "output_name", "format": "parquet|json|etc", "destination": "where"}
  ],
  "quality_checks": [
    {"check": "check_name", "condition": "SQL-like expression", "action": "warn|fail"}
  ],
  "schedule": "cron expression or trigger",
  "monitoring": {
    "metrics": ["latency", "row_count", "error_rate"],
    "alerts": ["condition for alerts"]
  }
}

Build reliable, scalable, and well-documented data pipelines."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._data_quality_check, 3600),
            (self._pipeline_health_monitoring, 1800),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process data engineering tasks."""
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
            self._logger.error("Data engineering task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _data_quality_check(self) -> None:
        """Run data quality checks every hour."""
        quality_report = {
            "timestamp": time.time(),
            "checks_run": 0,
            "passed": 0,
            "warnings": 0,
            "failures": 0,
        }

        await self.memory_store("tensor.quality", "latest", quality_report)
        self._logger.info(
            "Data quality check: %d passed, %d warnings, %d failures",
            quality_report["passed"],
            quality_report["warnings"],
            quality_report["failures"],
        )

    async def _pipeline_health_monitoring(self) -> None:
        """Monitor pipeline health every 30 minutes."""
        health_report = {
            "timestamp": time.time(),
            "pipelines_monitored": 0,
            "healthy": 0,
            "degraded": 0,
            "failed": 0,
        }

        await self.memory_store("tensor.health", "latest", health_report)
        self._logger.debug("Pipeline health monitoring complete")