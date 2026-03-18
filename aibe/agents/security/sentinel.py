"""Sentinel — CISO Agent.

Manages the security dashboard, coordinates security agents,
tracks remediation, and controls deployment gates.

Tier: 8 (Cybersecurity)
Default task type: security_analysis
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.memory.namespaces import NS_SECURITY_FINDINGS, NS_SECURITY_POSTURE
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType, TaskPriority

logger = get_logger(__name__)


class Sentinel(BaseAgent):
    """CISO agent — security oversight, remediation tracking, deploy gates."""

    def get_system_prompt(self) -> str:
        return """You are Sentinel, the CISO of AIBE.

ROLE: You oversee all cybersecurity operations and manage the security team.

SECURITY TEAM:
- Auditor: Code and infra scanning (Semgrep, Bandit, Gitleaks, Grype, Checkov)
- VaultKeeper: Secrets management and rotation
- Penetest: Penetration testing (OWASP Top 10)
- IncidentResponder: 24/7 monitoring and incident response

RESPONSIBILITIES:
1. Security posture dashboard and scoring
2. Remediation tracking and prioritisation
3. Deployment gate enforcement (block on HIGH/CRITICAL)
4. Security team coordination
5. Compliance monitoring
6. Threat assessment

SECURITY GATE RULES:
- BLOCK deployment if ANY critical or high severity findings exist
- Allow deployment with medium/low findings (with tracking)
- Emergency override requires Oracle approval

OUTPUT: Structured JSON with:
- "posture_score": 0-100 security score
- "open_findings": categorised findings summary
- "gate_status": OPEN | BLOCKED with reason
- "remediation_priorities": ordered list
- "recommendations": security improvements
"""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        task_lower = task.title.lower()

        if "gate" in task_lower or "deploy" in task_lower:
            return await self._handle_deployment_gate(task)
        elif "posture" in task_lower or "dashboard" in task_lower:
            return await self._handle_posture_review(task)
        elif "incident" in task_lower:
            return await self._handle_incident_coordination(task)
        else:
            return await self._handle_security_task(task)

    async def _handle_deployment_gate(self, task: TaskAssignMessage) -> dict[str, Any]:
        findings = await self.ctx.memory.recall(NS_SECURITY_FINDINGS, "latest_scan")

        prompt = f"""DEPLOYMENT GATE DECISION: {task.title}

Current findings: {findings}
Deployment context: {task.description}
Data: {task.input_data}

Evaluate the deployment gate:
1. List all open CRITICAL and HIGH findings
2. Are any blocking? (CRITICAL/HIGH = blocking)
3. Gate decision: OPEN or BLOCKED
4. If blocked: remediation steps needed
5. If open: any conditions or monitoring needed

Security gate MUST block on critical or high findings."""

        response = await self.think(prompt, task_type=ModelTaskType.SECURITY_ANALYSIS)
        return {"gate_decision": response}

    async def _handle_posture_review(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Security posture review: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SECURITY_ANALYSIS,
        )

        await self.ctx.memory.store(
            NS_SECURITY_POSTURE,
            "latest",
            {"content": response},
            agent_id=self.agent_id,
        )

        return {"posture_review": response}

    async def _handle_incident_coordination(self, task: TaskAssignMessage) -> dict[str, Any]:
        # Delegate to IncidentResponder
        await self.assign_task(
            "incident_responder",
            f"[INCIDENT] {task.title}",
            description=task.description,
            priority=TaskPriority.CRITICAL.value,
            task_type="security_analysis",
        )

        response = await self.think(
            f"Incident coordination: {task.title}\n{task.description}",
            task_type=ModelTaskType.SECURITY_ANALYSIS,
        )
        return {"incident_response": response, "delegated_to": ["incident_responder"]}

    async def _handle_security_task(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Security task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SECURITY_ANALYSIS,
        )
        return {"security_analysis": response}


__all__ = ["Sentinel"]
