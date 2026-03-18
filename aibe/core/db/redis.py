"""Redis async client with connection pool.

Provides separate clients for cache, general use, and Celery broker.
"""

from __future__ import annotations

import redis.asyncio as aioredis

from aibe.core.config import get_settings
from aibe.core.logging import get_logger

logger = get_logger(__name__)

_client: aioredis.Redis | None = None  # type: ignore[type-arg]
_cache_client: aioredis.Redis | None = None  # type: ignore[type-arg]


async def get_redis() -> aioredis.Redis:  # type: ignore[type-arg]
    """Get or create the main Redis client."""
    global _client  # noqa: PLW0603
    if _client is None:
        settings = get_settings()
        _client = aioredis.from_url(
            settings.redis.url,
            max_connections=settings.redis.max_connections,
            decode_responses=True,
        )
        logger.info("Redis client created", url=settings.redis.url)
    return _client


async def get_redis_cache() -> aioredis.Redis:  # type: ignore[type-arg]
    """Get or create the cache-dedicated Redis client."""
    global _cache_client  # noqa: PLW0603
    if _cache_client is None:
        settings = get_settings()
        _cache_client = aioredis.from_url(
            settings.redis.cache_url,
            max_connections=settings.redis.max_connections,
            decode_responses=True,
        )
        logger.info("Redis cache client created", url=settings.redis.cache_url)
    return _cache_client


async def close_redis() -> None:
    """Close all Redis connections."""
    global _client, _cache_client  # noqa: PLW0603
    if _client is not None:
        await _client.aclose()
        _client = None
    if _cache_client is not None:
        await _cache_client.aclose()
        _cache_client = None
    logger.info("Redis connections closed")


__all__ = [
    "close_redis",
    "get_redis",
    "get_redis_cache",
]
