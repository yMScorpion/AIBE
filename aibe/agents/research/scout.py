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
        self.register_handler("research.idea.critique", self._handle_critique)
        self.register_handler("agency.start_research", self._handle_start_research)

    async def _handle_start_research(self, data: dict) -> None:
        self._logger.info("Manual trigger received: starting business idea generation loop immediately.")
        await self._business_idea_loop()

    def get_system_prompt(self) -> str:
        return (
            "You are Scout, the Lead Opportunity Hunter and Market Research Agent of Aibe.\n"
            "Your primary mission is to research and identify highly profitable, scalable, and autonomous online business ideas that can be executed entirely by Aibe (an AI agency).\n"
            "A winning idea MUST have: 1. High profit margin, 2. Low manual human intervention, 3. High demand/trend, 4. Technical feasibility for AI agents to build and run (e.g., SaaS, automated content creation, digital products, programmatic SEO).\n"
            "You don't just accept the first idea. You actively research, propose ideas to your peers (Vega and Pulse), and engage in a deep debate. If they point out flaws, you iterate or pivot.\n"
            "Your philosophy: Quality over quantity. Data-driven hypotheses. Embrace debate."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._market_scan_loop, 1800),
            (self._business_idea_loop, 3600),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _market_scan_loop(self) -> None:
        """Scan market sources every 30 minutes."""
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

    async def _business_idea_loop(self) -> None:
        """Generate and propose a business idea to the research team."""
        intel = await self.memory_recall("scout.market_intel", "latest")
        data = intel.get("data", "") if intel else "No recent data."
        
        prompt = (
            "Based on the latest market intel and your instructions, propose ONE highly profitable, "
            "autonomous online business idea that an AI agency like Aibe can execute. "
            "Include: 1. Name, 2. Target Audience, 3. Revenue Model, 4. AI execution strategy.\n"
            f"Market Intel: {data}"
        )
        try:
            idea = await self.think(prompt)
            bus = self._get_bus()
            if bus:
                payload = {
                    "idea": idea,
                    "proposed_by": "scout",
                    "timestamp": time.time(),
                    "status": "proposed"
                }
                await self.memory_store("scout.current_idea", "latest", payload)
                await bus.publish("research.idea.proposed", payload)
                self._logger.info("Proposed a new business idea for debate.")
        except Exception as e:
            self._logger.error(f"Failed to generate business idea: {e}")

    async def _handle_critique(self, data: dict) -> None:
        """Handle critiques from Vega or Pulse and refine the idea."""
        critique = data.get("critique", "")
        agent = data.get("agent", "unknown")
        idea_payload = await self.memory_recall("scout.current_idea", "latest")
        
        if not idea_payload:
            return
            
        current_idea = idea_payload.get("idea", "")
        
        prompt = (
            f"Your peer {agent} has critiqued your business idea.\n"
            f"Current Idea:\n{current_idea}\n\n"
            f"Critique from {agent}:\n{critique}\n\n"
            "Refine the idea based on this feedback. If the critique is too harsh or the idea is fundamentally flawed, "
            "pivot to a completely new idea. Output the refined or new idea."
        )
        
        try:
            refined_idea = await self.think(prompt)
            bus = self._get_bus()
            if bus:
                payload = {
                    "idea": refined_idea,
                    "proposed_by": "scout",
                    "timestamp": time.time(),
                    "status": "refined",
                    "refined_after_critique_by": agent
                }
                await self.memory_store("scout.current_idea", "latest", payload)
                await bus.publish("research.idea.refined", payload)
                self._logger.info(f"Refined business idea based on {agent}'s critique.")
                
                # If both Vega and Pulse are happy, we could send it to Oracle.
                # For now, let's say if we get refined, we send it to Oracle to evaluate
                await bus.publish("executive.idea.review", payload)
        except Exception as e:
            self._logger.error(f"Failed to refine business idea: {e}")
