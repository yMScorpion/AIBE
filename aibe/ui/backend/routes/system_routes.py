# aibe/ui/backend/routes/system_routes.py
"""System management endpoints — boot, shutdown, status."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from aibe.ui.backend.dependencies import get_orchestrator

logger = logging.getLogger("aibe.routes.system")
router = APIRouter(prefix="/api/system", tags=["system"])


class BootRequest(BaseModel):
    tiers: Optional[list[int]] = None
    exclude_agents: Optional[list[str]] = None


class BootResponse(BaseModel):
    status: str
    message: str
    booting_tiers: list[int]
    excluded: list[str]


class ShutdownResponse(BaseModel):
    status: str
    message: str


class SystemStatusResponse(BaseModel):
    running: bool
    mode: str
    total_agents: int
    active_agents: int
    agents_by_status: dict[str, int]
    uptime_seconds: float
    boot_time: Optional[str] = None


# Global state for tracking boot process
_boot_start_time: float = 0.0
_system_mode: str = "initializing"


@router.post("/boot", response_model=BootResponse)
async def boot_system(
    body: BootRequest,
    orchestrator=Depends(get_orchestrator),
):
    """Boot or reboot the agent system."""
    global _boot_start_time, _system_mode

    _boot_start_time = time.time()
    _system_mode = "booting"

    tiers = body.tiers if body.tiers is not None else list(range(0, 9))
    excluded = body.exclude_agents or []

    logger.info("System boot initiated: tiers=%s, excluded=%s", tiers, excluded)

    # Boot is async — we return immediately and let it complete in background
    async def _do_boot():
        global _system_mode
        try:
            await orchestrator.boot(tiers=tiers, exclude_agents=excluded)
            _system_mode = "running"
            logger.info("System boot completed")
        except Exception as exc:
            _system_mode = "error"
            logger.error("System boot failed: %s", str(exc))

    asyncio.create_task(_do_boot())

    return BootResponse(
        status="booting",
        message="System boot initiated",
        booting_tiers=tiers,
        excluded=excluded,
    )


@router.post("/shutdown", response_model=ShutdownResponse)
async def shutdown_system(orchestrator=Depends(get_orchestrator)):
    """Gracefully shut down all agents."""
    global _system_mode

    logger.info("System shutdown initiated")
    _system_mode = "shutting_down"

    async def _do_shutdown():
        global _system_mode
        try:
            await orchestrator.shutdown()
            _system_mode = "stopped"
            logger.info("System shutdown completed")
        except Exception as exc:
            _system_mode = "error"
            logger.error("System shutdown failed: %s", str(exc))

    asyncio.create_task(_do_shutdown())

    return ShutdownResponse(
        status="shutting_down",
        message="System shutdown initiated",
    )


@router.get("/status", response_model=SystemStatusResponse)
async def system_status(orchestrator=Depends(get_orchestrator)):
    """Get current system status."""
    registry = orchestrator.registry
    agents = (
        registry.get_all()
        if hasattr(registry, "get_all")
        else list(getattr(registry, "_agents", {}).values())
    )

    status_counts: dict[str, int] = {}
    for agent in agents:
        status = getattr(agent, "status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

    active = status_counts.get("running", 0) + status_counts.get("ready", 0)

    uptime = time.time() - _boot_start_time if _boot_start_time > 0 else 0

    return SystemStatusResponse(
        running=_system_mode == "running",
        mode=_system_mode,
        total_agents=len(agents),
        active_agents=active,
        agents_by_status=status_counts,
        uptime_seconds=round(uptime, 2),
        boot_time=time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(_boot_start_time)
        ) if _boot_start_time > 0 else None,
    )


@router.post("/start-agency")
async def start_agency(orchestrator=Depends(get_orchestrator)):
    """Force Scout to start researching an idea immediately."""
    global _system_mode
    if _system_mode != "running":
        return {"status": "error", "message": "System must be booted first"}
    
    # Get the bus from the orchestrator
    bus = orchestrator._bus
    if bus:
        await bus.publish("agency.start_research", {"timestamp": time.time(), "trigger": "manual"})
        logger.info("Published agency.start_research event")
        return {"status": "success", "message": "Agency started researching ideas"}
    return {"status": "error", "message": "Message bus not available"}


@router.post("/maintenance")
async def enter_maintenance(orchestrator=Depends(get_orchestrator)):
    """Enter maintenance mode."""
    global _system_mode
    _system_mode = "maintenance"
    logger.info("System entered maintenance mode")
    return {"status": "maintenance", "message": "System in maintenance mode"}


@router.post("/resume")
async def resume_from_maintenance(orchestrator=Depends(get_orchestrator)):
    """Resume from maintenance mode."""
    global _system_mode
    if _system_mode == "maintenance":
        _system_mode = "running"
        logger.info("System resumed from maintenance mode")
        return {"status": "running", "message": "System resumed"}
    return {"status": _system_mode, "message": "System was not in maintenance mode"}