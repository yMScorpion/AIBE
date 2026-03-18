"""VaultKeeper — Secrets Management Agent. Tier: 8 (Security)."""

from __future__ import annotations
from typing import Any
from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class VaultKeeper(BaseAgent):
    """Secrets manager — Vault operations, rotation, access control."""

    def get_system_prompt(self) -> str:
        return """You are VaultKeeper, the Secrets Manager of AIBE.
ROLE: You manage all secrets via HashiCorp Vault — creation, rotation, access.
RESPONSIBILITIES: Secret rotation schedules, access policy management,
audit logging, emergency revocation, transit encryption.
RULES: Never log or expose secret values. Rotate on 90-day cycles.
OUTPUT: JSON with rotation_status, policy_changes, and audit_events."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Secrets management task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SECURITY_ANALYSIS,
        )
        return {"vault": response}

__all__ = ["VaultKeeper"]
