"""Budget enforcer using Redis atomic counters.

Tracks per-agent daily spend and enforces budget thresholds:
- At 80%: downgrade model tier (use fallbacks)
- At 100%: suspend agent
"""

from __future__ import annotations

from datetime import datetime, timezone

from aibe.core.config import get_settings
from aibe.core.db.redis import get_redis
from aibe.core.exceptions import RouterBudgetExceededError
from aibe.core.logging import get_logger

logger = get_logger(__name__)


class BudgetEnforcer:
    """Per-agent daily LLM budget enforcement via Redis."""

    def _budget_key(self, agent_id: str) -> str:
        """Redis key for today's spend."""
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        return f"budget:{agent_id}:{today}"

    async def record_spend(self, agent_id: str, cost_usd: float) -> float:
        """Record a spend event and return new total.

        Args:
            agent_id: The agent that incurred the cost.
            cost_usd: Cost in USD.

        Returns:
            New total spend for today.
        """
        redis = await get_redis()
        key = self._budget_key(agent_id)

        # Atomic increment (multiply by 1000 for cent precision, Redis INCRBYFLOAT)
        new_total_str = await redis.incrbyfloat(key, cost_usd)
        new_total = float(new_total_str)

        # Ensure key expires at end of day (24h TTL)
        ttl = await redis.ttl(key)
        if ttl == -1:  # No expiry set yet
            await redis.expire(key, 86400)

        logger.debug(
            "Budget spend recorded",
            agent_id=agent_id,
            cost_usd=cost_usd,
            total_today=new_total,
        )
        return new_total

    async def get_spend(self, agent_id: str) -> float:
        """Get current daily spend for an agent.

        Args:
            agent_id: Agent identifier.

        Returns:
            Total spend in USD for today.
        """
        redis = await get_redis()
        key = self._budget_key(agent_id)
        value = await redis.get(key)
        return float(value) if value else 0.0

    async def check_budget(
        self,
        agent_id: str,
        daily_limit_usd: float,
    ) -> tuple[bool, bool]:
        """Check if agent is within budget.

        Args:
            agent_id: Agent identifier.
            daily_limit_usd: Agent's daily budget limit.

        Returns:
            Tuple of (should_downgrade, should_suspend).
            - should_downgrade: True if spend >= 80% of limit.
            - should_suspend: True if spend >= 100% of limit.
        """
        current = await self.get_spend(agent_id)
        settings = get_settings()

        warning_threshold = daily_limit_usd * 0.80
        suspend_threshold = daily_limit_usd * 1.00

        should_downgrade = current >= warning_threshold
        should_suspend = current >= suspend_threshold

        if should_suspend:
            logger.warning(
                "Agent budget SUSPENDED",
                agent_id=agent_id,
                current=current,
                limit=daily_limit_usd,
            )
        elif should_downgrade:
            logger.info(
                "Agent budget warning — downgrading models",
                agent_id=agent_id,
                current=current,
                limit=daily_limit_usd,
            )

        return should_downgrade, should_suspend

    async def enforce(self, agent_id: str, daily_limit_usd: float) -> None:
        """Enforce budget — raise if suspended.

        Args:
            agent_id: Agent identifier.
            daily_limit_usd: Daily budget cap.

        Raises:
            RouterBudgetExceededError: If agent is at 100% budget.
        """
        _, should_suspend = await self.check_budget(agent_id, daily_limit_usd)
        if should_suspend:
            current = await self.get_spend(agent_id)
            raise RouterBudgetExceededError(
                f"Agent {agent_id} daily budget exceeded: ${current:.2f} / ${daily_limit_usd:.2f}",
                agent_id=agent_id,
                budget_limit=daily_limit_usd,
                current_spend=current,
            )

    async def get_all_agent_budgets(self) -> dict[str, float]:
        """Get today's spend for all agents.

        Returns:
            Dict mapping agent_id to current spend.
        """
        redis = await get_redis()
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        pattern = f"budget:*:{today}"

        result: dict[str, float] = {}
        cursor: int | str = 0
        while True:
            cursor, keys = await redis.scan(cursor=int(cursor), match=pattern, count=100)
            for key in keys:
                # key format: budget:{agent_id}:{date}
                parts = str(key).split(":")
                if len(parts) >= 3:
                    agent_id = parts[1]
                    value = await redis.get(key)
                    result[agent_id] = float(value) if value else 0.0
            if cursor == 0:
                break

        return result


__all__ = ["BudgetEnforcer"]
