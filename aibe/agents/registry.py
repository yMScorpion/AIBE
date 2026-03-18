# aibe/agents/registry.py
"""Agent registry — tracks all active agents."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aibe.agents.base.agent import BaseAgent

logger = logging.getLogger("aibe.registry")


class AgentRegistry:
    """Registry for tracking all active agent instances."""

    def __init__(self) -> None:
        self._agents: dict[str, "BaseAgent"] = {}

    def register(self, agent: "BaseAgent") -> None:
        """Register an agent."""
        agent_id = getattr(agent, "agent_id", "unknown")
        self._agents[agent_id] = agent
        logger.info("Agent registered: %s", agent_id)

    def unregister(self, agent_id: str) -> None:
        """Unregister an agent."""
        if agent_id in self._agents:
            del self._agents[agent_id]
            logger.info("Agent unregistered: %s", agent_id)

    def get(self, agent_id: str) -> "BaseAgent | None":
        """Get an agent by ID."""
        return self._agents.get(agent_id)

    def get_all(self) -> list["BaseAgent"]:
        """Get all registered agents."""
        return list(self._agents.values())

    def get_by_tier(self, tier: int) -> list["BaseAgent"]:
        """Get all agents for a specific tier."""
        return [a for a in self._agents.values() if getattr(a, "tier", -1) == tier]

    def get_by_status(self, status: str) -> list["BaseAgent"]:
        """Get all agents with a specific status."""
        return [a for a in self._agents.values() if getattr(a, "status", "") == status]

    @property
    def count(self) -> int:
        """Total number of registered agents."""
        return len(self._agents)

    @property
    def active_count(self) -> int:
        """Number of active (running/ready) agents."""
        return len([
            a for a in self._agents.values()
            if getattr(a, "status", "") in ("running", "ready")
        ])

    def get_status_summary(self) -> dict[str, int]:
        """Get count of agents by status."""
        summary: dict[str, int] = {}
        for agent in self._agents.values():
            status = getattr(agent, "status", "unknown")
            summary[status] = summary.get(status, 0) + 1
        return summary