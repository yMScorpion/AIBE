"""Tests for aibe.core.exceptions — exception hierarchy."""

from __future__ import annotations

import pytest

from aibe.core.exceptions import (
    AIBEError,
    AgentError,
    BudgetExceededError,
    BusConnectionError,
    BusError,
    MemoryError,
    RouterBudgetExceededError,
    RouterError,
    SecurityError,
    VaultError,
    VMError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_aibe_error(self) -> None:
        """All custom exceptions should be catchable via AIBEError."""
        exceptions = [
            BusError("test"),
            MemoryError("test"),
            RouterError("test"),
            AgentError("test"),
            SecurityError("test"),
            VaultError("test"),
            VMError("test"),
            BudgetExceededError("test"),
        ]
        for exc in exceptions:
            assert isinstance(exc, AIBEError)

    def test_bus_connection_is_bus_error(self) -> None:
        with pytest.raises(BusError):
            raise BusConnectionError("cannot connect")

    def test_router_budget_exceeded_carries_details(self) -> None:
        exc = RouterBudgetExceededError(
            agent_id="oracle",
            budget_limit=5.0,
            current_spend=5.50,
        )
        assert exc.agent_id == "oracle"
        assert exc.budget_limit == 5.0
        assert exc.current_spend == 5.50
        assert exc.details["agent_id"] == "oracle"

    def test_budget_exceeded_carries_category(self) -> None:
        exc = BudgetExceededError(
            "Over ads budget",
            category="ads",
            limit=100.0,
            current=120.0,
        )
        assert exc.category == "ads"
        assert exc.limit == 100.0
        assert exc.current == 120.0

    def test_details_default_to_empty(self) -> None:
        exc = AIBEError("simple error")
        assert exc.details == {}
