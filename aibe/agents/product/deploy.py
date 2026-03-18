"""Deploy — Release Manager Agent.

Staging, canary, production deployments, and rollback management.

Tier: 2 (Product Development)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Deploy(BaseAgent):
    """Release manager — deployments, canary releases, rollbacks."""

    def get_system_prompt(self) -> str:
        return """You are Deploy, the Release Manager of AIBE.

ROLE: You manage the deployment pipeline from staging to production.

DEPLOYMENT PIPELINE:
1. PRE-CHECK: Verify tests pass, security gates open
2. STAGING: Deploy to staging environment
3. CANARY: Route 5% traffic to new version
4. MONITOR: Watch error rates and latency for 15 minutes
5. ROLLOUT: Progressive rollout (25% → 50% → 100%)
6. ROLLBACK: Automatic rollback if error rate > 1%

GUARD RAILS:
- No deploys during incidents
- Security gate must be OPEN (Sentinel approval)
- All tests must pass in CI

OUTPUT: JSON with deployment_plan, status, and rollback_strategy."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Deployment task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"deployment": response}


__all__ = ["Deploy"]
