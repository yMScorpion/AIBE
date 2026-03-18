"""Auditor — Code & Infra Security Scanner Agent. Tier: 8 (Security)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.memory.namespaces import NS_SECURITY_FINDINGS
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Auditor(BaseAgent):
    """Security scanner — Semgrep, Bandit, Gitleaks, Grype, Checkov."""

    def get_system_prompt(self) -> str:
        return """You are Auditor, the Security Scanner of AIBE.
ROLE: You perform automated security scanning of code and infrastructure.
TOOLS: Semgrep (SAST), Bandit (Python), Gitleaks (secrets), Grype (SCA), Checkov (IaC).
WORKFLOW: Scan → Classify findings → Score severity → Report to Sentinel.
Findings categories: CRITICAL > HIGH > MEDIUM > LOW > INFO.
OUTPUT: JSON with scan_results, findings_by_severity, and remediation_steps."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Security scan task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SECURITY_ANALYSIS,
        )
        await self.ctx.memory.store(
            NS_SECURITY_FINDINGS, f"scan-{task.task_id}",
            {"content": response}, agent_id=self.agent_id,
        )
        return {"scan_results": response}

__all__ = ["Auditor"]
