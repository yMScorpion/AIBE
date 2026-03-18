"""Penetest — Penetration Tester Agent. Tier: 8 (Security)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Penetest(BaseAgent):
    """Penetration tester — OWASP Top 10, API fuzzing, auth testing."""

    def get_system_prompt(self) -> str:
        return """You are Penetest, the Penetration Tester of AIBE.
ROLE: You perform security testing against AIBE's own systems.
SCOPE: OWASP Top 10, API security, authentication/authorization,
injection attacks, CSRF, XSS, IDOR, rate limiting, input validation.
RULES: Only test against staging/sandbox environments. Never production.
Report all findings to Sentinel immediately.
OUTPUT: JSON with test_results, vulnerabilities, severity, and PoC_steps."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Penetration test: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SECURITY_ANALYSIS,
        )
        return {"pentest_results": response}

__all__ = ["Penetest"]
