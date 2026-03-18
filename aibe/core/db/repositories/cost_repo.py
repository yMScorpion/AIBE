# aibe/core/db/repositories/cost_repo.py
"""Cost record CRUD repository."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from aibe.core.db.models import CostRecordModel


class CostRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def record(
        self,
        agent_id: str,
        model: str,
        tokens_in: int,
        tokens_out: int,
        cost_usd: float,
        task_type: str = "inference",
    ) -> CostRecordModel:
        rec = CostRecordModel(
            agent_id=agent_id,
            model=model,
            task_type=task_type,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost_usd,
        )
        self._session.add(rec)
        await self._session.commit()
        return rec

    async def get_agent_total(self, agent_id: str, since: datetime | None = None) -> float:
        stmt = select(func.coalesce(func.sum(CostRecordModel.cost_usd), 0.0)).where(
            CostRecordModel.agent_id == agent_id
        )
        if since:
            stmt = stmt.where(CostRecordModel.created_at >= since)
        result = await self._session.execute(stmt)
        return float(result.scalar_one())

    async def get_daily_totals(self, days: int = 7) -> list[dict]:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = (
            select(
                func.date(CostRecordModel.created_at).label("day"),
                func.sum(CostRecordModel.cost_usd).label("total"),
            )
            .where(CostRecordModel.created_at >= since)
            .group_by(func.date(CostRecordModel.created_at))
            .order_by(func.date(CostRecordModel.created_at))
        )
        result = await self._session.execute(stmt)
        return [{"date": str(row.day), "spent_usd": float(row.total)} for row in result]

    async def get_by_agent(self, agent_id: str, since: datetime | None = None) -> list[CostRecordModel]:
        stmt = (
            select(CostRecordModel)
            .where(CostRecordModel.agent_id == agent_id)
            .order_by(CostRecordModel.created_at.desc())
            .limit(200)
        )
        if since:
            stmt = stmt.where(CostRecordModel.created_at >= since)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())