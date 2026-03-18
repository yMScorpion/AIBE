"""HashiCorp Vault client for secrets management.

Handles reading, writing, and rotating secrets via the Vault KV v2 API.
"""

from __future__ import annotations

from typing import Any, Optional

import hvac  # type: ignore[import-untyped]

from aibe.core.config import get_settings
from aibe.core.exceptions import VaultConnectionError, VaultSecretNotFoundError
from aibe.core.logging import get_logger

logger = get_logger(__name__)

_client: Optional[hvac.Client] = None


def get_vault_client() -> hvac.Client:
    """Get or create the Vault client (lazy singleton).

    Returns:
        Authenticated hvac.Client.

    Raises:
        VaultConnectionError: If Vault is unreachable or auth fails.
    """
    global _client  # noqa: PLW0603
    if _client is not None and _client.is_authenticated():
        return _client

    settings = get_settings()
    try:
        _client = hvac.Client(
            url=settings.vault.addr,
            token=settings.vault.token.get_secret_value(),
        )
        if not _client.is_authenticated():
            raise VaultConnectionError(
                "Vault authentication failed",
                details={"addr": settings.vault.addr},
            )
        logger.info("Vault client connected", addr=settings.vault.addr)
        return _client
    except VaultConnectionError:
        raise
    except Exception as exc:
        raise VaultConnectionError(
            f"Failed to connect to Vault: {exc}",
            details={"addr": settings.vault.addr},
        ) from exc


def read_secret(path: str, mount_point: Optional[str] = None) -> dict[str, Any]:
    """Read a secret from Vault KV v2.

    Args:
        path: Secret path (e.g. 'openrouter/api-key').
        mount_point: KV mount point (defaults to settings).

    Returns:
        Secret data dict.

    Raises:
        VaultSecretNotFoundError: If the path does not exist.
    """
    client = get_vault_client()
    settings = get_settings()
    mp = mount_point or settings.vault.mount_point

    try:
        response = client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point=mp,
        )
        data: dict[str, Any] = response["data"]["data"]
        logger.debug("Secret read", path=path)
        return data
    except hvac.exceptions.InvalidPath:
        raise VaultSecretNotFoundError(
            f"Secret not found: {path}",
            details={"path": path, "mount_point": mp},
        )
    except Exception as exc:
        raise VaultSecretNotFoundError(
            f"Failed to read secret {path}: {exc}",
            details={"path": path},
        ) from exc


def write_secret(
    path: str,
    data: dict[str, Any],
    mount_point: Optional[str] = None,
) -> None:
    """Write a secret to Vault KV v2.

    Args:
        path: Secret path.
        data: Secret key-value data.
        mount_point: KV mount point.
    """
    client = get_vault_client()
    settings = get_settings()
    mp = mount_point or settings.vault.mount_point

    client.secrets.kv.v2.create_or_update_secret(
        path=path,
        secret=data,
        mount_point=mp,
    )
    logger.info("Secret written", path=path)


def delete_secret(path: str, mount_point: Optional[str] = None) -> None:
    """Delete a secret from Vault.

    Args:
        path: Secret path.
        mount_point: KV mount point.
    """
    client = get_vault_client()
    settings = get_settings()
    mp = mount_point or settings.vault.mount_point

    client.secrets.kv.v2.delete_metadata_and_all_versions(
        path=path,
        mount_point=mp,
    )
    logger.info("Secret deleted", path=path)


def list_secrets(path: str = "", mount_point: Optional[str] = None) -> list[str]:
    """List secrets under a path prefix.

    Args:
        path: Path prefix to list.
        mount_point: KV mount point.

    Returns:
        List of secret key names.
    """
    client = get_vault_client()
    settings = get_settings()
    mp = mount_point or settings.vault.mount_point

    try:
        response = client.secrets.kv.v2.list_secrets(
            path=path,
            mount_point=mp,
        )
        keys: list[str] = response["data"]["keys"]
        return keys
    except Exception:
        return []


def close_vault() -> None:
    """Close the Vault client."""
    global _client  # noqa: PLW0603
    _client = None
    logger.info("Vault client closed")


__all__ = [
    "close_vault",
    "delete_secret",
    "get_vault_client",
    "list_secrets",
    "read_secret",
    "write_secret",
]
