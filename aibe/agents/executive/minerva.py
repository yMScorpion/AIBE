"""Minerva — Chief Strategist Agent.

Minerva owns the Business Model Canvas, defines OKRs, manages
strategy iterations, and proposes pivots when KPIs indicate problems.

Tier: 0 (executive)
Default task type: complex_reasoning
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.memory.namespaces import (
    NS_BUSINESS_MODEL,
    NS_BUSINESS_OKRS,
    NS_BUSINESS_STRATEGY,
)
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType

logger = get_logger(__name__)


class Minerva(BaseAgent):
    """Chief strategist agent — Business Model Canvas and OKR management.

    Responsibilities:
    - Business Model Canvas creation and updates
    - OKR definition and tracking
    - Pivot recommendations when strategy isn't working
    - Strategy alignment across departments
    """

    def get_system_prompt(self) -> str:
        return """You are Minerva, Chief Strategist of AIBE.

ROLE: You are the strategic brain. You manage the Business Model Canvas,
define OKRs (Objectives and Key Results), and recommend pivots.

CORE FRAMEWORKS:
1. Business Model Canvas: 9 blocks (Value Props, Customer Segments,
   Channels, Customer Relationships, Revenue Streams, Key Resources,
   Key Activities, Key Partnerships, Cost Structure)
2. OKRs: Quarterly objectives with measurable key results
3. Strategy Iterations: Data-driven pivots when metrics indicate failure

PRINCIPLES:
- Every recommendation must be backed by data from agent reports
- Pivots require >2 weeks of negative trend data
- OKRs must be SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- Always consider resource constraints (budget, agent bandwidth)

OUTPUT FORMAT: Always respond with structured JSON containing:
- "canvas_updates": any BMC block changes
- "okr_status": current OKR progress
- "recommendations": strategic recommendations
- "pivot_signal": null or {"reason", "proposed_pivot", "evidence"}
"""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Handle strategic tasks."""
        task_lower = task.title.lower()

        if "canvas" in task_lower or "business model" in task_lower:
            return await self._handle_canvas(task)
        elif "okr" in task_lower or "objective" in task_lower:
            return await self._handle_okrs(task)
        elif "pivot" in task_lower or "strategy change" in task_lower:
            return await self._handle_pivot_analysis(task)
        else:
            return await self._handle_strategy_task(task)

    async def _handle_canvas(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Create or update the Business Model Canvas."""
        current_canvas = await self.ctx.memory.recall(NS_BUSINESS_MODEL, "canvas")

        prompt = f"""BUSINESS MODEL CANVAS TASK: {task.title}

Current Canvas: {current_canvas or 'No existing canvas — create initial version'}
Context: {task.description}
Input data: {task.input_data}

Create/update the Business Model Canvas with all 9 blocks:
1. Value Propositions
2. Customer Segments
3. Channels
4. Customer Relationships
5. Revenue Streams
6. Key Resources
7. Key Activities
8. Key Partnerships
9. Cost Structure

Provide structured JSON for each block with specific, actionable content."""

        response = await self.think(prompt, task_type=ModelTaskType.COMPLEX_REASONING)

        await self.ctx.memory.store(
            NS_BUSINESS_MODEL,
            "canvas",
            {"content": response, "task_id": task.task_id},
            agent_id=self.agent_id,
        )

        return {"canvas": response}

    async def _handle_okrs(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Define or review OKRs."""
        current_okrs = await self.ctx.memory.recall(NS_BUSINESS_OKRS, "current")
        strategy = await self.ctx.memory.recall(NS_BUSINESS_STRATEGY, "latest_discovery")

        prompt = f"""OKR MANAGEMENT: {task.title}

Current OKRs: {current_okrs or 'No existing OKRs'}
Business Strategy: {strategy or 'No strategy defined yet'}
Context: {task.description}

Define or review OKRs following this structure:
- Objective: Clear, inspiring goal statement
- Key Results: 3-5 measurable outcomes (with target numbers)
- Initiatives: Specific projects/tasks to achieve KRs
- Owner: Which agent/tier is responsible

Each KR should have: current_value, target_value, unit, deadline."""

        response = await self.think(prompt, task_type=ModelTaskType.COMPLEX_REASONING)

        await self.ctx.memory.store(
            NS_BUSINESS_OKRS,
            "current",
            {"content": response, "task_id": task.task_id},
            agent_id=self.agent_id,
        )

        return {"okrs": response}

    async def _handle_pivot_analysis(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Analyse whether a strategy pivot is needed."""
        prompt = f"""PIVOT ANALYSIS: {task.title}

Context: {task.description}
Data: {task.input_data}

Evaluate whether a strategic pivot is warranted:
1. What are the negative signals? (KPI trends, market changes)
2. How long have these signals persisted?
3. What are the proposed pivot options?
4. Risk/reward analysis for each option
5. Recommendation: HOLD, MINOR_ADJUSTMENT, or MAJOR_PIVOT

A pivot requires >2 weeks of negative trend data."""

        response = await self.think(prompt, task_type=ModelTaskType.COMPLEX_REASONING)

        return {"pivot_analysis": response}

    async def _handle_strategy_task(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Handle general strategic tasks."""
        response = await self.think(
            f"Strategic task: {task.title}\n\n{task.description}\n\n"
            f"Data: {task.input_data}\n\n"
            f"Provide strategic analysis and recommendations.",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"strategy": response}


__all__ = ["Minerva"]
