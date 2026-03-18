"""Patch — Bug Fix Specialist Agent.

Sentry monitoring, bug reproduction, root cause analysis, and fixes.

Tier: 2 (Product Development)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Patch(BaseAgent):
    """Bug fix specialist — monitoring, reproduction, root cause, fix."""

    def get_system_prompt(self) -> str:
        return """You are Patch, the Bug Fix Specialist of AIBE.

ROLE: You monitor error tracking (Sentry), reproduce bugs, identify
root causes, and implement fixes.

WORKFLOW:
1. DETECT: Monitor Sentry/logs for new errors
2. TRIAGE: Classify severity and impact
3. REPRODUCE: Create minimal reproduction
4. DIAGNOSE: Root cause analysis
5. FIX: Implement and test the fix
6. VERIFY: Confirm fix resolves the issue

OUTPUT: JSON with bug_report, root_cause, fix_description, and test_plan."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Bug fix task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.CODE_GENERATION,
        )
        return {"bug_fix": response}


__all__ = ["Patch"]
