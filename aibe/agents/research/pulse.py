"""Pulse — Real-Time Data Analyst Agent.

Monitors live feeds, social sentiment, pricing, and market signals.

Tier: 1 (Research)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Pulse(BaseAgent):
    """Real-time data analyst — sentiment, pricing, and signal monitoring."""

    def get_system_prompt(self) -> str:
        return """You are Pulse, the Real-Time Data Analyst of AIBE.

ROLE: You monitor live data feeds, track social sentiment, pricing
changes, news alerts, and market signals in real-time.

CAPABILITIES:
- Social media sentiment analysis (Twitter, Reddit, HN)
- Pricing and competitor monitoring
- News and events tracking
- Trend detection and anomaly alerting

OUTPUT: JSON with signals, sentiment_scores, anomalies, and alerts."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Real-time analysis: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.SIMPLE_EXTRACTION,
        )
        return {"signals": response}


__all__ = ["Pulse"]
