"""AIBE structured logging with structlog.

Provides JSON-formatted logging with automatic context binding
for agent_id, task_id, and trace_id across the system.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog


def setup_logging(*, log_level: str = "INFO", json_format: bool = True) -> None:
    """Configure structlog for the entire application.

    Call once at application startup (e.g. in FastAPI lifespan or
    worker init).

    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        json_format: If True, output JSON lines. If False, use colored console output.
    """
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if json_format:
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Quiet noisy third-party loggers
    for name in ("httpx", "httpcore", "uvicorn.access", "sqlalchemy.engine"):
        logging.getLogger(name).setLevel(logging.WARNING)


def get_logger(name: str, **initial_context: Any) -> structlog.stdlib.BoundLogger:
    """Get a bound structlog logger with optional initial context.

    Args:
        name: Logger name (typically __name__ or agent id).
        **initial_context: Key-value pairs to bind permanently to this logger.

    Returns:
        A BoundLogger instance.

    Example:
        >>> logger = get_logger("oracle", agent_id="oracle", tier=0)
        >>> logger.info("Starting KPI monitor loop")
    """
    logger: structlog.stdlib.BoundLogger = structlog.get_logger(name)
    if initial_context:
        logger = logger.bind(**initial_context)
    return logger


def bind_context(**context: Any) -> None:
    """Bind context variables for the current execution context.

    Uses contextvars so the bindings are automatically propagated
    to all log calls within the same async task / thread.

    Args:
        **context: Key-value pairs (e.g. trace_id, task_id, agent_id).
    """
    structlog.contextvars.bind_contextvars(**context)


def clear_context() -> None:
    """Clear all bound context variables."""
    structlog.contextvars.clear_contextvars()


__all__ = [
    "bind_context",
    "clear_context",
    "get_logger",
    "setup_logging",
]
