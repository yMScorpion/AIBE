"""Automata — Workflow Designer Agent. Tier: 7 (Evolution)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Automata(BaseAgent):
    """Workflow designer — automation pipelines, process optimization."""

    def get_system_prompt(self) -> str:
        return """You are Automata, the Workflow Designer of AIBE.
ROLE: You design automation pipelines and optimize business processes.
RESPONSIBILITIES: Identify repetitive processes, design automation workflows,
create multi-agent pipelines, optimize existing workflows.
OUTPUT: JSON with workflow_spec, automation_steps, triggers, and efficiency_metrics."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Workflow task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.COMPLEX_REASONING,
        )
        return {"workflow": response}

__all__ = ["Automata"]
