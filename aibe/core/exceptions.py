"""AIBE exception hierarchy.

All custom exceptions inherit from AIBEError, allowing callers to
catch broad categories or specific failures as needed.
"""

from __future__ import annotations


class AIBEError(Exception):
    """Base exception for all AIBE errors."""

    def __init__(self, message: str = "", *, details: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


# ── Infrastructure errors ─────────────────────────────────────


class BusError(AIBEError):
    """NATS message bus communication failure."""


class BusConnectionError(BusError):
    """Cannot connect to NATS server."""


class BusPublishError(BusError):
    """Failed to publish a message."""


class BusSubscriptionError(BusError):
    """Failed to subscribe to a subject."""


class MemoryError(AIBEError):  # noqa: A001  — intentional shadow of builtins
    """OpenViking memory system failure."""


class MemoryConnectionError(MemoryError):
    """Cannot connect to OpenViking."""


class MemoryWriteError(MemoryError):
    """Failed to write to OpenViking namespace."""


class MemoryReadError(MemoryError):
    """Failed to read from OpenViking namespace."""


class RouterError(AIBEError):
    """LLM model routing failure."""


class RouterModelUnavailableError(RouterError):
    """All models in the fallback chain are unavailable."""


class RouterBudgetExceededError(RouterError):
    """Agent has exceeded its daily LLM budget."""

    def __init__(
        self,
        message: str = "Daily LLM budget exceeded",
        *,
        agent_id: str = "",
        budget_limit: float = 0.0,
        current_spend: float = 0.0,
    ) -> None:
        super().__init__(
            message,
            details={
                "agent_id": agent_id,
                "budget_limit": budget_limit,
                "current_spend": current_spend,
            },
        )
        self.agent_id = agent_id
        self.budget_limit = budget_limit
        self.current_spend = current_spend


class RouterValidationError(RouterError):
    """Structured output validation failed after all retries."""


class BrowserError(AIBEError):
    """Lightpanda browser automation failure."""


class BrowserPoolExhaustedError(BrowserError):
    """No browser instances available in the pool."""


class BrowserNavigationError(BrowserError):
    """Failed to navigate to URL."""


class VaultError(AIBEError):
    """HashiCorp Vault secrets management failure."""


class VaultConnectionError(VaultError):
    """Cannot connect to Vault server."""


class VaultSecretNotFoundError(VaultError):
    """Requested secret path does not exist."""


class VMError(AIBEError):
    """Docker-based VM sandbox failure."""


class VMCreationError(VMError):
    """Failed to create sandbox container."""


class VMExecutionError(VMError):
    """Command execution inside sandbox failed."""


class VMTimeoutError(VMError):
    """Sandbox execution exceeded time limit."""


# ── Agent errors ──────────────────────────────────────────────


class AgentError(AIBEError):
    """Agent lifecycle or execution failure."""


class AgentStartupError(AgentError):
    """Agent failed to start."""


class AgentTaskError(AgentError):
    """Agent failed to execute a task."""


class AgentEscalationError(AgentError):
    """Agent escalation to higher tier failed."""


# ── Security errors ───────────────────────────────────────────


class SecurityError(AIBEError):
    """Security subsystem failure."""


class SecurityGateBlockedError(SecurityError):
    """Deployment blocked by security gate due to unresolved findings."""


class SecurityScanError(SecurityError):
    """Security scan tool execution failed."""


# ── Budget errors ─────────────────────────────────────────────


class BudgetExceededError(AIBEError):
    """A budget limit has been exceeded (ads, contractors, etc.)."""

    def __init__(
        self,
        message: str = "Budget exceeded",
        *,
        category: str = "",
        limit: float = 0.0,
        current: float = 0.0,
    ) -> None:
        super().__init__(
            message,
            details={"category": category, "limit": limit, "current": current},
        )
        self.category = category
        self.limit = limit
        self.current = current


# ── Task delegation errors ────────────────────────────────────


class TaskValidationError(AIBEError):
    """Task failed validation checks before assignment."""


class TaskRoutingError(AIBEError):
    """No suitable agent found for task assignment."""


# ── Meeting errors ────────────────────────────────────────────


class MeetingError(AIBEError):
    """Meeting engine failure."""


class MeetingQuorumError(MeetingError):
    """Not enough participants available for meeting."""


__all__ = [
    "AIBEError",
    "AgentError",
    "AgentEscalationError",
    "AgentStartupError",
    "AgentTaskError",
    "BrowserError",
    "BrowserNavigationError",
    "BrowserPoolExhaustedError",
    "BudgetExceededError",
    "BusConnectionError",
    "BusError",
    "BusPublishError",
    "BusSubscriptionError",
    "MeetingError",
    "MeetingQuorumError",
    "MemoryConnectionError",
    "MemoryError",
    "MemoryReadError",
    "MemoryWriteError",
    "RouterBudgetExceededError",
    "RouterError",
    "RouterModelUnavailableError",
    "RouterValidationError",
    "SecurityError",
    "SecurityGateBlockedError",
    "SecurityScanError",
    "TaskRoutingError",
    "TaskValidationError",
    "VMCreationError",
    "VMError",
    "VMExecutionError",
    "VMTimeoutError",
    "VaultConnectionError",
    "VaultError",
    "VaultSecretNotFoundError",
]
