"""WebSocket endpoint for real-time agent event streaming."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from aibe.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections for broadcasting events."""

    def __init__(self) -> None:
        self._connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.append(websocket)
        logger.info("WebSocket client connected", total=len(self._connections))

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.remove(websocket)
        logger.info("WebSocket client disconnected", total=len(self._connections))

    async def broadcast(self, event: dict[str, Any]) -> None:
        """Send an event to all connected clients."""
        dead: list[WebSocket] = []
        message = json.dumps(event, default=str)

        for ws in self._connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)

        for ws in dead:
            self._connections.remove(ws)

    @property
    def active_count(self) -> int:
        return len(self._connections)


# Global connection manager
ws_manager = ConnectionManager()


@router.websocket("/ws/events")
async def event_stream(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time agent events.

    Events include:
    - agent_status_change: {agent_id, old_status, new_status}
    - task_assigned: {task_id, source, target, title}
    - task_completed: {task_id, agent_id, status, duration}
    - meeting_update: {meeting_id, round, participants}
    - budget_alert: {agent_id, spend, limit, level}
    - security_alert: {severity, finding, agent_id}
    - heartbeat: {agent_id, status, uptime}
    """
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            # Client can send subscription preferences
            try:
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                    }))
                elif msg.get("type") == "subscribe":
                    # Future: filter events by subscription
                    await websocket.send_text(json.dumps({
                        "type": "subscribed",
                        "topics": msg.get("topics", ["*"]),
                    }))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as exc:
        logger.error("WebSocket error", error=str(exc))
        ws_manager.disconnect(websocket)


async def broadcast_event(event_type: str, data: dict[str, Any]) -> None:
    """Broadcast an event to all connected WebSocket clients.

    Args:
        event_type: Event type identifier.
        data: Event payload.
    """
    event = {
        "type": event_type,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        **data,
    }
    await ws_manager.broadcast(event)


__all__ = ["broadcast_event", "router", "ws_manager"]
