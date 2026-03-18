"""ClickHouse analytics client for cost/metrics/event storage."""

from __future__ import annotations

from typing import Any

import clickhouse_connect
from clickhouse_connect.driver.client import Client as CHClient

from aibe.core.config import get_settings
from aibe.core.logging import get_logger

logger = get_logger(__name__)

_client: CHClient | None = None


def get_clickhouse() -> CHClient:
    """Get or create the ClickHouse client."""
    global _client  # noqa: PLW0603
    if _client is None:
        settings = get_settings()
        _client = clickhouse_connect.get_client(
            host=settings.clickhouse.host,
            port=settings.clickhouse.port,
            username=settings.clickhouse.user,
            password=settings.clickhouse.password.get_secret_value(),
            database=settings.clickhouse.database,
        )
        logger.info(
            "ClickHouse client created",
            host=settings.clickhouse.host,
            database=settings.clickhouse.database,
        )
    return _client


def insert_event(table: str, data: list[dict[str, Any]]) -> None:
    """Insert rows into a ClickHouse table.

    Args:
        table: Target table name.
        data: List of row dictionaries.
    """
    if not data:
        return
    client = get_clickhouse()
    columns = list(data[0].keys())
    rows = [[row[col] for col in columns] for row in data]
    client.insert(table, rows, column_names=columns)
    logger.debug("ClickHouse insert", table=table, row_count=len(data))


def query(sql: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Execute a ClickHouse query and return rows as dicts.

    Args:
        sql: SQL query string.
        parameters: Optional query parameters.

    Returns:
        List of row dictionaries.
    """
    client = get_clickhouse()
    result = client.query(sql, parameters=parameters or {})
    columns = result.column_names
    return [dict(zip(columns, row, strict=True)) for row in result.result_rows]


def close_clickhouse() -> None:
    """Close the ClickHouse client."""
    global _client  # noqa: PLW0603
    if _client is not None:
        _client.close()
        _client = None
        logger.info("ClickHouse client closed")


__all__ = [
    "close_clickhouse",
    "get_clickhouse",
    "insert_event",
    "query",
]
