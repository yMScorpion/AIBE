# aibe/agents/social/grove.py
"""Grove — Forum & Community Platforms Agent (Tier 4).

Manages presence on Reddit, Hacker News, Discord, ProductHunt,
and other community-driven platforms.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class GroveAgent(BaseAgent):
    """Forum and community platform management agent."""

    agent_id = "grove"
    name = "Grove"
    tier = 4
    escalation_target = "nova"
    daily_budget_usd = 2.0

    MONITORED_PLATFORMS = ["reddit", "hackernews", "discord", "producthunt", "quora"]

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._mentions: list[dict] = []

    def get_system_prompt(self) -> str:
        return """You are Grove, the Forum & Community Platforms Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Monitor Reddit, Hacker News, Discord, ProductHunt, and Quora for brand mentions
- Participate authentically in relevant community discussions
- Share valuable insights without being overtly promotional
- Identify opportunities for thought leadership and brand awareness
- Track community sentiment and emerging discussions in our space

PLATFORM-SPECIFIC GUIDELINES:

Reddit:
- Follow subreddit rules strictly
- Provide genuine value; avoid self-promotion
- Use appropriate flair and formatting
- Karma management: build reputation before promoting

Hacker News:
- Technical accuracy is paramount
- Thoughtful, substantive comments only
- Avoid marketing language entirely
- Focus on engineering and product insights

Discord:
- Match community tone and culture
- Be helpful and responsive
- Engage in relevant channels only
- Build relationships over time

ProductHunt:
- Support launches with genuine engagement
- Connect with makers and founders
- Share constructive feedback

OUTPUT FORMAT:
{
  "platform": "reddit|hackernews|discord|producthunt|quora",
  "thread_url": "link to discussion",
  "context": "summary of discussion",
  "opportunity_type": "mention|question|discussion|launch",
  "recommended_action": "respond|monitor|ignore|escalate",
  "draft_response": "if responding, the proposed content",
  "risk_level": "low|medium|high"
}

Authenticity is key — never astroturf or manipulate community sentiment."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._forum_scan, 3600),
            (self._mention_processing, 1800),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process forum engagement tasks."""
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
            self._logger.error("Forum task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _forum_scan(self) -> None:
        """Scan forums for mentions and opportunities every hour."""
        browser_pool = getattr(self._context, "browser_pool", None) if self._context else None

        scan_results = {
            "platforms_scanned": [],
            "mentions_found": 0,
            "opportunities": [],
            "timestamp": time.time(),
        }

        for platform in self.MONITORED_PLATFORMS:
            if browser_pool:
                try:
                    # Would use browser pool to scan platform
                    scan_results["platforms_scanned"].append(platform)
                except Exception as exc:
                    self._logger.warning("Failed to scan %s: %s", platform, str(exc))
            else:
                scan_results["platforms_scanned"].append(f"{platform} (simulated)")

        await self.memory_store("grove.scans", "latest", scan_results)
        self._logger.info(
            "Forum scan complete: %d platforms, %d mentions",
            len(scan_results["platforms_scanned"]),
            scan_results["mentions_found"],
        )

    async def _mention_processing(self) -> None:
        """Process and prioritize mentions every 30 minutes."""
        unprocessed = [m for m in self._mentions if not m.get("processed")]

        for mention in unprocessed:
            # Determine priority based on platform and context
            priority = "low"
            if mention.get("platform") == "hackernews":
                priority = "medium"  # HN mentions are high-visibility
            if mention.get("sentiment") == "negative":
                priority = "high"

            mention["priority"] = priority
            mention["processed"] = True

        await self.memory_store(
            "grove.mentions",
            "processed",
            {"mentions": self._mentions, "updated_at": time.time()},
        )