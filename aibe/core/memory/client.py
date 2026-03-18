"""OpenViking memory client for persistent agent memory.

Provides store, recall, semantic search, and batch operations.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from aibe.core.config import get_settings
from aibe.core.exceptions import MemoryConnectionError, MemoryReadError, MemoryWriteError
from aibe.core.logging import get_logger
from aibe.core.memory.models import MemoryRecord

logger = get_logger(__name__)


class OpenVikingClient:
    """Client for the OpenViking distributed memory system."""

    def __init__(self) -> None:
        self._http: httpx.AsyncClient | None = None

    async def connect(self) -> None:
        """Initialize the HTTP client connection."""
        if self._http is not None:
            return

        settings = get_settings()
        if not settings.openviking.connection_string:
            logger.warning("OpenViking connection string not set — using mock mode")
            return

        try:
            self._http = httpx.AsyncClient(
                base_url=settings.openviking.connection_string,
                headers={
                    "Authorization": f"Bearer {settings.openviking.api_key.get_secret_value()}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
            logger.info("OpenViking client connected")
        except Exception as exc:
            raise MemoryConnectionError(f"Failed to connect to OpenViking: {exc}") from exc

    async def store(
        self,
        namespace: str,
        key: str,
        value: dict[str, Any],
        *,
        metadata: dict[str, Any] | None = None,
        agent_id: str = "",
    ) -> None:
        """Store a value in a namespace.

        Args:
            namespace: Target namespace path.
            key: Unique key within the namespace.
            value: Data to store.
            metadata: Optional metadata tags.
            agent_id: Agent performing the write.
        """
        record = MemoryRecord(
            namespace=namespace,
            key=key,
            value=value,
            metadata=metadata or {},
            agent_id=agent_id,
            timestamp=datetime.now(tz=timezone.utc),
        )

        if self._http is None:
            logger.debug("OpenViking mock store", namespace=namespace, key=key)
            return

        try:
            response = await self._http.post(
                "/v1/memory/store",
                json=record.model_dump(mode="json"),
            )
            response.raise_for_status()
            logger.debug("Stored memory", namespace=namespace, key=key)
        except Exception as exc:
            raise MemoryWriteError(
                f"Failed to store to {namespace}/{key}: {exc}",
                details={"namespace": namespace, "key": key},
            ) from exc

    async def recall(self, namespace: str, key: str) -> dict[str, Any] | None:
        """Recall a specific value by namespace and key.

        Args:
            namespace: Source namespace path.
            key: Key to recall.

        Returns:
            The stored value dict, or None if not found.
        """
        if self._http is None:
            logger.debug("OpenViking mock recall", namespace=namespace, key=key)
            return None

        try:
            response = await self._http.get(
                "/v1/memory/recall",
                params={"namespace": namespace, "key": key},
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            return data.get("value")
        except Exception as exc:
            raise MemoryReadError(
                f"Failed to recall {namespace}/{key}: {exc}",
                details={"namespace": namespace, "key": key},
            ) from exc

    async def semantic_search(
        self,
        namespace: str,
        query: str,
        *,
        limit: int = 10,
        min_score: float = 0.5,
    ) -> list[dict[str, Any]]:
        """Semantic search within a namespace.

        Args:
            namespace: Namespace to search within.
            query: Natural language search query.
            limit: Maximum results to return.
            min_score: Minimum similarity score (0.0-1.0).

        Returns:
            List of matching records with scores.
        """
        if self._http is None:
            logger.debug("OpenViking mock search", namespace=namespace, query=query)
            return []

        try:
            response = await self._http.post(
                "/v1/memory/search",
                json={
                    "namespace": namespace,
                    "query": query,
                    "limit": limit,
                    "min_score": min_score,
                },
            )
            response.raise_for_status()
            results: list[dict[str, Any]] = response.json().get("results", [])
            return results
        except Exception as exc:
            raise MemoryReadError(
                f"Semantic search failed in {namespace}: {exc}",
                details={"namespace": namespace, "query": query},
            ) from exc

    async def batch_write(self, records: list[MemoryRecord]) -> None:
        """Write multiple records in a single batch.

        Args:
            records: List of memory records to store.
        """
        if not records:
            return

        if self._http is None:
            logger.debug("OpenViking mock batch_write", count=len(records))
            return

        try:
            response = await self._http.post(
                "/v1/memory/batch",
                json=[r.model_dump(mode="json") for r in records],
            )
            response.raise_for_status()
            logger.debug("Batch write completed", count=len(records))
        except Exception as exc:
            raise MemoryWriteError(
                f"Batch write failed: {exc}",
                details={"record_count": len(records)},
            ) from exc

    async def disconnect(self) -> None:
        """Close the HTTP client."""
        if self._http is not None:
            await self._http.aclose()
            self._http = None
            logger.info("OpenViking client disconnected")


__all__ = ["OpenVikingClient"]
