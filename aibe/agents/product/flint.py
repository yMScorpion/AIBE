# aibe/agents/product/flint.py
"""Flint — Backend/API Development Agent (Tier 2)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class FlintAgent(BaseAgent):
    agent_id = "flint"
    name = "Flint"
    tier = 2
    escalation_target = "forge"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Flint, a Backend/API Development Agent. You build APIs and backend services."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._api_health_check, 900)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _api_health_check(self) -> None:
        self._logger.info("API health check — monitoring generated endpoints")