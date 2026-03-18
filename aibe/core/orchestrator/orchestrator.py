"""System orchestrator — boots and manages all 35 agents.

The orchestrator is the top-level runtime that:
1. Creates shared infrastructure (bus, memory, router)
2. Instantiates agents via the factory
3. Starts agents in tier order (0 first, 9 last)
4. Monitors health and handles restarts
5. Shuts down gracefully
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional

from aibe.agents.base.context import AgentContext
from aibe.agents.factory import AGENT_CATALOG, create_agent, get_agent_names_by_tier
from aibe.agents.registry import AgentRegistry
from aibe.core.config import get_settings
from aibe.core.logging import get_logger
from aibe.core.memory.client import OpenVikingClient
from aibe.core.message_bus.client import NATSBus
from aibe.core.router.router import ModelRouter
from aibe.core.tools.registry import ToolRegistry
from aibe.core.tools.builtins.tools import register_builtins

logger = get_logger(__name__)


class SystemOrchestrator:
    """Top-level orchestrator for the entire AIBE system.

    Usage:
        orchestrator = SystemOrchestrator()
        await orchestrator.boot()
        # ... system runs ...
        await orchestrator.shutdown()
    """

    def __init__(self) -> None:
        self._registry = AgentRegistry()
        self._bus: Optional[NATSBus] = None
        self._memory: Optional[OpenVikingClient] = None
        self._router: Optional[ModelRouter] = None
        self._tool_registry = ToolRegistry()
        self._running = False

    @property
    def registry(self) -> AgentRegistry:
        return self._registry

    @property
    def tool_registry(self) -> ToolRegistry:
        return self._tool_registry

    async def boot(
        self,
        *,
        tiers: Optional[list[int]] = None,
        exclude_agents: Optional[list[str]] = None,
    ) -> None:
        """Boot the entire system.

        Args:
            tiers: Only boot agents from these tiers (default: all 0-8, skip 9).
            exclude_agents: Agent IDs to skip.
        """
        settings = get_settings()
        logger.info("System boot starting", environment=settings.environment)

        # 1. Initialize shared infrastructure
        self._bus = NATSBus()
        await self._bus.connect()

        self._memory = OpenVikingClient()
        await self._memory.connect()

        self._router = ModelRouter()
        self._router.initialize()

        # 2. Register built-in tools
        register_builtins(self._tool_registry)
        logger.info("Tools registered", count=self._tool_registry.count)

        # 3. Determine which agents to boot
        active_tiers = tiers if tiers is not None else list(range(0, 9))  # Skip Tier 9 (Sales) by default
        excluded = set(exclude_agents or [])

        # 4. Boot agents tier by tier (lower tiers first)
        for tier in sorted(active_tiers):
            agent_ids = get_agent_names_by_tier(tier)
            for agent_id in agent_ids:
                if agent_id in excluded:
                    logger.info("Skipping agent", agent_id=agent_id, reason="excluded")
                    continue

                try:
                    await self._boot_agent(agent_id, tier)
                except Exception as exc:
                    logger.error(
                        "Failed to boot agent",
                        agent_id=agent_id,
                        error=str(exc),
                    )

        self._running = True
        logger.info(
            "System boot complete",
            total_agents=self._registry.count,
            active_agents=self._registry.active_count,
        )

    async def _boot_agent(self, agent_id: str, tier: int) -> None:
        """Boot a single agent."""
        settings = get_settings()

        # Look up budget from config (default $5/day)
        agent_config = self._get_agent_config(agent_id)
        daily_budget = agent_config.get("daily_budget_usd", 5.0)
        agent_name = agent_config.get("name", agent_id.title())

        assert self._bus is not None
        assert self._memory is not None
        assert self._router is not None

        ctx = AgentContext(
            bus=self._bus,
            memory=self._memory,
            router=self._router,
            agent_id=agent_id,
            agent_name=agent_name,
            tier=tier,
            daily_budget_usd=daily_budget,
        )

        agent = create_agent(agent_id, ctx)
        await agent.start()
        self._registry.register(agent)

        logger.info("Agent booted", agent_id=agent_id, tier=tier, budget=daily_budget)

    def _get_agent_config(self, agent_id: str) -> dict[str, Any]:
        """Get agent config from agents.yaml.

        Returns config dict or defaults.
        """
        # In production, this loads from agents.yaml
        # For now, return reasonable defaults
        defaults: dict[str, dict[str, Any]] = {
            "oracle": {"name": "Oracle", "daily_budget_usd": 10.0},
            "minerva": {"name": "Minerva", "daily_budget_usd": 8.0},
            "forge": {"name": "Forge", "daily_budget_usd": 8.0},
            "sentinel": {"name": "Sentinel", "daily_budget_usd": 5.0},
            "helix": {"name": "Helix", "daily_budget_usd": 5.0},
            "nova": {"name": "Nova", "daily_budget_usd": 3.0},
            "ledger": {"name": "Ledger", "daily_budget_usd": 3.0},
            "cipher": {"name": "Cipher", "daily_budget_usd": 5.0},
            "darwin": {"name": "Darwin", "daily_budget_usd": 3.0},
        }
        return defaults.get(agent_id, {"name": agent_id.title(), "daily_budget_usd": 3.0})

    async def shutdown(self) -> None:
        """Gracefully shut down all agents and infrastructure."""
        logger.info("System shutdown starting")
        self._running = False

        # Stop agents in reverse tier order (highest first)
        for agent in sorted(
            self._registry.get_all(),
            key=lambda a: a.ctx.tier,
            reverse=True,
        ):
            try:
                await agent.stop()
                logger.info("Agent stopped", agent_id=agent.agent_id)
            except Exception as exc:
                logger.error("Failed to stop agent", agent_id=agent.agent_id, error=str(exc))

        # Disconnect infrastructure
        if self._bus is not None:
            await self._bus.disconnect()
        if self._memory is not None:
            await self._memory.disconnect()

        logger.info("System shutdown complete")

    def get_status(self) -> dict[str, Any]:
        """Get full system status."""
        return {
            "running": self._running,
            "total_agents": self._registry.count,
            "active_agents": self._registry.active_count,
            "status_summary": self._registry.get_status_summary(),
            "tools_registered": self._tool_registry.count,
        }


__all__ = ["SystemOrchestrator"]
