"""Scout — Market Intelligence Agent.

Multi-source research pipeline: web search, competitor analysis,
market sizing, and trend identification.

Tier: 1 (Research)
Default task type: deep_research
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.memory.namespaces import NS_RESEARCH_MARKET, NS_RESEARCH_TRENDS
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType

logger = get_logger(__name__)


class Scout(BaseAgent):
    """Market intelligence agent — multi-source research pipeline."""

    def get_system_prompt(self) -> str:
        return """You are Scout, the Market Intelligence Specialist of AIBE.

ROLE: You conduct comprehensive market research using multiple sources.
You are the system's primary researcher and fact-finder.

RESEARCH PIPELINE:
1. Gather: Search web, databases, APIs for raw data
2. Cross-reference: Verify information across multiple sources
3. Analyse: Extract patterns, trends, and insights
4. Synthesise: Create actionable intelligence reports

SOURCES AVAILABLE:
- Web search (Exa, SerpApi)
- News aggregation (Jina)
- Company databases
- Market reports
- Social media trends

OUTPUT FORMAT: Structured JSON with:
- "sources": list of sources consulted with URLs
- "findings": categorised findings
- "confidence": 0-1 confidence score per finding
- "trends": identified market trends
- "recommendations": actionable next steps
"""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        task_lower = task.title.lower()

        if "competitor" in task_lower:
            return await self._handle_competitor_research(task)
        elif "trend" in task_lower:
            return await self._handle_trend_analysis(task)
        elif "market" in task_lower and "size" in task_lower:
            return await self._handle_market_sizing(task)
        else:
            return await self._handle_general_research(task)

    async def _handle_competitor_research(self, task: TaskAssignMessage) -> dict[str, Any]:
        prompt = f"""COMPETITOR RESEARCH: {task.title}

Context: {task.description}
Data: {task.input_data}

Conduct deep competitive analysis:
1. Identify direct and indirect competitors (minimum 5)
2. For each competitor: product offering, pricing, market position, strengths/weaknesses
3. Competitive positioning map
4. Market gaps and opportunities
5. Recommended differentiation strategy

Cite your sources and assign confidence scores."""

        response = await self.think(prompt, task_type=ModelTaskType.DEEP_RESEARCH)

        await self.ctx.memory.store(
            NS_RESEARCH_MARKET,
            f"competitors-{task.task_id}",
            {"content": response},
            agent_id=self.agent_id,
        )

        return {"competitor_research": response}

    async def _handle_trend_analysis(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Market trend analysis: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.DEEP_RESEARCH,
        )

        await self.ctx.memory.store(
            NS_RESEARCH_TRENDS,
            f"trends-{task.task_id}",
            {"content": response},
            agent_id=self.agent_id,
        )

        return {"trends": response}

    async def _handle_market_sizing(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Market sizing analysis: {task.title}\n{task.description}\nData: {task.input_data}\n\n"
            f"Estimate TAM, SAM, SOM with methodology and sources.",
            task_type=ModelTaskType.DEEP_RESEARCH,
        )
        return {"market_size": response}

    async def _handle_general_research(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Research task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.DEEP_RESEARCH,
        )
        return {"research": response}


__all__ = ["Scout"]
