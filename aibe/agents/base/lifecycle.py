"""Agent lifecycle state machine.

Valid transitions:
    INITIALIZING → READY → RUNNING → PAUSED → READY
                                   → STOPPED
                                   → ERROR → READY (via restart)
                                           → DEGRADED
"""

from __future__ import annotations

from aibe.core.logging import get_logger
from aibe.core.types import AgentStatus

logger = get_logger(__name__)

# Valid state transitions: from_state → {allowed_to_states}
VALID_TRANSITIONS: dict[AgentStatus, set[AgentStatus]] = {
    AgentStatus.INITIALIZING: {AgentStatus.READY, AgentStatus.ERROR},
    AgentStatus.READY: {AgentStatus.RUNNING, AgentStatus.STOPPED, AgentStatus.ERROR},
    AgentStatus.RUNNING: {
        AgentStatus.READY,
        AgentStatus.PAUSED,
        AgentStatus.STOPPED,
        AgentStatus.ERROR,
    },
    AgentStatus.PAUSED: {AgentStatus.READY, AgentStatus.STOPPED, AgentStatus.ERROR},
    AgentStatus.STOPPED: {AgentStatus.INITIALIZING},
    AgentStatus.ERROR: {AgentStatus.READY, AgentStatus.DEGRADED, AgentStatus.STOPPED},
    AgentStatus.DEGRADED: {AgentStatus.READY, AgentStatus.STOPPED, AgentStatus.ERROR},
}


class LifecycleManager:
    """Manages agent status transitions with validation."""

    def __init__(self, agent_id: str) -> None:
        self._agent_id = agent_id
        self._status = AgentStatus.INITIALIZING

    @property
    def status(self) -> AgentStatus:
        """Current agent status."""
        return self._status

    def can_transition(self, target: AgentStatus) -> bool:
        """Check if a transition to the target status is valid.

        Args:
            target: Desired target status.

        Returns:
            True if the transition is allowed.
        """
        allowed = VALID_TRANSITIONS.get(self._status, set())
        return target in allowed

    def transition(self, target: AgentStatus, reason: str = "") -> None:
        """Transition to a new status.

        Args:
            target: Target status.
            reason: Optional reason for the transition.

        Raises:
            ValueError: If the transition is not valid.
        """
        if not self.can_transition(target):
            msg = (
                f"Invalid transition for agent {self._agent_id}: "
                f"{self._status.value} → {target.value}"
            )
            raise ValueError(msg)

        old = self._status
        self._status = target
        logger.info(
            "Agent status transition",
            agent_id=self._agent_id,
            old_status=old.value,
            new_status=target.value,
            reason=reason,
        )

    @property
    def is_active(self) -> bool:
        """Check if agent is in an active (can process tasks) state."""
        return self._status in {AgentStatus.READY, AgentStatus.RUNNING}

    @property
    def is_stopped(self) -> bool:
        """Check if agent is fully stopped."""
        return self._status == AgentStatus.STOPPED


__all__ = ["LifecycleManager", "VALID_TRANSITIONS"]
