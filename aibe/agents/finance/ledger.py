"""Ledger — CFO Agent.

Tracks revenue, expenses, generates P&L reports, and enforces
budget constraints across all agents and departments.

Tier: 5 (Finance & Operations)
Default task type: standard_reasoning
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType

logger = get_logger(__name__)


class Ledger(BaseAgent):
    """CFO agent — financial tracking, P&L, and budget enforcement.

    Responsibilities:
    - Revenue tracking (Stripe, invoices, MRR)
    - Expense categorisation (LLM, infra, contractors, ads)
    - P&L report generation
    - Budget enforcement (approvals, alerts)
    - Financial projections
    """

    def get_system_prompt(self) -> str:
        return """You are Ledger, the CFO of AIBE.

ROLE: You track all financial data, generate reports, and enforce budgets.

FINANCIAL CATEGORIES:
- Revenue: MRR, ARR, one-time sales, partnership income
- LLM Costs: Per-agent daily spend, model routing costs
- Infrastructure: Cloud, APIs, domain, hosting
- Advertising: Meta Ads, Google Ads campaigns
- Contractors: External hiring via Upwork/Fiverr
- Content: Image/video/audio generation costs

BUDGET RULES:
- Daily LLM budget: $50 (configurable)
- Daily ads cap: $100 (configurable)
- Monthly contractor budget: $500 (configurable)
- Contractor auto-approve: < $200
- Contractor human-approve: $200-$500

OUTPUT FORMAT: Structured JSON with:
- "financial_data": numbers and calculations
- "analysis": insights and trends
- "alerts": any budget warnings
- "recommendations": cost optimization suggestions
"""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        task_lower = task.title.lower()

        if "p&l" in task_lower or "profit" in task_lower or "loss" in task_lower:
            return await self._handle_pnl(task)
        elif "budget" in task_lower:
            return await self._handle_budget_review(task)
        elif "expense" in task_lower or "cost" in task_lower:
            return await self._handle_expense_analysis(task)
        else:
            return await self._handle_financial_task(task)

    async def _handle_pnl(self, task: TaskAssignMessage) -> dict[str, Any]:
        prompt = f"""P&L REPORT: {task.title}

Data: {task.input_data}
Context: {task.description}

Generate a comprehensive P&L report including:
1. Revenue breakdown by source
2. Cost breakdown by category (LLM, infra, ads, contractors)
3. Gross margin
4. Net margin
5. Month-over-month trends
6. Burn rate and runway

Provide JSON with all calculations shown."""

        response = await self.think(prompt, task_type=ModelTaskType.STANDARD_REASONING)
        return {"pnl_report": response}

    async def _handle_budget_review(self, task: TaskAssignMessage) -> dict[str, Any]:
        prompt = f"""BUDGET REVIEW: {task.title}

Data: {task.input_data}
Context: {task.description}

Review budget utilisation across all categories:
1. LLM spend vs daily/monthly budget
2. Ad spend vs daily cap
3. Contractor spend vs monthly budget
4. Infrastructure costs
5. Any budget violations or warnings
6. Optimisation opportunities

Flag any agents over 80% of their daily budget."""

        response = await self.think(prompt, task_type=ModelTaskType.STANDARD_REASONING)
        return {"budget_review": response}

    async def _handle_expense_analysis(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Expense analysis: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"expense_analysis": response}

    async def _handle_financial_task(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Financial task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"financial_analysis": response}


__all__ = ["Ledger"]
