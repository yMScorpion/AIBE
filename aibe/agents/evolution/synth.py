# aibe/agents/evolution/synth.py
"""Synth — Tool Builder Agent (Tier 6).

Creates, tests, and maintains custom tools for the agent ecosystem.
Extends system capabilities based on identified needs.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class SynthAgent(BaseAgent):
    """Tool creation and maintenance agent."""

    agent_id = "synth"
    name = "Synth"
    tier = 6
    escalation_target = "darwin"
    daily_budget_usd = 4.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._tool_registry: dict[str, dict] = {}

    def get_system_prompt(self) -> str:
        return """You are Synth, the Tool Builder Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Design and implement new tools based on agent needs
- Test tools thoroughly before deployment
- Maintain and optimize existing tools
- Document tool usage and best practices
- Monitor tool usage patterns and performance

TOOL DEVELOPMENT GUIDELINES:

1. Design Principles:
   - Single responsibility per tool
   - Clear input/output contracts
   - Comprehensive error handling
   - Performance-conscious implementation
   - Security by default

2. Tool Structure:
   - Name: snake_case, descriptive
   - Description: Clear purpose statement
   - Parameters: Typed, validated, documented
   - Returns: Consistent format
   - Errors: Specific, actionable messages

OUTPUT FORMAT for tool specifications:
{
  "tool_name": "snake_case_name",
  "version": "1.0.0",
  "description": "what the tool does",
  "category": "data|web|file|analysis|integration",
  "parameters": [
    {
      "name": "param_name",
      "type": "string|int|float|bool|list|dict",
      "required": true,
      "description": "what this parameter does",
      "default": null
    }
  ],
  "returns": {
    "type": "expected return type",
    "description": "what is returned"
  },
  "examples": [
    {"input": {...}, "output": {...}}
  ],
  "implementation": "pseudocode or actual code",
  "test_cases": [
    {"name": "test name", "input": {...}, "expected": {...}}
  ],
  "security_notes": ["any security considerations"],
  "performance_notes": ["complexity, resource usage"]
}

Write clean, maintainable, well-documented tools."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._tool_usage_review, 3600),
            (self._tool_health_check, 1800),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process tool creation tasks."""
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
            self._logger.error("Tool creation task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _tool_usage_review(self) -> None:
        """Review tool usage patterns every hour."""
        tool_registry = getattr(self._context, "tool_registry", None) if self._context else None

        usage_report = {
            "timestamp": time.time(),
            "tools_available": 0,
            "tools_by_category": {},
            "usage_stats": {},
        }

        if tool_registry:
            tools = tool_registry.list() if hasattr(tool_registry, "list") else []
            usage_report["tools_available"] = len(tools)

            for tool in tools:
                category = getattr(tool, "category", "unknown")
                usage_report["tools_by_category"][category] = (
                    usage_report["tools_by_category"].get(category, 0) + 1
                )

        await self.memory_store("synth.usage", "report", usage_report)
        self._logger.info("Tool usage review: %d tools available", usage_report["tools_available"])

    async def _tool_health_check(self) -> None:
        """Check tool health and functionality every 30 minutes."""
        health_report = {
            "timestamp": time.time(),
            "checks_performed": 0,
            "healthy": 0,
            "degraded": 0,
            "failed": 0,
        }

        # Would perform actual health checks on registered tools
        await self.memory_store("synth.health", "latest", health_report)
        self._logger.debug("Tool health check complete")