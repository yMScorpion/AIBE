# aibe/agents/social/spark.py
"""Spark — Social Media Publishing Agent (Tier 4).

Responsible for creating and scheduling social media posts across platforms.
Optimizes posting times and content format for maximum engagement.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class SparkAgent(BaseAgent):
    """Social media content creation and publishing agent."""

    agent_id = "spark"
    name = "Spark"
    tier = 4
    escalation_target = "nova"
    daily_budget_usd = 2.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._scheduled_posts: list[dict] = []

    def get_system_prompt(self) -> str:
        return """You are Spark, the Social Media Publishing Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Create engaging social media content for multiple platforms (Twitter/X, LinkedIn, Instagram, TikTok)
- Optimize content format and length for each platform's requirements
- Schedule posts for optimal engagement times based on audience analytics
- Maintain consistent brand voice across all channels
- Track posting schedules and ensure timely publication

OUTPUT FORMAT:
When creating posts, provide JSON with:
{
  "platform": "twitter|linkedin|instagram|tiktok",
  "content": "post text",
  "hashtags": ["tag1", "tag2"],
  "media_suggestion": "description of suggested visual",
  "optimal_time": "HH:MM UTC",
  "engagement_prediction": "low|medium|high"
}

GUIDELINES:
- Twitter/X: Max 280 chars, punchy, use 2-3 hashtags
- LinkedIn: Professional tone, 150-300 words, industry hashtags
- Instagram: Visual-first, compelling caption, 5-10 hashtags
- TikTok: Trend-aware, casual, hook in first 3 seconds

Be creative, on-brand, and data-driven in your content decisions."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._posting_loop, 1800),
            (self._trend_alignment_check, 3600),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process incoming content creation tasks."""
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
            self._logger.error("Task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _posting_loop(self) -> None:
        """Check and publish scheduled posts every 30 minutes."""
        current_time = time.time()
        
        # Check for posts ready to publish
        ready_posts = [
            p for p in self._scheduled_posts
            if p.get("scheduled_time", 0) <= current_time and not p.get("published")
        ]

        for post in ready_posts:
            self._logger.info(
                "Publishing post to %s: %s...",
                post.get("platform"),
                post.get("content", "")[:50],
            )
            post["published"] = True
            post["published_at"] = current_time

        # Store updated schedule
        await self.memory_store(
            "spark.schedule",
            "posts",
            {"posts": self._scheduled_posts, "updated_at": current_time},
        )

        self._logger.info(
            "Posting loop complete: %d posts published, %d pending",
            len(ready_posts),
            len([p for p in self._scheduled_posts if not p.get("published")]),
        )

    async def _trend_alignment_check(self) -> None:
        """Check if scheduled content aligns with current trends."""
        # Retrieve trend data from Echo agent
        trends = await self.memory_recall("echo.trends", "latest")
        
        if not trends:
            self._logger.debug("No trend data available for alignment check")
            return

        pending_posts = [p for p in self._scheduled_posts if not p.get("published")]
        
        if pending_posts and trends.get("trending_topics"):
            self._logger.info(
                "Checking %d pending posts against %d trending topics",
                len(pending_posts),
                len(trends.get("trending_topics", [])),
            )