"""Webhook signature verification for DeAPI webhook events."""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

from pydantic import BaseModel

from deapi._exceptions import DeapiError


class WebhookEventData(BaseModel):
    """Data payload from a webhook event."""
    job_request_id: str
    status: str
    previous_status: str | None = None
    job_type: str | None = None
    completed_at: str | None = None
    result_url: str | None = None
    processing_time_ms: int | None = None

    model_config = {"extra": "allow"}


class WebhookEvent(BaseModel):
    """Parsed and verified webhook event."""
    event: str
    delivery_id: str
    timestamp: str
    data: WebhookEventData

    @property
    def type(self) -> str:
        """Alias for event type (e.g. 'job.completed')."""
        return self.event


class InvalidSignatureError(DeapiError):
    """Raised when webhook signature verification fails."""

    def __init__(self, message: str = "Invalid webhook signature") -> None:
        super().__init__(message)


def verify_signature(
    *,
    payload: bytes | str,
    signature: str,
    timestamp: str,
    secret: str,
    tolerance: int = 300,
) -> None:
    """Verify a webhook signature.

    Args:
        payload: Raw request body (bytes or string).
        signature: Value of X-DeAPI-Signature header (e.g. "sha256=abcdef...").
        timestamp: Value of X-DeAPI-Timestamp header (unix timestamp string).
        secret: Your webhook signing secret.
        tolerance: Maximum age in seconds before rejecting (default 300 = 5 min).

    Raises:
        InvalidSignatureError: If signature is invalid or timestamp is too old.
    """
    if tolerance > 0:
        try:
            ts = int(timestamp)
        except (ValueError, TypeError) as exc:
            raise InvalidSignatureError("Invalid timestamp format") from exc

        age = abs(time.time() - ts)
        if age > tolerance:
            raise InvalidSignatureError(
                f"Timestamp too old: {int(age)}s exceeds tolerance of {tolerance}s"
            )

    if isinstance(payload, str):
        payload = payload.encode("utf-8")

    signed_content = f"{timestamp}.".encode("utf-8") + payload
    expected = hmac.new(
        secret.encode("utf-8"),
        signed_content,
        hashlib.sha256,
    ).hexdigest()

    expected_sig = f"sha256={expected}"

    if not hmac.compare_digest(expected_sig, signature):
        raise InvalidSignatureError()


def construct_event(
    *,
    payload: bytes | str,
    signature: str,
    timestamp: str,
    secret: str,
    tolerance: int = 300,
) -> WebhookEvent:
    """Verify signature and parse the webhook payload into a WebhookEvent.

    Args:
        payload: Raw request body.
        signature: Value of X-DeAPI-Signature header.
        timestamp: Value of X-DeAPI-Timestamp header.
        secret: Your webhook signing secret.
        tolerance: Maximum age in seconds (default 300).

    Returns:
        Parsed WebhookEvent with verified signature.

    Raises:
        InvalidSignatureError: If signature is invalid or timestamp is stale.
    """
    verify_signature(
        payload=payload,
        signature=signature,
        timestamp=timestamp,
        secret=secret,
        tolerance=tolerance,
    )

    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")

    body: dict[str, Any] = json.loads(payload)
    return WebhookEvent.model_validate(body)
