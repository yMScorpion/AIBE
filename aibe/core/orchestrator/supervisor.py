# aibe/core/orchestrator/supervisor.py
"""Agent supervisor — monitors health and auto-restarts failed agents."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aibe.agents.registry import AgentRegistry
    from aibe.core.orchestrator.orchestrator import SystemOrchestrator

logger = logging.getLogger("aibe.supervisor")


class AgentSupervisor:
    """Monitors agent health and automatically restarts failed agents.
    
    Features:
    - Periodic health checks
    - Automatic restart with exponential backoff
    - Max restart limit per agent
    - Escalation to Sentinel after max retries
    """

    CHECK_INTERVAL = 30  # seconds
    MAX_RESTARTS = 3
    BASE_COOLDOWN = 60  # seconds

    def __init__(
        self,
        registry: "AgentRegistry",
        orchestrator: "SystemOrchestrator",
    ) -> None:
        self._registry = registry
        self._orchestrator = orchestrator
        self._running = False
        self._task: asyncio.Task | None = None
        self._restart_counts: dict[str, int] = {}
        self._cooldown_until: dict[str, float] = {}

    async def start(self) -> None:
        """Start the supervisor."""
        self._running = True
        self._task = asyncio.create_task(self._run())
        logger.info("Agent supervisor started")

    async def stop(self) -> None:
        """Stop the supervisor."""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Agent supervisor stopped")

    async def _run(self) -> None:
        """Main supervision loop."""
        while self._running:
            try:
                await self._check_all_agents()
            except Exception as exc:
                logger.error("Supervisor check failed: %s", str(exc))
            await asyncio.sleep(self.CHECK_INTERVAL)

    async def _check_all_agents(self) -> None:
        """Check health of all agents."""
        agents = (
            self._registry.get_all()
            if hasattr(self._registry, "get_all")
            else list(getattr(self._registry, "_agents", {}).values())
        )

        current_time = time.time()

        for agent in agents:
            agent_id = getattr(agent, "agent_id", "unknown")
            status = getattr(agent, "status", "unknown")

            # Skip agents that were intentionally stopped
            if status == "stopped":
                continue

            # Skip agents in cooldown
            if agent_id in self._cooldown_until:
                if current_time < self._cooldown_until[agent_id]:
                    continue
                del self._cooldown_until[agent_id]

            # Check if agent needs restart
            needs_restart = False
            reason = ""

            if status == "error":
                needs_restart = True
                reason = "Agent in error state"
            elif status == "ready":
                start_time = getattr(agent, "_start_time", 0)
                if start_time == 0:
                    needs_restart = True
                    reason = "Agent never fully started"

            if needs_restart:
                await self._restart_agent(agent_id, reason)

    async def _restart_agent(self, agent_id: str, reason: str) -> bool:
        """Attempt to restart an agent.
        
        Returns True if restart was successful.
        """
        # Check restart count
        count = self._restart_counts.get(agent_id, 0)
        
        if count >= self.MAX_RESTARTS:
            logger.error(
                "Agent %s exceeded max restarts (%d), notifying Sentinel",
                agent_id,
                self.MAX_RESTARTS,
            )
            await self._notify_sentinel(agent_id, reason)
            return False

        logger.warning(
            "Restarting agent %s (attempt %d/%d): %s",
            agent_id,
            count + 1,
            self.MAX_RESTARTS,
            reason,
        )

        try:
            agent = (
                self._registry.get(agent_id)
                if hasattr(self._registry, "get")
                else getattr(self._registry, "_agents", {}).get(agent_id)
            )

            if agent is None:
                logger.error("Agent %s not found in registry", agent_id)
                return False

            # Stop and restart
            await agent.stop()
            await asyncio.sleep(1)  # Brief pause
            await agent.start()

            self._restart_counts[agent_id] = count + 1
            
            # Set cooldown with exponential backoff
            cooldown = self.BASE_COOLDOWN * (2 ** count)
            self._cooldown_until[agent_id] = time.time() + cooldown
            
            logger.info(
                "Agent %s restarted successfully (cooldown: %ds)",
                agent_id,
                cooldown,
            )
            return True

        except Exception as exc:
            logger.error("Failed to restart agent %s: %s", agent_id, str(exc))
            self._restart_counts[agent_id] = count + 1
            return False

    async def _notify_sentinel(self, agent_id: str, reason: str) -> None:
        """Notify Sentinel about persistent agent failure."""
        bus = getattr(self._orchestrator, "bus", None)
        if bus:
            try:
                await bus.publish(
                    "tasks.escalation.sentinel",
                    {
                        "source": "supervisor",
                        "target": "sentinel",
                        "severity": "high",
                        "message": f"Agent {agent_id} failed {self.MAX_RESTARTS} restart attempts: {reason}",
                        "agent_id": agent_id,
                        "timestamp": time.time(),
                    },
                )
            except Exception:
                pass