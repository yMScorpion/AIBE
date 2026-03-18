"""Docker-based sandbox VM manager for safe code execution.

Creates isolated, ephemeral containers for running untrusted code
from agents like Forge, Flint, Ember, Synth, and Auditor.
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional

import docker  # type: ignore[import-untyped]
from docker.models.containers import Container  # type: ignore[import-untyped]

from aibe.core.exceptions import VMCreationError, VMExecutionError, VMTimeoutError
from aibe.core.logging import get_logger
from aibe.core.vm_manager.templates import ALL_TEMPLATES, SandboxTemplate

logger = get_logger(__name__)


class SandboxManager:
    """Manages Docker containers for sandboxed code execution.

    Each execution creates an ephemeral container that's destroyed
    after the command completes or times out.
    """

    def __init__(self) -> None:
        self._docker: Optional[docker.DockerClient] = None

    def _get_client(self) -> docker.DockerClient:
        """Get or create the Docker client."""
        if self._docker is None:
            try:
                self._docker = docker.from_env()
                self._docker.ping()
                logger.info("Docker client connected")
            except Exception as exc:
                raise VMCreationError(
                    f"Cannot connect to Docker daemon: {exc}",
                ) from exc
        return self._docker

    async def execute(
        self,
        code: str,
        *,
        template_name: str = "python",
        timeout_seconds: Optional[int] = None,
        environment: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Execute code in a sandboxed container.

        Args:
            code: Code string to execute.
            template_name: Sandbox template name ('python', 'node', 'shell').
            timeout_seconds: Override timeout (uses template default if None).
            environment: Additional environment variables.

        Returns:
            Dict with keys: exit_code, stdout, stderr, timed_out.

        Raises:
            VMCreationError: If container creation fails.
            VMExecutionError: If execution fails unexpectedly.
            VMTimeoutError: If execution exceeds timeout.
        """
        template = ALL_TEMPLATES.get(template_name)
        if template is None:
            raise VMCreationError(
                f"Unknown sandbox template: {template_name}",
                details={"available": list(ALL_TEMPLATES.keys())},
            )

        effective_timeout = timeout_seconds or template.timeout_seconds
        env = {**template.environment, **(environment or {})}

        return await asyncio.get_event_loop().run_in_executor(
            None,
            self._run_container,
            template,
            code,
            effective_timeout,
            env,
        )

    def _run_container(
        self,
        template: SandboxTemplate,
        code: str,
        timeout: int,
        environment: dict[str, str],
    ) -> dict[str, Any]:
        """Run code in a container (blocking, runs in executor)."""
        client = self._get_client()
        container: Optional[Container] = None

        try:
            # Prepare command
            if template.entrypoint == "python":
                command = ["python", "-c", code]
            elif template.entrypoint == "node":
                command = ["node", "-e", code]
            elif template.entrypoint == "/bin/sh":
                command = ["/bin/sh", "-c", code]
            else:
                command = [template.entrypoint, "-c", code]

            container = client.containers.run(
                image=template.image,
                command=command,
                mem_limit=template.memory_limit,
                nano_cpus=int(template.cpu_limit * 1e9),
                network_disabled=template.network_disabled,
                read_only=template.read_only_rootfs,
                environment=environment,
                detach=True,
                auto_remove=False,
                stderr=True,
            )

            # Wait for completion with timeout
            result = container.wait(timeout=timeout)
            exit_code = result.get("StatusCode", -1)

            stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace")
            stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace")

            logger.info(
                "Sandbox execution completed",
                template=template.name,
                exit_code=exit_code,
                stdout_len=len(stdout),
            )

            return {
                "exit_code": exit_code,
                "stdout": stdout[:50000],  # Cap at 50KB
                "stderr": stderr[:10000],  # Cap at 10KB
                "timed_out": False,
            }

        except docker.errors.ContainerError as exc:
            raise VMExecutionError(
                f"Container execution failed: {exc}",
                details={"template": template.name},
            ) from exc

        except Exception as exc:
            if "read timeout" in str(exc).lower() or "timed out" in str(exc).lower():
                raise VMTimeoutError(
                    f"Sandbox execution timed out after {timeout}s",
                    details={"template": template.name, "timeout": timeout},
                ) from exc
            raise VMExecutionError(
                f"Unexpected sandbox error: {exc}",
                details={"template": template.name},
            ) from exc

        finally:
            if container is not None:
                try:
                    container.remove(force=True)
                except Exception:
                    pass

    async def pull_images(self) -> None:
        """Pre-pull all template images."""
        client = self._get_client()
        for template in ALL_TEMPLATES.values():
            try:
                logger.info("Pulling image", image=template.image)
                await asyncio.get_event_loop().run_in_executor(
                    None, client.images.pull, template.image
                )
                logger.info("Image pulled", image=template.image)
            except Exception as exc:
                logger.warning("Failed to pull image", image=template.image, error=str(exc))

    def close(self) -> None:
        """Close the Docker client."""
        if self._docker is not None:
            self._docker.close()
            self._docker = None
            logger.info("Docker client closed")


__all__ = ["SandboxManager"]
