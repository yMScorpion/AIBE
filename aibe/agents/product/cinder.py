# aibe/agents/product/cinder.py
"""Cinder — Infrastructure Agent (Tier 2)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class CinderAgent(BaseAgent):
    agent_id = "cinder"
    name = "Cinder"
    tier = 2
    escalation_target = "forge"
    daily_budget_usd = 2.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Cinder, an Infrastructure Agent. You manage cloud infra and deployments."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._infra_monitor, 600)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _infra_monitor(self) -> None:
        self._logger.info("Infra monitoring cycle complete")