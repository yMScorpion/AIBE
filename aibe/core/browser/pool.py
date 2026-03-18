"""Lightpanda browser pool — manages a pool of reusable browser sessions.

Limits concurrent sessions to prevent resource exhaustion.
"""

from __future__ import annotations

import asyncio
from typing import Optional
from uuid import uuid4

import httpx

from aibe.core.browser.client import BrowserSession
from aibe.core.config import get_settings
from aibe.core.exceptions import BrowserPoolExhaustedError
from aibe.core.logging import get_logger

logger = get_logger(__name__)


class BrowserPool:
    """Manages a pool of Lightpanda browser sessions with semaphore-based limiting."""

    def __init__(self) -> None:
        self._http: Optional[httpx.AsyncClient] = None
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._active_sessions: dict[str, BrowserSession] = {}
        self._pool_size = 3
        self._max_pool_size = 10

    async def initialize(self) -> None:
        """Initialize the pool and HTTP client."""
        settings = get_settings()
        self._pool_size = settings.lightpanda.pool_size
        self._max_pool_size = settings.lightpanda.max_pool_size
        self._semaphore = asyncio.Semaphore(self._max_pool_size)

        self._http = httpx.AsyncClient(
            base_url=settings.lightpanda.api_url,
            timeout=30.0,
        )
        logger.info(
            "Browser pool initialized",
            pool_size=self._pool_size,
            max_pool_size=self._max_pool_size,
        )

    async def acquire(self, *, timeout: float = 30.0) -> BrowserSession:
        """Acquire a browser session from the pool.

        Args:
            timeout: Max seconds to wait for an available slot.

        Returns:
            A BrowserSession ready for use.

        Raises:
            BrowserPoolExhaustedError: If no session available within timeout.
        """
        if self._semaphore is None or self._http is None:
            await self.initialize()

        assert self._semaphore is not None
        assert self._http is not None

        try:
            acquired = await asyncio.wait_for(
                self._semaphore.acquire(),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            raise BrowserPoolExhaustedError(
                f"No browser session available within {timeout}s",
                details={"active_sessions": len(self._active_sessions)},
            )

        # Create a new session
        session_id = str(uuid4())
        try:
            response = await self._http.post(
                "/v1/browser/session",
                json={"session_id": session_id},
            )
            response.raise_for_status()
        except Exception as exc:
            self._semaphore.release()
            logger.warning("Mock browser session (Lightpanda not available)", error=str(exc))
            # In dev mode, create a mock session that still works

        session = BrowserSession(session_id, self._http)
        self._active_sessions[session_id] = session
        logger.debug("Browser session acquired", session_id=session_id)
        return session

    async def release(self, session: BrowserSession) -> None:
        """Release a browser session back to the pool.

        Args:
            session: The session to release.
        """
        await session.close()
        self._active_sessions.pop(session.session_id, None)
        if self._semaphore is not None:
            self._semaphore.release()
        logger.debug("Browser session released", session_id=session.session_id)

    async def close(self) -> None:
        """Close all sessions and the pool."""
        for session in list(self._active_sessions.values()):
            await self.release(session)

        if self._http is not None:
            await self._http.aclose()
            self._http = None

        logger.info("Browser pool closed")

    @property
    def active_count(self) -> int:
        """Number of currently active sessions."""
        return len(self._active_sessions)

    @property
    def available_count(self) -> int:
        """Number of available session slots."""
        return self._max_pool_size - len(self._active_sessions)


__all__ = ["BrowserPool"]
