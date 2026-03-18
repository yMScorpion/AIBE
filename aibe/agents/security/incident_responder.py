"""IncidentResponder — Security Incident Response Agent. Tier: 8 (Security)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class IncidentResponder(BaseAgent):
    """Incident responder — 24/7 monitoring, triage, containment, recovery."""

    def get_system_prompt(self) -> str:
        return """You are IncidentResponder, the Security Incident Handler of AIBE.
ROLE: You monitor for security incidents and execute response playbooks.
WORKFLOW: Detect → Triage → Contain → Eradicate → Recover → Post-mortem.
PLAYBOOKS: DDoS, Data breach, Credential compromise, Service degradation.
ESCALATION: Critical incidents → Sentinel → Oracle (emergency summit).
OUTPUT: JSON with incident_report, containment_actions, and recovery_status."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Incident response: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SECURITY_ANALYSIS,
        )
        return {"incident": response}

__all__ = ["IncidentResponder"]
