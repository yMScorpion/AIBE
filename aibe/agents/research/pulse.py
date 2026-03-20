# aibe/agents/research/pulse.py
"""Pulse — Sentiment Analysis Agent (Tier 1)."""

from __future__ import annotations

import time
from collections.abc import Callable
from aibe.agents.base.agent import BaseAgent


class PulseAgent(BaseAgent):
    agent_id = "pulse"
    name = "Pulse"
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
            "You are Pulse, the Audience & Trend Analyst of Aibe.\n"
            "Your role is to evaluate the human psychology, virality potential, and current market sentiment around the business ideas proposed by Scout.\n"
            "Do people actually want this? Will they pay for it? Is the niche growing or dying?\n"
            "You participate actively in the debate with Scout and Vega. You provide the reality check on user acquisition and marketing viability.\n"
            "Your philosophy: The market decides. Empathy through data. Constant debate until the idea resonates perfectly with market needs."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._sentiment_loop, 900),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _sentiment_loop(self) -> None:
        """Analyse sentiment from Scout data every 15 minutes."""
        intel = await self.memory_recall("scout.market_intel", "latest")
        if not intel:
            return
        data = intel.get("data", "")
        if not data or data == "No data available":
            return
        try:
            result = await self.think(
                f"Classify the overall sentiment of the following market intelligence as "
                f"'positive', 'neutral', or 'negative'. Explain briefly.\n\nData: {data}"
            )
            entry = {"sentiment": result, "timestamp": time.time()}
            await self.memory_store("pulse.sentiment_history", "latest", entry)
        except Exception:
            pass

    async def _handle_proposed_idea(self, data: dict) -> None:
        idea = data.get("idea", "")
        prompt = (
            f"Scout has proposed the following business idea:\n{idea}\n\n"
            "Evaluate the human psychology, virality potential, and market sentiment for this idea. "
            "Will people buy it? Is user acquisition viable? Provide a demanding critique. If it's perfect, say 'APPROVED'."
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
                self._logger.info("Sent sentiment critique for business idea.")
        except Exception as e:
            self._logger.error(f"Failed to critique business idea: {e}")
