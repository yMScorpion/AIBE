# aibe/agents/marketing/prism.py
"""Prism — Marketing Analytics Agent (Tier 3)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class PrismAgent(BaseAgent):
    agent_id = "prism"
    name = "Prism"
    tier = 3
    escalation_target = "helix"
    daily_budget_usd = 2.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Prism, a Marketing Analytics Agent. You aggregate and analyse marketing metrics."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._analytics_digest, 1800)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _analytics_digest(self) -> None:
        self._logger.info("Marketing analytics digest complete")