"""Lightpanda browser client for web scraping and automation.

Wraps individual browser sessions from the pool.
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

from aibe.core.config import get_settings
from aibe.core.exceptions import BrowserNavigationError
from aibe.core.logging import get_logger

logger = get_logger(__name__)


class BrowserSession:
    """A single browser session for navigating and extracting content."""

    def __init__(self, session_id: str, http: httpx.AsyncClient) -> None:
        self._session_id = session_id
        self._http = http

    @property
    def session_id(self) -> str:
        return self._session_id

    async def navigate(self, url: str, *, wait_for: str = "load") -> str:
        """Navigate to a URL and return page content.

        Args:
            url: Target URL.
            wait_for: Wait condition ('load', 'networkidle', 'domcontentloaded').

        Returns:
            Page HTML content.

        Raises:
            BrowserNavigationError: If navigation fails.
        """
        try:
            response = await self._http.post(
                "/v1/browser/navigate",
                json={
                    "session_id": self._session_id,
                    "url": url,
                    "wait_for": wait_for,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            return str(data.get("content", ""))
        except Exception as exc:
            raise BrowserNavigationError(
                f"Failed to navigate to {url}: {exc}",
                details={"url": url, "session_id": self._session_id},
            ) from exc

    async def extract_text(self, selector: str = "body") -> str:
        """Extract text content from the current page.

        Args:
            selector: CSS selector for target element.

        Returns:
            Extracted text content.
        """
        try:
            response = await self._http.post(
                "/v1/browser/extract",
                json={
                    "session_id": self._session_id,
                    "selector": selector,
                    "mode": "text",
                },
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            return str(data.get("text", ""))
        except Exception as exc:
            logger.error("Text extraction failed", error=str(exc), selector=selector)
            return ""

    async def screenshot(self) -> bytes:
        """Take a screenshot of the current page.

        Returns:
            PNG image bytes.
        """
        try:
            response = await self._http.post(
                "/v1/browser/screenshot",
                json={"session_id": self._session_id},
            )
            response.raise_for_status()
            return response.content
        except Exception as exc:
            logger.error("Screenshot failed", error=str(exc))
            return b""

    async def execute_js(self, script: str) -> Any:
        """Execute JavaScript in the page context.

        Args:
            script: JavaScript code to execute.

        Returns:
            Result of the script execution.
        """
        try:
            response = await self._http.post(
                "/v1/browser/execute",
                json={
                    "session_id": self._session_id,
                    "script": script,
                },
            )
            response.raise_for_status()
            return response.json().get("result")
        except Exception as exc:
            logger.error("JS execution failed", error=str(exc))
            return None

    async def close(self) -> None:
        """Close this browser session."""
        try:
            await self._http.post(
                "/v1/browser/close",
                json={"session_id": self._session_id},
            )
            logger.debug("Browser session closed", session_id=self._session_id)
        except Exception as exc:
            logger.error("Failed to close session", error=str(exc))


__all__ = ["BrowserSession"]
