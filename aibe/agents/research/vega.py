# aibe/agents/research/vega.py
"""Vega — Data Analytics Agent (Tier 1)."""

from __future__ import annotations

from aibe.agents.base.agent import BaseAgent


class VegaAgent(BaseAgent):
    agent_id = "vega"
    name = "Vega"
    tier = 1
    escalation_target = "oracle"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return (
            "You are Vega, a Data Analytics Agent. "
            "You analyse datasets, generate reports, and provide insights to support decision-making."
        )

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)