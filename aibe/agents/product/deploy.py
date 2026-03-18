# aibe/agents/product/deploy.py
"""Deploy — Deployment Agent (Tier 2)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class DeployAgent(BaseAgent):
    agent_id = "deploy"
    name = "Deploy"
    tier = 2
    escalation_target = "forge"
    daily_budget_usd = 2.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Deploy, a Deployment Agent. You handle CI/CD pipelines and deployments."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._deploy_readiness, 1800)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _deploy_readiness(self) -> None:
        self._logger.info("Deployment readiness check complete")