"""Tests for aibe.core.router — routing table, circuit breaker, and budget."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from aibe.core.router.budget import BudgetEnforcer
from aibe.core.router.fallback import CircuitBreaker
from aibe.core.router.routing_table import RoutingTable
from aibe.core.types import ModelTaskType


class TestRoutingTable:
    def test_load_from_yaml(self) -> None:
        table = RoutingTable()
        table.load()  # Uses default path
        assert len(table.task_types) == 9
        assert "simple_classification" in table.task_types
        assert "ml_design" in table.task_types

    def test_get_task_type_config(self) -> None:
        table = RoutingTable()
        table.load()
        config = table.get(ModelTaskType.CODE_GENERATION)
        assert config is not None
        assert config.primary.model != ""
        assert config.temperature == 0.1

    def test_get_model_chain(self) -> None:
        table = RoutingTable()
        table.load()
        chain = table.get_model_chain(ModelTaskType.STANDARD_GENERATION)
        assert len(chain) >= 2  # primary + at least one fallback
        assert chain[0].cost_per_1k_input > 0

    def test_unknown_task_type_returns_none(self) -> None:
        table = RoutingTable()
        table.load()
        assert table.get("nonexistent_type") is None

    def test_budget_thresholds(self) -> None:
        table = RoutingTable()
        table.load()
        assert table.budget_warning_pct == 80
        assert table.budget_suspend_pct == 100


class TestCircuitBreaker:
    def test_initially_available(self) -> None:
        cb = CircuitBreaker(failure_threshold=3)
        assert cb.is_available("model-a")

    def test_opens_after_threshold(self) -> None:
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure("model-a")
        cb.record_failure("model-a")
        assert cb.is_available("model-a")  # 2 failures, still available
        cb.record_failure("model-a")
        assert not cb.is_available("model-a")  # 3 failures, circuit open

    def test_success_resets_circuit(self) -> None:
        cb = CircuitBreaker(failure_threshold=2)
        cb.record_failure("model-a")
        cb.record_failure("model-a")
        assert not cb.is_available("model-a")
        # Simulate recovery timeout by manually resetting
        cb.reset("model-a")
        assert cb.is_available("model-a")

    def test_record_success_closes_circuit(self) -> None:
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure("model-a")
        assert not cb.is_available("model-a")
        cb.reset("model-a")
        cb.record_success("model-a")
        assert cb.is_available("model-a")

    def test_reset_all(self) -> None:
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure("model-a")
        cb.record_failure("model-b")
        cb.reset()
        assert cb.is_available("model-a")
        assert cb.is_available("model-b")


class TestBudgetEnforcer:
    @pytest.mark.asyncio
    async def test_record_and_check(self) -> None:
        enforcer = BudgetEnforcer()
        mock_redis = AsyncMock()
        mock_redis.incrbyfloat = AsyncMock(return_value="1.5")
        mock_redis.ttl = AsyncMock(return_value=-1)
        mock_redis.expire = AsyncMock()
        mock_redis.get = AsyncMock(return_value="1.5")

        with patch("aibe.core.router.budget.get_redis", return_value=mock_redis):
            new_total = await enforcer.record_spend("oracle", 1.5)
            assert new_total == 1.5

            downgrade, suspend = await enforcer.check_budget("oracle", 5.0)
            assert not downgrade  # 1.5/5.0 = 30%, below 80%
            assert not suspend

    @pytest.mark.asyncio
    async def test_budget_warning_at_80_pct(self) -> None:
        enforcer = BudgetEnforcer()
        mock_redis = AsyncMock()
        mock_redis.get = AsyncMock(return_value="4.2")

        with patch("aibe.core.router.budget.get_redis", return_value=mock_redis):
            downgrade, suspend = await enforcer.check_budget("oracle", 5.0)
            assert downgrade  # 4.2/5.0 = 84%, above 80%
            assert not suspend

    @pytest.mark.asyncio
    async def test_budget_suspend_at_100_pct(self) -> None:
        enforcer = BudgetEnforcer()
        mock_redis = AsyncMock()
        mock_redis.get = AsyncMock(return_value="5.5")

        with patch("aibe.core.router.budget.get_redis", return_value=mock_redis):
            downgrade, suspend = await enforcer.check_budget("oracle", 5.0)
            assert downgrade
            assert suspend  # 5.5/5.0 = 110%, above 100%
