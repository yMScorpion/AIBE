# aibe/agents/executive/minerva.py
"""Minerva — Chief Strategist and OKR Director (Tier 0)."""

from __future__ import annotations

import time
from aibe.agents.base.agent import BaseAgent


class MinervaAgent(BaseAgent):
    agent_id = "minerva"
    name = "Minerva"
    tier = 0
    escalation_target = "oracle"
    daily_budget_usd = 10.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("executive.strategy.formulated", self._handle_strategy)

    def get_system_prompt(self) -> str:
        return (
            "You are Minerva, the Chief Strategist and OKR Director of Aibe.\n"
            "You work directly with Oracle to break down the grand vision into measurable, achievable OKRs for the Product, Marketing, and Sales teams.\n"
            "You enforce accountability. If a metric is failing, you pivot the strategy and re-delegate.\n"
            "Philosophy: Strategy without execution is hallucination. Delegate efficiently and expect autonomous course-correction."
        )

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _handle_strategy(self, data: dict) -> None:
        strategy = data.get("strategy", "")
        idea = data.get("idea", "")
        prompt = (
            f"Oracle has defined the following strategy for our new business:\n{strategy}\n\n"
            f"Idea context:\n{idea}\n\n"
            "Break this down into 3-5 specific OKRs and actionable tasks for the Product (Forge), Marketing (Helix), and Sales (Mercury) teams. "
            "Output the delegation plan."
        )
        try:
            delegation_plan = await self.think(prompt)
            bus = self._get_bus()
            if bus:
                payload = {
                    "delegation_plan": delegation_plan,
                    "timestamp": time.time()
                }
                await bus.publish("executive.delegate", payload)
                self._logger.info("Formulated OKRs and delegation plan.")
        except Exception as e:
            self._logger.error(f"Failed to create delegation plan: {e}")
