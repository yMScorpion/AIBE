"""Model routing table loader.

Loads the routing_table.yaml config and provides lookup by ModelTaskType.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from aibe.core.config import PROJECT_ROOT
from aibe.core.logging import get_logger
from aibe.core.types import ModelTaskType

logger = get_logger(__name__)

DEFAULT_ROUTING_TABLE_PATH = PROJECT_ROOT / "aibe" / "config" / "routing_table.yaml"


@dataclass(frozen=True)
class ModelSpec:
    """A specific model with its cost rates."""

    model: str
    cost_per_1k_input: float
    cost_per_1k_output: float


@dataclass(frozen=True)
class TaskTypeConfig:
    """Configuration for a single task type."""

    description: str
    primary: ModelSpec
    fallback: list[ModelSpec] = field(default_factory=list)
    max_tokens: int = 4096
    temperature: float = 0.3


class RoutingTable:
    """In-memory routing table mapping task types to model chains."""

    def __init__(self) -> None:
        self._table: dict[str, TaskTypeConfig] = {}
        self._budget_warning_pct: int = 80
        self._budget_suspend_pct: int = 100

    def load(self, path: Path | None = None) -> None:
        """Load routing table from YAML file.

        Args:
            path: Path to routing_table.yaml. Defaults to config dir.
        """
        config_path = path or DEFAULT_ROUTING_TABLE_PATH
        if not config_path.exists():
            logger.warning("Routing table not found, using empty config", path=str(config_path))
            return

        with open(config_path, encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f)

        task_types = raw.get("task_types", {})
        for type_name, type_cfg in task_types.items():
            primary_raw = type_cfg.get("primary", {})
            primary = ModelSpec(
                model=primary_raw.get("model", ""),
                cost_per_1k_input=primary_raw.get("cost_per_1k_input", 0.0),
                cost_per_1k_output=primary_raw.get("cost_per_1k_output", 0.0),
            )

            fallback_list = []
            for fb in type_cfg.get("fallback", []):
                fallback_list.append(
                    ModelSpec(
                        model=fb.get("model", ""),
                        cost_per_1k_input=fb.get("cost_per_1k_input", 0.0),
                        cost_per_1k_output=fb.get("cost_per_1k_output", 0.0),
                    )
                )

            self._table[type_name] = TaskTypeConfig(
                description=type_cfg.get("description", ""),
                primary=primary,
                fallback=fallback_list,
                max_tokens=type_cfg.get("max_tokens", 4096),
                temperature=type_cfg.get("temperature", 0.3),
            )

        budget_cfg = raw.get("budget", {})
        self._budget_warning_pct = budget_cfg.get("warning_threshold_pct", 80)
        self._budget_suspend_pct = budget_cfg.get("suspend_threshold_pct", 100)

        logger.info("Routing table loaded", task_types=len(self._table))

    def get(self, task_type: ModelTaskType | str) -> TaskTypeConfig | None:
        """Look up config for a task type.

        Args:
            task_type: The task type enum value or string name.

        Returns:
            TaskTypeConfig or None if not found.
        """
        key = task_type.value if isinstance(task_type, ModelTaskType) else task_type
        return self._table.get(key)

    def get_model_chain(self, task_type: ModelTaskType | str) -> list[ModelSpec]:
        """Get the ordered list of models (primary + fallbacks) for a task type.

        Args:
            task_type: The task type.

        Returns:
            List of ModelSpec starting with primary, then fallbacks.
        """
        config = self.get(task_type)
        if config is None:
            return []
        return [config.primary, *config.fallback]

    @property
    def budget_warning_pct(self) -> int:
        """Percentage at which to downgrade model tier."""
        return self._budget_warning_pct

    @property
    def budget_suspend_pct(self) -> int:
        """Percentage at which to suspend agent."""
        return self._budget_suspend_pct

    @property
    def task_types(self) -> list[str]:
        """List of all configured task type names."""
        return list(self._table.keys())


__all__ = ["ModelSpec", "RoutingTable", "TaskTypeConfig"]
