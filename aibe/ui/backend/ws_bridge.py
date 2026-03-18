# aibe/ui/backend/ws_bridge.py
"""Bridge NATS events to WebSocket clients."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aibe.core.orchestrator.orchestrator import SystemOrchestrator
    from aibe.ui.backend.routes.ws_routes import ConnectionManager

logger = logging.getLogger("aibe.ws_bridge")

NATS_TO_WS = {
    "agent.heartbeat.>": "agent_heartbeat",
    "agent.status.>": "agent_status_changed",
    "tasks.result.>": "task_completed",
    "tasks.escalation.>": "escalation",
    "meetings.>": "meeting_update",
}


class WSBridge:
    """Subscribe to NATS subjects and forward events to all WebSocket clients."""

    def __init__(self, orchestrator: "SystemOrchestrator", manager: "ConnectionManager") -> None:
        self._orchestrator = orchestrator
        self._manager = manager
        self._running = False
        self._heartbeat_task: asyncio.Task | None = None

    async def start(self) -> None:
        self._running = True
        bus = getattr(self._orchestrator, "bus", None)

        if bus is not None:
            for subject, event_name in NATS_TO_WS.items():
                try:
                    await bus.subscribe(subject, self._make_handler(event_name))
                except Exception:
                    logger.warning("Could not subscribe to %s", subject)

        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        logger.info("WSBridge started")

    async def stop(self) -> None:
        self._running = False
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
        logger.info("WSBridge stopped")

    def _make_handler(self, event_name: str):
        async def handler(data):
            msg = {
                "event": event_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": data if isinstance(data, dict) else {"raw": str(data)},
            }
            await self._manager.broadcast(json.dumps(msg))

        return handler

    async def _heartbeat_loop(self) -> None:
        while self._running:
            try:
                registry = self._orchestrator.registry
                agents = registry.get_all() if hasattr(registry, "get_all") else list(registry._agents.values())
                agent_statuses = {}
                for a in agents:
                    aid = getattr(a, "agent_id", "unknown")
                    agent_statuses[aid] = getattr(a, "status", "unknown")

                msg = {
                    "event": "system_heartbeat",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "data": {
                        "active_agents": len(agents),
                        "statuses": agent_statuses,
                    },
                }
                await self._manager.broadcast(json.dumps(msg))
            except Exception:
                logger.debug("Heartbeat broadcast error", exc_info=True)
            await asyncio.sleep(30)