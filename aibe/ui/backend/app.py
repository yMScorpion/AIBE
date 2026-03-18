"""AIBE FastAPI application factory.

Creates the FastAPI app with middleware, lifespan events,
and all route groups.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from aibe.core.config import get_settings
from aibe.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan — startup and shutdown hooks."""
    settings = get_settings()
    setup_logging(
        log_level=settings.log_level,
        json_format=settings.is_production,
    )
    logger.info(
        "AIBE starting",
        environment=settings.environment,
        version="2.0.0",
    )
    # ── Startup ───────────────────────────────────────────
    # Connect infrastructure (lazy — each component connects on first use)
    logger.info("Infrastructure connections will be established on first use")
    yield
    # ── Shutdown ──────────────────────────────────────────
    logger.info("AIBE shutting down")
    # Cleanup will be handled by individual component shutdown hooks


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(
        title="AIBE — AI Business Engine",
        description="Autonomous AI company with 41 specialised agents",
        version="2.0.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )
    # ── CORS ──────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # ── Routes ────────────────────────────────────────────
    from aibe.ui.backend.routes import health, agents, tasks, meetings, costs, websocket

    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
    app.include_router(meetings.router, prefix="/api/meetings", tags=["Meetings"])
    app.include_router(costs.router, prefix="/api/costs", tags=["Costs"])
    app.include_router(websocket.router, tags=["WebSocket"])
    # ── Dashboard Static Files ────────────────────────────
    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    if frontend_dir.is_dir():

        @app.get("/", include_in_schema=False)
        async def dashboard() -> FileResponse:
            return FileResponse(frontend_dir / "index.html")

        app.mount(
            "/static",
            StaticFiles(directory=str(frontend_dir)),
            name="static",
        )
    logger.info("AIBE app created", routes=len(app.routes))
    return app


# Uvicorn entrypoint
app = create_app()
__all__ = ["app", "create_app"]