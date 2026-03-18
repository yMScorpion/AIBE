"""Docker container templates for sandboxed code execution."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SandboxTemplate:
    """Docker container configuration for a sandbox type."""

    name: str
    image: str
    memory_limit: str = "256m"
    cpu_limit: float = 0.5
    network_disabled: bool = True
    read_only_rootfs: bool = True
    timeout_seconds: int = 60
    environment: dict[str, str] = field(default_factory=dict)
    volumes: dict[str, str] = field(default_factory=dict)
    entrypoint: str = ""


# ── Pre-defined sandbox templates ─────────────────────────────

SANDBOX_PYTHON = SandboxTemplate(
    name="python",
    image="python:3.12-slim",
    memory_limit="512m",
    cpu_limit=1.0,
    timeout_seconds=120,
    entrypoint="python",
)

SANDBOX_NODE = SandboxTemplate(
    name="node",
    image="node:20-slim",
    memory_limit="512m",
    cpu_limit=1.0,
    timeout_seconds=120,
    entrypoint="node",
)

SANDBOX_SHELL = SandboxTemplate(
    name="shell",
    image="alpine:3.19",
    memory_limit="128m",
    cpu_limit=0.25,
    timeout_seconds=30,
    entrypoint="/bin/sh",
)

SANDBOX_SECURITY_SCAN = SandboxTemplate(
    name="security-scan",
    image="returntocorp/semgrep:latest",
    memory_limit="1g",
    cpu_limit=2.0,
    timeout_seconds=300,
    network_disabled=False,  # Needs network for rule updates
    read_only_rootfs=False,
)

ALL_TEMPLATES = {
    t.name: t
    for t in [SANDBOX_PYTHON, SANDBOX_NODE, SANDBOX_SHELL, SANDBOX_SECURITY_SCAN]
}


__all__ = [
    "ALL_TEMPLATES",
    "SANDBOX_NODE",
    "SANDBOX_PYTHON",
    "SANDBOX_SECURITY_SCAN",
    "SANDBOX_SHELL",
    "SandboxTemplate",
]
