"""Celery application configuration and task autodiscovery."""
from __future__ import annotations

from celery import Celery
from celery.schedules import crontab

from aibe.core.config import get_settings

settings = get_settings()

app = Celery(
    "aibe",
    broker=settings.redis.celery_url,
    backend=settings.redis.celery_url,
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_default_queue="default",
    task_routes={
        "aibe.workers.tasks.security_*": {"queue": "security"},
        "aibe.workers.tasks.ml_*": {"queue": "ml"},
    },
    beat_schedule={
        "budget-check-hourly": {
            "task": "aibe.workers.tasks.check_budgets",
            "schedule": crontab(minute=0),
        },
        "metric-aggregation-hourly": {
            "task": "aibe.workers.tasks.aggregate_metrics",
            "schedule": crontab(minute=5),
        },
        "daily-pnl": {
            "task": "aibe.workers.tasks.generate_daily_pnl",
            "schedule": crontab(hour=23, minute=55),
        },
    },
)

# Autodiscover tasks in aibe.workers.tasks (when that module exists)
# app.autodiscover_tasks(["aibe.workers"])

__all__ = ["app"]