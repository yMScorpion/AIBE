"""Fallback chain with circuit breaker pattern.

Tracks consecutive failures per model and opens the circuit
to prevent cascading failures.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from aibe.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class CircuitState:
    """State of a single circuit breaker."""

    failure_count: int = 0
    last_failure_time: float = 0.0
    state: str = "closed"  # closed | open | half-open
    half_open_calls: int = 0


class CircuitBreaker:
    """Circuit breaker for model fallback chains.

    After `failure_threshold` consecutive failures, the circuit opens.
    After `recovery_timeout` seconds, it moves to half-open for probing.
    If the probe succeeds, it closes. If it fails, it re-opens.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 60.0,
        half_open_max_calls: int = 2,
    ) -> None:
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout_seconds
        self._half_open_max_calls = half_open_max_calls
        self._circuits: dict[str, CircuitState] = {}

    def _get_circuit(self, model: str) -> CircuitState:
        if model not in self._circuits:
            self._circuits[model] = CircuitState()
        return self._circuits[model]

    def is_available(self, model: str) -> bool:
        """Check if a model is available (circuit not open).

        Args:
            model: Model identifier.

        Returns:
            True if the model can be called.
        """
        circuit = self._get_circuit(model)

        if circuit.state == "closed":
            return True

        if circuit.state == "open":
            # Check if recovery timeout has elapsed
            if time.monotonic() - circuit.last_failure_time >= self._recovery_timeout:
                circuit.state = "half-open"
                circuit.half_open_calls = 0
                logger.info("Circuit half-open", model=model)
                return True
            return False

        # half-open: allow limited calls
        return circuit.half_open_calls < self._half_open_max_calls

    def record_success(self, model: str) -> None:
        """Record a successful call, closing the circuit if needed.

        Args:
            model: Model identifier.
        """
        circuit = self._get_circuit(model)
        if circuit.state == "half-open":
            logger.info("Circuit closed after successful probe", model=model)
        circuit.failure_count = 0
        circuit.state = "closed"
        circuit.half_open_calls = 0

    def record_failure(self, model: str) -> None:
        """Record a failed call, potentially opening the circuit.

        Args:
            model: Model identifier.
        """
        circuit = self._get_circuit(model)
        circuit.failure_count += 1
        circuit.last_failure_time = time.monotonic()

        if circuit.state == "half-open":
            circuit.half_open_calls += 1
            if circuit.half_open_calls >= self._half_open_max_calls:
                circuit.state = "open"
                logger.warning("Circuit re-opened after half-open failures", model=model)
            return

        if circuit.failure_count >= self._failure_threshold:
            circuit.state = "open"
            logger.warning(
                "Circuit opened",
                model=model,
                failure_count=circuit.failure_count,
            )

    def reset(self, model: str | None = None) -> None:
        """Reset circuit breaker state.

        Args:
            model: Specific model to reset, or None to reset all.
        """
        if model is not None:
            self._circuits.pop(model, None)
        else:
            self._circuits.clear()


__all__ = ["CircuitBreaker", "CircuitState"]
