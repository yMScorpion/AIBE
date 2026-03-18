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

    def get_system_prompt(self) -> str:
        return (
            "You are Pulse, a Sentiment Analysis Agent. "
            "You analyse market data and communications to classify sentiment "
            "as positive, neutral, or negative. Be precise and data-driven."
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
            self._logger.info("No market intel available — skipping sentiment analysis")
            return

        data = intel.get("data", "")
        if not data or data == "No data available":
            return

        try:
            result = await self.think(
                f"Classify the overall sentiment of the following market intelligence as "
                f"'positive', 'neutral', or 'negative'. Explain briefly.\n\nData: {data}"
            )
            entry = {
                "sentiment": result,
                "source_timestamp": intel.get("timestamp"),
                "analysis_timestamp": time.time(),
            }
            await self.memory_store("pulse.sentiment_history", "latest", entry)
            self._logger.info("Sentiment analysis completed")
        except Exception:
            self._logger.debug("Sentiment analysis skipped — LLM unavailable")