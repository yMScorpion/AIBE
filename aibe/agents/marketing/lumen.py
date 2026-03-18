# aibe/agents/marketing/lumen.py
"""Lumen — Visual Design Agent (Tier 3)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class LumenAgent(BaseAgent):
    agent_id = "lumen"
    name = "Lumen"
    tier = 3
    escalation_target = "helix"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Lumen, a Visual Design Agent. You create visual assets for marketing."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._asset_check, 3600)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _asset_check(self) -> None:
        self._logger.info("Asset check complete")