# aibe/ui/backend/app.py
"""FastAPI application with full lifespan management."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from aibe.ui.backend.dependencies import (
    set_meeting_store,
    set_orchestrator,
    set_task_tracker,
)

logger = logging.getLogger("aibe.app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Boot orchestrator, task tracker, meeting store; teardown on exit."""
    from aibe.core.orchestrator.orchestrator import SystemOrchestrator
    from aibe.core.task_tracker import TaskTracker
    from aibe.core.meeting_store import MeetingStore
    from aibe.ui.backend.ws_bridge import WSBridge
    from aibe.ui.backend.routes.ws_routes import manager

    orchestrator = SystemOrchestrator()
    tracker = TaskTracker(orchestrator=orchestrator)
    meeting_store = MeetingStore()

    try:
        await orchestrator.boot()
        logger.info("Orchestrator booted successfully")

        set_orchestrator(orchestrator)
        set_task_tracker(tracker)
        set_meeting_store(meeting_store)

        await tracker.start()

        bridge = WSBridge(orchestrator=orchestrator, manager=manager)
        await bridge.start()

        yield
    except Exception:
        logger.exception("Failed during lifespan")
        raise
    finally:
        logger.info("Shutting down …")
        try:
            await bridge.stop()
        except Exception:
            pass
        try:
            await tracker.stop()
        except Exception:
            pass
        try:
            await orchestrator.shutdown()
        except Exception:
            pass
        logger.info("Shutdown complete")


def create_app() -> FastAPI:
    app = FastAPI(
        title="AIBE v2.0",
        version="2.0.0",
        lifespan=lifespan,
    )

    # --- CORS ----------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Middleware -----------------------------------------------------------
    from aibe.ui.backend.middleware.security import SecurityHeadersMiddleware

    app.add_middleware(SecurityHeadersMiddleware)

    # --- Routes --------------------------------------------------------------
    from aibe.ui.backend.routes.agent_routes import router as agent_router
    from aibe.ui.backend.routes.cost_routes import router as cost_router
    from aibe.ui.backend.routes.meeting_routes import router as meeting_router
    from aibe.ui.backend.routes.metrics_routes import router as metrics_router
    from aibe.ui.backend.routes.system_routes import router as system_router
    from aibe.ui.backend.routes.task_routes import router as task_router
    from aibe.ui.backend.routes.ws_routes import router as ws_router

    app.include_router(agent_router)
    app.include_router(task_router)
    app.include_router(meeting_router)
    app.include_router(cost_router)
    app.include_router(system_router)
    app.include_router(metrics_router)
    app.include_router(ws_router)

    # --- Health --------------------------------------------------------------
    @app.get("/api/health")
    async def health() -> dict:
        from aibe.ui.backend.dependencies import _orchestrator

        return {
            "status": "ok",
            "orchestrator": _orchestrator is not None,
            "version": "2.0.0",
        }

    return app


app = create_app()