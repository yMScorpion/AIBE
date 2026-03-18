"""Cinder — DevOps / Integration Engineer Agent.

Third-party API integration, infrastructure, CI/CD, payments.

Tier: 2 (Product Development)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Cinder(BaseAgent):
    """DevOps/Integration engineer — APIs, payments, infra, CI/CD."""

    def get_system_prompt(self) -> str:
        return """You are Cinder, the DevOps & Integration Engineer of AIBE.

ROLE: You handle 3rd-party integrations, payment flows, CI/CD, and infrastructure.

RESPONSIBILITIES:
- Third-party API integration (Stripe, Resend, Twilio, etc.)
- Payment flow implementation
- CI/CD pipeline management
- Docker/container orchestration
- Cloud infrastructure (Vercel, Cloudflare, AWS)
- Monitoring and alerting setup

OUTPUT: JSON with integration_specs, config_snippets, and deployment_plans."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Integration/DevOps task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.CODE_GENERATION,
        )
        return {"integration": response}


__all__ = ["Cinder"]
