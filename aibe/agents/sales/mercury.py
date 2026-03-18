"""Mercury — Sales Director Agent. Tier: 9 (Sales — conditional activation)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType, TaskPriority


class Mercury(BaseAgent):
    """Sales director — pipeline management, team coordination."""

    def get_system_prompt(self) -> str:
        return """You are Mercury, the Sales Director of AIBE.
ROLE: You lead the sales team and manage the sales pipeline.
NOTE: This tier activates ONLY when the product is ready for sales.
TEAM: Closer (deal closing), Orator (demos), Guardian (success), Escalator (renewals).
RESPONSIBILITIES: Pipeline management, quota setting, territory planning,
sales strategy, team coordination.
OUTPUT: JSON with pipeline_stats, forecasts, team_assignments, and strategies."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Sales task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        delegated = []
        task_lower = task.title.lower()
        if "deal" in task_lower or "close" in task_lower:
            await self.assign_task("closer", f"[From Mercury] {task.title}")
            delegated.append("closer")
        if "demo" in task_lower:
            await self.assign_task("orator", f"[From Mercury] {task.title}")
            delegated.append("orator")
        return {"sales": response, "delegated_to": delegated}

__all__ = ["Mercury"]
