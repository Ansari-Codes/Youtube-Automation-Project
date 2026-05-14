from __future__ import annotations


class DeapiError(Exception):
    """Base exception for all SDK errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        body: dict | None = None,  # type: ignore[type-arg]
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body


class AuthenticationError(DeapiError):
    """401 — Invalid or missing API key."""


class AccountSuspendedError(DeapiError):
    """403 — Account suspended."""


class NotFoundError(DeapiError):
    """404 — Resource not found."""


class ValidationError(DeapiError):
    """422 — Request validation failed."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = 422,
        body: dict | None = None,  # type: ignore[type-arg]
        errors: dict[str, list[str]] | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, body=body)
        self.errors = errors or {}


class InsufficientBalanceError(ValidationError):
    """422 with balance error — not enough credits."""


class RateLimitError(DeapiError):
    """429 — Rate limited."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = 429,
        body: dict | None = None,  # type: ignore[type-arg]
        retry_after: float = 0.0,
        limit_type: str = "",
    ) -> None:
        super().__init__(message, status_code=status_code, body=body)
        self.retry_after = retry_after
        self.limit_type = limit_type


class ServerError(DeapiError):
    """5xx — Server-side error."""


class JobTimeoutError(DeapiError):
    """Polling timeout — job didn't complete within max_wait."""


class NetworkError(DeapiError):
    """Network connectivity error."""
