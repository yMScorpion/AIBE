# aibe/agents/evolution/automata.py
"""Automata — Workflow Automation Agent (Tier 6).

Designs and optimizes automated workflows across the agent ecosystem.
Identifies bottlenecks and creates efficient multi-agent pipelines.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class AutomataAgent(BaseAgent):
    """Workflow automation and optimization agent."""

    agent_id = "automata"
    name = "Automata"
    tier = 6
    escalation_target = "darwin"
    daily_budget_usd = 3.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._workflows: dict[str, dict] = {}

    def get_system_prompt(self) -> str:
        return """You are Automata, the Workflow Automation Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Design efficient multi-agent workflows for complex tasks
- Identify and eliminate bottlenecks in existing processes
- Create reusable workflow templates
- Monitor workflow execution and optimize performance
- Handle workflow failures with appropriate fallbacks

WORKFLOW DESIGN PRINCIPLES:

1. Decomposition: Break complex tasks into atomic steps
2. Parallelization: Identify steps that can run concurrently
3. Dependencies: Map clear input/output relationships
4. Fault Tolerance: Include retry logic and fallbacks
5. Observability: Add checkpoints and progress tracking

OUTPUT FORMAT for workflow definitions:
{
  "workflow_id": "unique identifier",
  "name": "descriptive name",
  "description": "what this workflow accomplishes",
  "trigger": {
    "type": "manual|scheduled|event",
    "config": {}
  },
  "steps": [
    {
      "step_id": "step_1",
      "agent": "agent_id",
      "action": "task description",
      "inputs": {"param": "value or $previous_step.output"},
      "outputs": ["output_name"],
      "timeout_seconds": 300,
      "retry": {"max_attempts": 3, "backoff": "exponential"},
      "on_failure": "abort|continue|fallback_step"
    }
  ],
  "parallel_groups": [
    {"steps": ["step_2", "step_3"], "join": "all|any"}
  ],
  "success_criteria": "definition of workflow success",
  "estimated_duration_seconds": 600,
  "cost_estimate_usd": 0.50
}

Design robust, efficient, and maintainable workflows."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._workflow_optimization, 3600),
            (self._bottleneck_detection, 1800),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process workflow design tasks."""
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
            self._logger.error("Workflow task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _workflow_optimization(self) -> None:
        """Analyze and optimize workflows every hour."""
        optimization_report = {
            "timestamp": time.time(),
            "workflows_analyzed": len(self._workflows),
            "optimizations_found": 0,
            "recommendations": [],
        }

        for wf_id, workflow in self._workflows.items():
            steps = workflow.get("steps", [])
            
            # Check for sequential steps that could be parallelized
            for i, step in enumerate(steps[:-1]):
                next_step = steps[i + 1]
                # If next step doesn't depend on current step's output
                if not self._has_dependency(next_step, step):
                    optimization_report["optimizations_found"] += 1
                    optimization_report["recommendations"].append({
                        "workflow_id": wf_id,
                        "type": "parallelization",
                        "steps": [step.get("step_id"), next_step.get("step_id")],
                    })

        await self.memory_store("automata.optimization", "latest", optimization_report)
        self._logger.info(
            "Workflow optimization: %d workflows, %d optimizations found",
            optimization_report["workflows_analyzed"],
            optimization_report["optimizations_found"],
        )

    async def _bottleneck_detection(self) -> None:
        """Detect workflow bottlenecks every 30 minutes."""
        bottleneck_report = {
            "timestamp": time.time(),
            "bottlenecks": [],
        }

        # Would analyze actual workflow execution data
        await self.memory_store("automata.bottlenecks", "latest", bottleneck_report)
        self._logger.debug("Bottleneck detection complete")

    @staticmethod
    def _has_dependency(step: dict, previous_step: dict) -> bool:
        """Check if step depends on previous step's outputs."""
        inputs = step.get("inputs", {})
        prev_id = previous_step.get("step_id", "")
        
        for value in inputs.values():
            if isinstance(value, str) and f"${prev_id}" in value:
                return True
        return False