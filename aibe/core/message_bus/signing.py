"""HMAC-SHA256 message signing and verification.

Every message published to the bus is signed to prevent tampering.
"""

from __future__ import annotations

import hashlib
import hmac

from aibe.core.config import get_settings
from aibe.core.message_bus.models import MessageBase


def _get_signing_key() -> bytes:
    """Get the HMAC signing key from settings."""
    settings = get_settings()
    return settings.secret_key.get_secret_value().encode("utf-8")


def sign_message(message: MessageBase) -> str:
    """Compute HMAC-SHA256 signature for a message.

    Signs the message_id + source_agent + timestamp to prevent replay.

    Args:
        message: The message to sign.

    Returns:
        Hex-encoded HMAC signature string.
    """
    key = _get_signing_key()
    payload = f"{message.message_id}:{message.source_agent}:{message.timestamp.isoformat()}"
    return hmac.new(key, payload.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_message(message: MessageBase) -> bool:
    """Verify HMAC-SHA256 signature on a received message.

    Args:
        message: The message to verify.

    Returns:
        True if signature is valid, False otherwise.
    """
    if not message.signature:
        return False
    expected = sign_message(message)
    return hmac.compare_digest(message.signature, expected)


__all__ = ["sign_message", "verify_message"]
