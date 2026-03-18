# aibe/agents/research/scout.py
"""Scout — Market Research Agent (Tier 1)."""

from __future__ import annotations

import time
from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class ScoutAgent(BaseAgent):
    agent_id = "scout"
    name = "Scout"
    tier = 1
    escalation_target = "oracle"
    daily_budget_usd = 5.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return (
            "You are Scout, a Market Research Agent. "
            "You scan markets, identify trends, and provide intelligence to the executive team. "
            "Be thorough, cite sources when available, and focus on actionable insights."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._market_scan_loop, 1800),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _market_scan_loop(self) -> None:
        """Scan market sources every 30 minutes."""
        # Check if browser pool is available
        browser_pool = getattr(self._context, "browser_pool", None) if self._context else None

        if browser_pool:
            try:
                headlines = await browser_pool.fetch_headlines(
                    sources=["techcrunch", "hackernews", "producthunt"]
                )
            except Exception:
                headlines = None
        else:
            headlines = None

        if headlines is None:
            # Fallback: use LLM knowledge
            try:
                result = await self.think(
                    "Provide 5 current tech industry trends and their business implications. "
                    "Format as a JSON list with 'trend' and 'implication' keys."
                )
                intel = {"source": "llm_knowledge", "data": result, "timestamp": time.time()}
            except Exception:
                intel = {"source": "none", "data": "No data available", "timestamp": time.time()}
        else:
            intel = {"source": "web_scrape", "data": headlines, "timestamp": time.time()}

        await self.memory_store("scout.market_intel", "latest", intel)
        self._logger.info("Market scan completed (source: %s)", intel["source"])