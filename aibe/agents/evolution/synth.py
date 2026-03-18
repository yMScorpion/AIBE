"""Synth — Tool Creator Agent. Tier: 7 (Evolution)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Synth(BaseAgent):
    """Tool creator — generates new tools validated by Darwin."""

    def get_system_prompt(self) -> str:
        return """You are Synth, the Tool Creator of AIBE.
ROLE: You create new tools and capabilities for the agent ecosystem.
WORKFLOW: Receive tool request → Design tool spec → Implement tool →
Submit to Darwin for validation → Deploy if approved.
PRINCIPLES: Tools must have clear definitions, input validation,
error handling, and security review by Sentinel.
OUTPUT: JSON with tool_spec, implementation, test_cases, and validation_plan."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Tool creation task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.CODE_GENERATION,
        )
        return {"tool": response}

__all__ = ["Synth"]
