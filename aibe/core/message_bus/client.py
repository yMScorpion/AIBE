"""NATS message bus client with JetStream support.

Provides publish/subscribe, request-reply, auto-reconnect,
and JetStream stream management.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

import nats
from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg
from nats.js.client import JetStreamContext

from aibe.core.config import get_settings
from aibe.core.exceptions import BusConnectionError, BusPublishError, BusSubscriptionError
from aibe.core.logging import get_logger
from aibe.core.message_bus.models import MessageBase
from aibe.core.message_bus.signing import sign_message
from aibe.core.message_bus.streams import ALL_STREAMS, StreamConfig

logger = get_logger(__name__)

MessageHandler = Callable[[MessageBase], Awaitable[None]]


class NATSBus:
    """High-level NATS client wrapping publish, subscribe, and JetStream."""

    def __init__(self) -> None:
        self._nc: NATSClient | None = None
        self._js: JetStreamContext | None = None
        self._subscriptions: list[Any] = []

    @property
    def is_connected(self) -> bool:
        """Check if the NATS client is connected."""
        return self._nc is not None and self._nc.is_connected

    async def connect(self) -> None:
        """Connect to NATS server and set up JetStream."""
        if self.is_connected:
            return

        settings = get_settings()
        try:
            self._nc = await nats.connect(
                servers=[settings.nats.url],
                max_reconnect_attempts=settings.nats.max_reconnect_attempts,
                reconnect_time_wait=settings.nats.reconnect_time_wait_seconds,
                error_cb=self._on_error,
                reconnected_cb=self._on_reconnect,
                disconnected_cb=self._on_disconnect,
            )
            self._js = self._nc.jetstream()
            logger.info("Connected to NATS", server=settings.nats.url)

            # Ensure all JetStream streams exist
            await self._ensure_streams()

        except Exception as exc:
            raise BusConnectionError(
                f"Failed to connect to NATS: {exc}",
                details={"server": settings.nats.url},
            ) from exc

    async def _ensure_streams(self) -> None:
        """Create or update JetStream streams."""
        if self._js is None:
            return

        for stream_cfg in ALL_STREAMS:
            try:
                await self._js.find_stream_name_by_subject(stream_cfg.subjects[0])
                logger.debug("Stream already exists", stream=stream_cfg.name)
            except Exception:
                await self._js.add_stream(
                    name=stream_cfg.name,
                    subjects=stream_cfg.subjects,
                    max_bytes=stream_cfg.max_bytes,
                    max_age=stream_cfg.max_age_hours * 3600 * 1_000_000_000,  # nanoseconds
                    storage=stream_cfg.storage,
                    retention=stream_cfg.retention,
                    num_replicas=stream_cfg.num_replicas,
                    duplicate_window=stream_cfg.duplicate_window_seconds * 1_000_000_000,
                )
                logger.info("Created JetStream stream", stream=stream_cfg.name)

    async def publish(self, subject: str, message: MessageBase) -> None:
        """Publish a signed message to a subject.

        Args:
            subject: NATS subject (e.g. 'tasks.assign.oracle').
            message: Pydantic message to publish.

        Raises:
            BusPublishError: If publish fails.
        """
        if not self.is_connected or self._js is None:
            raise BusPublishError("Not connected to NATS")

        # Sign the message
        message.signature = sign_message(message)

        try:
            data = message.model_dump_json().encode("utf-8")
            await self._js.publish(subject, data)
            logger.debug(
                "Published message",
                subject=subject,
                message_id=message.message_id,
                source=message.source_agent,
            )
        except Exception as exc:
            raise BusPublishError(
                f"Failed to publish to {subject}: {exc}",
                details={"subject": subject, "message_id": message.message_id},
            ) from exc

    async def subscribe(
        self,
        subject: str,
        handler: Callable[[Msg], Awaitable[None]],
        *,
        queue: str = "",
        durable: str = "",
    ) -> None:
        """Subscribe to a subject with a message handler.

        Args:
            subject: NATS subject pattern (supports wildcards).
            handler: Async callback receiving raw NATS messages.
            queue: Queue group name for load balancing.
            durable: Durable consumer name for JetStream.

        Raises:
            BusSubscriptionError: If subscription fails.
        """
        if not self.is_connected or self._js is None:
            raise BusSubscriptionError("Not connected to NATS")

        try:
            if durable:
                sub = await self._js.subscribe(
                    subject,
                    queue=queue,
                    durable=durable,
                    cb=handler,
                )
            else:
                if self._nc is None:
                    raise BusSubscriptionError("NATS client is None")
                sub = await self._nc.subscribe(subject, queue=queue, cb=handler)

            self._subscriptions.append(sub)
            logger.info(
                "Subscribed to subject",
                subject=subject,
                queue=queue,
                durable=durable,
            )
        except BusSubscriptionError:
            raise
        except Exception as exc:
            raise BusSubscriptionError(
                f"Failed to subscribe to {subject}: {exc}",
                details={"subject": subject},
            ) from exc

    async def request(
        self,
        subject: str,
        message: MessageBase,
        timeout: float = 10.0,
    ) -> bytes:
        """Send a request and wait for a reply.

        Args:
            subject: NATS subject.
            message: Request message.
            timeout: Seconds to wait for reply.

        Returns:
            Raw reply data.
        """
        if not self.is_connected or self._nc is None:
            raise BusPublishError("Not connected to NATS")

        message.signature = sign_message(message)
        data = message.model_dump_json().encode("utf-8")
        response = await self._nc.request(subject, data, timeout=timeout)
        return response.data

    async def disconnect(self) -> None:
        """Gracefully disconnect from NATS."""
        for sub in self._subscriptions:
            try:
                await sub.unsubscribe()
            except Exception:
                pass
        self._subscriptions.clear()

        if self._nc is not None:
            await self._nc.drain()
            self._nc = None
            self._js = None
            logger.info("Disconnected from NATS")

    # ── Internal callbacks ────────────────────────────────────

    async def _on_error(self, exc: Exception) -> None:
        logger.error("NATS error", error=str(exc))

    async def _on_reconnect(self) -> None:
        logger.warning("NATS reconnected")

    async def _on_disconnect(self) -> None:
        logger.warning("NATS disconnected")


__all__ = ["NATSBus"]
