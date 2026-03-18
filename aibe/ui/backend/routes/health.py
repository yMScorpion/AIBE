"""Health check routes."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "aibe",
        "version": "2.0.0",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


@router.get("/ready")
async def readiness_check() -> dict[str, str]:
    """Readiness check — verifies all dependencies are available."""
    # TODO: Check DB, Redis, NATS connectivity
    return {
        "status": "ready",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
