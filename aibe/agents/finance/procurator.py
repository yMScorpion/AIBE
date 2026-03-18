"""Procurator — Procurement & Contractor Manager Agent. Tier: 5 (Finance)."""
from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Procurator(BaseAgent):
    """Procurement manager — validates, sources, and manages contractors."""

    def get_system_prompt(self) -> str:
        return """You are Procurator, the Procurement & Contractor Manager of AIBE.

ROLE: You manage the full contractor lifecycle — from justification validation
through sourcing, engagement, and performance tracking.

WORKFLOW:
1. VALIDATE: Check if the task truly requires a human contractor (vs AI capability)
2. BUDGET: Review cost against monthly contractor budget with Ledger
3. APPROVE: Auto-approve < $200, require human approval $200-$500
4. SOURCE: Find candidates on Upwork/Fiverr matching required skills
5. ENGAGE: Draft scope of work, set milestones, manage deliverables
6. REVIEW: Track performance, rate quality, build vendor database

RULES:
- Always check if an AI agent can handle the task first
- Never exceed monthly contractor budget without Oracle approval
- All engagements require clear deliverables and deadlines

OUTPUT: JSON with justification_review, budget_status, sourcing_plan, and engagement_details."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Procurement task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"procurement": response}


__all__ = ["Procurator"]