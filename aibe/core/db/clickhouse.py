# aibe/core/db/clickhouse.py
"""Optional ClickHouse sink for analytics data."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("aibe.clickhouse")


@dataclass
class CostEvent:
    agent_id: str
    model: str
    task_type: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    timestamp: datetime


class ClickHouseSink:
    """Batch-insert cost events into ClickHouse.

    Falls back gracefully if ClickHouse is unavailable.
    """

    BATCH_SIZE = 100
    FLUSH_INTERVAL = 10.0  # seconds

    def __init__(self) -> None:
        self._url = os.getenv("CLICKHOUSE_URL", "http://localhost:8123")
        self._database = os.getenv("CLICKHOUSE_DB", "aibe_analytics")
        self._buffer: deque[CostEvent] = deque()
        self._running = False
        self._flush_task: asyncio.Task | None = None
        self._available = False
        self._client: Any = None

    async def start(self) -> None:
        self._running = True
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self._url}/ping", timeout=5)
                self._available = resp.status_code == 200
        except Exception:
            self._available = False
            logger.warning("ClickHouse unavailable — running in memory-only mode")

        if self._available:
            await self._ensure_table()
            self._flush_task = asyncio.create_task(self._flush_loop())
            logger.info("ClickHouse sink started")

    async def stop(self) -> None:
        self._running = False
        if self._flush_task and not self._flush_task.done():
            self._flush_task.cancel()
        if self._buffer and self._available:
            await self._flush()

    async def _ensure_table(self) -> None:
        ddl = f"""
        CREATE TABLE IF NOT EXISTS {self._database}.llm_costs (
            agent_id String,
            model String,
            task_type String,
            tokens_in UInt32,
            tokens_out UInt32,
            cost_usd Float64,
            timestamp DateTime
        ) ENGINE = MergeTree()
        ORDER BY (agent_id, timestamp)
        """
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                await client.post(self._url, content=ddl, timeout=10)
        except Exception:
            logger.warning("Could not create ClickHouse table")

    def push(self, event: CostEvent) -> None:
        self._buffer.append(event)
        if len(self._buffer) >= self.BATCH_SIZE and self._available:
            asyncio.create_task(self._flush())

    async def _flush(self) -> None:
        if not self._buffer or not self._available:
            return
        batch = []
        while self._buffer and len(batch) < self.BATCH_SIZE:
            batch.append(self._buffer.popleft())

        rows = "\n".join(
            f"('{e.agent_id}','{e.model}','{e.task_type}',{e.tokens_in},{e.tokens_out},{e.cost_usd},'{e.timestamp.strftime('%Y-%m-%d %H:%M:%S')}')"
            for e in batch
        )
        sql = f"INSERT INTO {self._database}.llm_costs VALUES {rows}"

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                await client.post(self._url, content=sql, timeout=10)
        except Exception:
            logger.warning("ClickHouse flush failed, returning %d events to buffer", len(batch))
            self._buffer.extendleft(reversed(batch))

    async def _flush_loop(self) -> None:
        while self._running:
            await asyncio.sleep(self.FLUSH_INTERVAL)
            if self._buffer:
                await self._flush()

    async def query_daily_history(self, days: int = 7) -> list[dict]:
        if not self._available:
            return []
        sql = f"""
        SELECT toDate(timestamp) AS day, sum(cost_usd) AS total
        FROM {self._database}.llm_costs
        WHERE timestamp >= today() - {days}
        GROUP BY day ORDER BY day
        """
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self._url,
                    content=sql,
                    params={"default_format": "JSONEachRow"},
                    timeout=10,
                )
                import json

                return [json.loads(line) for line in resp.text.strip().split("\n") if line]
        except Exception:
            return []