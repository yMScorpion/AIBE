# aibe/agents/research/vega.py
"""Vega — Data Analytics Agent (Tier 1)."""

from __future__ import annotations

import time
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
        self.register_handler("research.idea.proposed", self._handle_proposed_idea)
        self.register_handler("research.idea.refined", self._handle_proposed_idea)

    def get_system_prompt(self) -> str:
        return (
            "You are Vega, the Strategic Critic and Feasibility Analyst of Aibe.\n"
            "When Scout proposes a business idea, your job is to ruthlessly but constructively analyze its technical feasibility, market saturation, and execution complexity.\n"
            "You evaluate if the Aibe agency (with its dev, marketing, and sales agents) can actually build and scale this.\n"
            "Engage in debate with Scout and Pulse. Do not agree easily. Point out edge cases, potential bottlenecks, and demand better solutions until a truly winning, flawless idea is formed.\n"
            "Your philosophy: Rigorous validation, zero fluff, and collaborative refinement through debate."
        )

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _handle_proposed_idea(self, data: dict) -> None:
        idea = data.get("idea", "")
        prompt = (
            f"Scout has proposed the following business idea:\n{idea}\n\n"
            "Provide a rigorous feasibility analysis. Point out technical hurdles, market saturation, "
            "and execution complexities. Be constructive but demanding. If it's perfect, say 'APPROVED'."
        )
        try:
            critique = await self.think(prompt)
            bus = self._get_bus()
            if bus and "APPROVED" not in critique:
                payload = {
                    "critique": critique,
                    "agent": self.name,
                    "timestamp": time.time()
                }
                await bus.publish("research.idea.critique", payload)
                self._logger.info("Sent critique for business idea.")
        except Exception as e:
            self._logger.error(f"Failed to critique business idea: {e}")
