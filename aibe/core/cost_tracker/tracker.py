"""Real-time cost tracking and aggregation.

Maintains per-agent and per-category spend counters in Redis,
with periodic flush to ClickHouse for long-term analytics.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from aibe.core.config import get_settings
from aibe.core.db.redis import get_redis
from aibe.core.logging import get_logger

logger = get_logger(__name__)


class CostTracker:
    """Tracks all system costs: LLM usage, ads, contractors, infra.

    Uses Redis for real-time counters and can flush to ClickHouse
    for historical analytics.
    """

    # Redis key prefixes
    _PREFIX_LLM = "cost:llm"
    _PREFIX_ADS = "cost:ads"
    _PREFIX_CONTRACTOR = "cost:contractor"
    _PREFIX_INFRA = "cost:infra"

    async def record_llm_cost(
        self,
        agent_id: str,
        model: str,
        tokens_input: int,
        tokens_output: int,
        cost_usd: float,
        task_type: str = "",
    ) -> None:
        """Record an LLM API call cost.

        Args:
            agent_id: Agent that made the call.
            model: Model used.
            tokens_input: Input tokens consumed.
            tokens_output: Output tokens generated.
            cost_usd: Total cost in USD.
            task_type: Task type that triggered the call.
        """
        redis = await get_redis()
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

        pipe = redis.pipeline()
        # Per-agent daily total
        pipe.incrbyfloat(f"{self._PREFIX_LLM}:{agent_id}:{today}", cost_usd)
        # Global daily total
        pipe.incrbyfloat(f"{self._PREFIX_LLM}:total:{today}", cost_usd)
        # Per-model daily total
        pipe.incrbyfloat(f"{self._PREFIX_LLM}:model:{model}:{today}", cost_usd)
        # Token counters
        pipe.incrby(f"tokens:input:{today}", tokens_input)
        pipe.incrby(f"tokens:output:{today}", tokens_output)
        await pipe.execute()

        # Set TTL on keys (7 days)
        for key in [
            f"{self._PREFIX_LLM}:{agent_id}:{today}",
            f"{self._PREFIX_LLM}:total:{today}",
            f"{self._PREFIX_LLM}:model:{model}:{today}",
            f"tokens:input:{today}",
            f"tokens:output:{today}",
        ]:
            ttl = await redis.ttl(key)
            if ttl == -1:
                await redis.expire(key, 604800)  # 7 days

        logger.debug(
            "LLM cost recorded",
            agent_id=agent_id,
            model=model,
            cost_usd=f"{cost_usd:.6f}",
        )

    async def record_ad_spend(
        self,
        platform: str,
        campaign_id: str,
        spend_usd: float,
    ) -> None:
        """Record advertising spend.

        Args:
            platform: Ad platform ('meta', 'google').
            campaign_id: Campaign identifier.
            spend_usd: Amount spent.
        """
        redis = await get_redis()
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

        pipe = redis.pipeline()
        pipe.incrbyfloat(f"{self._PREFIX_ADS}:{platform}:{today}", spend_usd)
        pipe.incrbyfloat(f"{self._PREFIX_ADS}:total:{today}", spend_usd)
        await pipe.execute()

        logger.info("Ad spend recorded", platform=platform, spend_usd=spend_usd)

    async def record_contractor_cost(
        self,
        contractor_name: str,
        amount_usd: float,
    ) -> None:
        """Record contractor payment.

        Args:
            contractor_name: Contractor identifier.
            amount_usd: Payment amount.
        """
        redis = await get_redis()
        month = datetime.now(tz=timezone.utc).strftime("%Y-%m")

        pipe = redis.pipeline()
        pipe.incrbyfloat(f"{self._PREFIX_CONTRACTOR}:{contractor_name}:{month}", amount_usd)
        pipe.incrbyfloat(f"{self._PREFIX_CONTRACTOR}:total:{month}", amount_usd)
        await pipe.execute()

        logger.info("Contractor cost recorded", contractor=contractor_name, amount=amount_usd)

    async def get_daily_llm_spend(self, date: Optional[str] = None) -> float:
        """Get total LLM spend for a day.

        Args:
            date: Date in 'YYYY-MM-DD' format. Defaults to today.

        Returns:
            Total LLM spend in USD.
        """
        redis = await get_redis()
        day = date or datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        value = await redis.get(f"{self._PREFIX_LLM}:total:{day}")
        return float(value) if value else 0.0

    async def get_agent_llm_spend(self, agent_id: str, date: Optional[str] = None) -> float:
        """Get LLM spend for a specific agent today.

        Args:
            agent_id: Agent identifier.
            date: Optional date override.

        Returns:
            Agent's LLM spend in USD.
        """
        redis = await get_redis()
        day = date or datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        value = await redis.get(f"{self._PREFIX_LLM}:{agent_id}:{day}")
        return float(value) if value else 0.0

    async def get_daily_ad_spend(self, date: Optional[str] = None) -> float:
        """Get total ad spend for a day.

        Args:
            date: Optional date override.

        Returns:
            Total ad spend in USD.
        """
        redis = await get_redis()
        day = date or datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        value = await redis.get(f"{self._PREFIX_ADS}:total:{day}")
        return float(value) if value else 0.0

    async def get_monthly_contractor_spend(self, month: Optional[str] = None) -> float:
        """Get total contractor spend for a month.

        Args:
            month: Month in 'YYYY-MM' format. Defaults to current month.

        Returns:
            Total contractor spend in USD.
        """
        redis = await get_redis()
        m = month or datetime.now(tz=timezone.utc).strftime("%Y-%m")
        value = await redis.get(f"{self._PREFIX_CONTRACTOR}:total:{m}")
        return float(value) if value else 0.0

    async def get_daily_token_usage(self, date: Optional[str] = None) -> dict[str, int]:
        """Get token usage for a day.

        Args:
            date: Optional date override.

        Returns:
            Dict with 'input' and 'output' token counts.
        """
        redis = await get_redis()
        day = date or datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        input_tokens = await redis.get(f"tokens:input:{day}")
        output_tokens = await redis.get(f"tokens:output:{day}")
        return {
            "input": int(input_tokens) if input_tokens else 0,
            "output": int(output_tokens) if output_tokens else 0,
        }

    async def get_cost_summary(self) -> dict[str, Any]:
        """Get a full cost summary for today.

        Returns:
            Dict with llm_total, ad_total, token counts, and budget status.
        """
        settings = get_settings()
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

        llm_total = await self.get_daily_llm_spend(today)
        ad_total = await self.get_daily_ad_spend(today)
        tokens = await self.get_daily_token_usage(today)
        contractor_total = await self.get_monthly_contractor_spend()

        return {
            "date": today,
            "llm_spend_usd": round(llm_total, 4),
            "llm_budget_usd": settings.budget.daily_llm_usd,
            "llm_budget_pct": round((llm_total / max(settings.budget.daily_llm_usd, 0.01)) * 100, 1),
            "ad_spend_usd": round(ad_total, 2),
            "ad_budget_usd": settings.budget.daily_ads_cap_usd,
            "contractor_spend_usd": round(contractor_total, 2),
            "contractor_budget_usd": settings.budget.monthly_contractor_usd,
            "tokens_input": tokens["input"],
            "tokens_output": tokens["output"],
        }


__all__ = ["CostTracker"]
