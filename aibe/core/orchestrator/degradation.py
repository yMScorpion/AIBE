# aibe/core/orchestrator/degradation.py
"""Graceful degradation management for system resilience."""

from __future__ import annotations

import logging
import time
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aibe.agents.registry import AgentRegistry

logger = logging.getLogger("aibe.degradation")


class DegradationMode(str, Enum):
    """System degradation modes."""
    
    NORMAL = "normal"
    DEGRADED = "degraded"
    EMERGENCY = "emergency"
    MAINTENANCE = "maintenance"


class DegradationRestrictions:
    """Restrictions applied in each degradation mode."""

    def __init__(self, mode: DegradationMode) -> None:
        self.mode = mode
        self._restrictions = self._get_restrictions(mode)

    @staticmethod
    def _get_restrictions(mode: DegradationMode) -> dict[str, Any]:
        """Get restrictions for a given mode."""
        if mode == DegradationMode.NORMAL:
            return {
                "autonomous_loops_enabled": True,
                "heartbeat_interval": 30,
                "new_tasks_allowed": True,
                "meetings_allowed": True,
                "log_level": "INFO",
            }
        elif mode == DegradationMode.DEGRADED:
            return {
                "autonomous_loops_enabled": False,
                "heartbeat_interval": 120,
                "new_tasks_allowed": True,
                "meetings_allowed": False,
                "log_level": "DEBUG",
            }
        elif mode == DegradationMode.EMERGENCY:
            return {
                "autonomous_loops_enabled": False,
                "heartbeat_interval": 300,
                "new_tasks_allowed": False,
                "meetings_allowed": False,
                "log_level": "DEBUG",
                "essential_agents_only": ["sentinel", "incident_responder"],
            }
        elif mode == DegradationMode.MAINTENANCE:
            return {
                "autonomous_loops_enabled": False,
                "heartbeat_interval": 60,
                "new_tasks_allowed": False,
                "meetings_allowed": False,
                "log_level": "INFO",
                "drain_existing_tasks": True,
            }
        return {}

    def __getattr__(self, name: str) -> Any:
        return self._restrictions.get(name)


class DegradationManager:
    """Manages system-wide degradation state.
    
    Monitors system health and transitions between modes
    based on defined thresholds.
    """

    # Thresholds for mode transitions
    DEGRADED_ERROR_THRESHOLD = 0.30  # >30% agents in error
    EMERGENCY_ERROR_THRESHOLD = 0.50  # >50% agents in error

    def __init__(self) -> None:
        self._current_mode = DegradationMode.NORMAL
        self._mode_history: list[dict] = []
        self._forced_mode: DegradationMode | None = None

    @property
    def mode(self) -> DegradationMode:
        """Get current degradation mode."""
        return self._forced_mode if self._forced_mode else self._current_mode

    def force_mode(self, mode: DegradationMode) -> None:
        """Force a specific mode (e.g., for maintenance)."""
        self._forced_mode = mode
        self._record_transition(mode, "forced")
        logger.info("Degradation mode forced to %s", mode.value)

    def clear_forced_mode(self) -> None:
        """Clear forced mode and return to automatic assessment."""
        self._forced_mode = None
        logger.info("Forced degradation mode cleared")

    def assess(
        self,
        registry: "AgentRegistry",
        bus_healthy: bool = True,
        memory_healthy: bool = True,
    ) -> DegradationMode:
        """Assess current system state and determine appropriate mode.
        
        Args:
            registry: Agent registry to check agent health
            bus_healthy: Whether NATS bus is healthy
            memory_healthy: Whether memory store is healthy
            
        Returns:
            Assessed degradation mode
        """
        if self._forced_mode:
            return self._forced_mode

        agents = (
            registry.get_all()
            if hasattr(registry, "get_all")
            else list(getattr(registry, "_agents", {}).values())
        )

        if not agents:
            return DegradationMode.EMERGENCY

        # Count agent states
        total = len(agents)
        error_count = sum(1 for a in agents if getattr(a, "status", "") == "error")
        error_rate = error_count / total

        # Check for critical agents
        critical_agents = ["oracle", "minerva", "sentinel"]
        critical_down = sum(
            1 for a in agents
            if getattr(a, "agent_id", "") in critical_agents
            and getattr(a, "status", "") in ("error", "stopped")
        )

        # Determine mode
        new_mode = DegradationMode.NORMAL

        if not bus_healthy or critical_down > 0 or error_rate >= self.EMERGENCY_ERROR_THRESHOLD:
            new_mode = DegradationMode.EMERGENCY
        elif not memory_healthy or error_rate >= self.DEGRADED_ERROR_THRESHOLD:
            new_mode = DegradationMode.DEGRADED

        # Record transition if changed
        if new_mode != self._current_mode:
            self._record_transition(new_mode, f"auto: error_rate={error_rate:.2f}")
            logger.warning(
                "Degradation mode changed: %s -> %s",
                self._current_mode.value,
                new_mode.value,
            )
            self._current_mode = new_mode

        return self._current_mode

    def get_restrictions(self) -> DegradationRestrictions:
        """Get current restrictions based on mode."""
        return DegradationRestrictions(self.mode)

    def _record_transition(self, mode: DegradationMode, reason: str) -> None:
        """Record mode transition for audit."""
        self._mode_history.append({
            "timestamp": time.time(),
            "mode": mode.value,
            "reason": reason,
        })
        # Keep last 100 transitions
        self._mode_history = self._mode_history[-100:]

    def get_history(self) -> list[dict]:
        """Get mode transition history."""
        return list(self._mode_history)