# aibe/agents/social/bloom.py
"""Bloom — Community Engagement Agent (Tier 4).

Manages community interactions, responds to comments and messages,
and maintains positive brand presence across social platforms.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class BloomAgent(BaseAgent):
    """Community engagement and reputation management agent."""

    agent_id = "bloom"
    name = "Bloom"
    tier = 4
    escalation_target = "nova"
    daily_budget_usd = 2.5

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._engagement_queue: list[dict] = []

    def get_system_prompt(self) -> str:
        return """You are Bloom, the Community Engagement Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Monitor and respond to comments, mentions, and DMs across social platforms
- Maintain positive brand sentiment through thoughtful engagement
- Identify and escalate potential PR issues or negative sentiment spikes
- Build relationships with community members and brand advocates
- Track engagement metrics and community health indicators

ENGAGEMENT GUIDELINES:
1. Response Tone: Friendly, helpful, authentic — never corporate or robotic
2. Response Time: Prioritize by urgency (complaints > questions > praise)
3. Escalation Triggers:
   - Viral negative content (>100 engagements)
   - Legal/safety concerns
   - Influencer complaints
   - Coordinated negative campaigns

OUTPUT FORMAT for engagement responses:
{
  "platform": "twitter|instagram|linkedin|discord",
  "original_content": "user's message",
  "sentiment": "positive|neutral|negative",
  "priority": "low|medium|high|critical",
  "response": "your crafted response",
  "action": "respond|escalate|monitor|ignore",
  "escalation_reason": "if applicable"
}

Be empathetic, solution-oriented, and always represent the brand positively."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._engagement_check, 900),
            (self._sentiment_aggregation, 1800),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process engagement tasks."""
        self._status = "running"
        try:
            result = await self.on_task_receive(data)
            bus = self._get_bus()
            if bus:
                await bus.publish(
                    f"tasks.result.{data.get('source', 'unknown')}",
                    {"task_id": data.get("task_id"), "status": "completed", "output": result},
                )
            self._tasks_completed += 1
        except Exception as exc:
            self._error_count += 1
            self._logger.error("Engagement task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _engagement_check(self) -> None:
        """Check for pending engagements every 15 minutes."""
        # Retrieve any queued engagement items
        queue_data = await self.memory_recall("bloom.engagement", "queue")
        
        if queue_data and queue_data.get("items"):
            self._engagement_queue = queue_data["items"]
            
            # Process high-priority items
            critical_items = [
                item for item in self._engagement_queue
                if item.get("priority") in ("high", "critical") and not item.get("processed")
            ]
            
            for item in critical_items:
                if item.get("priority") == "critical":
                    await self.escalate(
                        f"Critical engagement issue: {item.get('summary', 'Unknown')}",
                        severity="high",
                    )
                item["processed"] = True
                item["processed_at"] = time.time()

            self._logger.info(
                "Engagement check: %d critical items processed, %d total in queue",
                len(critical_items),
                len(self._engagement_queue),
            )

    async def _sentiment_aggregation(self) -> None:
        """Aggregate community sentiment every 30 minutes."""
        processed_items = [
            item for item in self._engagement_queue
            if item.get("processed") and item.get("sentiment")
        ]

        if not processed_items:
            return

        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for item in processed_items:
            sentiment = item.get("sentiment", "neutral")
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1

        total = sum(sentiment_counts.values())
        sentiment_score = 0.0
        if total > 0:
            sentiment_score = (
                sentiment_counts["positive"] - sentiment_counts["negative"]
            ) / total

        report = {
            "period": "30min",
            "total_engagements": total,
            "sentiment_distribution": sentiment_counts,
            "sentiment_score": round(sentiment_score, 3),
            "timestamp": time.time(),
        }

        await self.memory_store("bloom.sentiment", "latest", report)
        self._logger.info("Sentiment score: %.2f (n=%d)", sentiment_score, total)