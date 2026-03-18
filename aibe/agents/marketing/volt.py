# aibe/agents/marketing/volt.py
"""Volt — Advertising Agent (Tier 3)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class VoltAgent(BaseAgent):
    agent_id = "volt"
    name = "Volt"
    tier = 3
    escalation_target = "helix"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Volt, an Advertising Agent. You manage ad campaigns and optimise performance."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._ad_performance, 900)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _ad_performance(self) -> None:
        self._logger.info("Ad performance monitoring complete")