from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx

from deapi._config import ClientConfig
from deapi._constants import ENDPOINTS
from deapi._exceptions import (
    AccountSuspendedError,
    AuthenticationError,
    DeapiError,
    InsufficientBalanceError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class BaseClient:
    """Shared logic for sync and async HTTP clients."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config

    def _resolve_endpoint(self, operation: str) -> str:
        """Resolve an operation name to a full URL path."""
        version = self._config.api_version
        version_endpoints = ENDPOINTS.get(version)
        if version_endpoints is None:
            raise DeapiError(f"Unsupported API version: {version}")
        path = version_endpoints.get(operation)
        if path is None:
            raise DeapiError(f"Operation '{operation}' is not available in API {version}")
        return f"{self._config.base_url}{self._config.api_prefix}/{path}"

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._config.api_key}",
            "Accept": "application/json",
            "User-Agent": self._config._user_agent,
        }

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Map HTTP error responses to typed exceptions."""
        if response.is_success:
            return

        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        message = body.get("message", response.text or f"HTTP {status}")

        if status == 401:
            raise AuthenticationError(message, status_code=status, body=body)

        if status == 403:
            raise AccountSuspendedError(message, status_code=status, body=body)

        if status == 404:
            raise NotFoundError(message, status_code=status, body=body)

        if status == 422:
            errors = body.get("errors", {})
            if "balance" in errors:
                raise InsufficientBalanceError(
                    message, status_code=status, body=body, errors=errors
                )
            raise ValidationError(message, status_code=status, body=body, errors=errors)

        if status == 429:
            retry_after = float(response.headers.get("Retry-After", "0"))
            limit_type = response.headers.get("X-RateLimit-Type", "")
            raise RateLimitError(
                message,
                status_code=status,
                body=body,
                retry_after=retry_after,
                limit_type=limit_type,
            )

        if status >= 500:
            raise ServerError(message, status_code=status, body=body)

        raise DeapiError(message, status_code=status, body=body)

    def _should_retry(self, exc: Exception, attempt: int) -> float | None:
        """Determine if a request should be retried and return wait time in seconds.

        Returns None if no retry should happen.
        """
        if attempt >= self._config.max_retries:
            return None

        if isinstance(exc, RateLimitError):
            return max(exc.retry_after, 1.0)

        if isinstance(exc, ServerError):
            return min(2 ** attempt, 8.0)

        if isinstance(exc, NetworkError):
            return min(2 ** attempt, 8.0)

        return None


class SyncHTTPClient(BaseClient):
    """Synchronous HTTP client with retry logic."""

    def __init__(self, config: ClientConfig) -> None:
        super().__init__(config)
        self._http = httpx.Client(
            timeout=config.timeout,
            headers=self._default_headers(),
        )

    def close(self) -> None:
        self._http.close()

    def request(
        self,
        method: str,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: list[tuple[str, tuple[str, bytes, str]]] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        last_exc: Exception | None = None

        for attempt in range(self._config.max_retries + 1):
            try:
                response = self._http.request(
                    method,
                    url,
                    json=json,
                    data=data,
                    files=files,
                    params=params,
                )
                self._raise_for_status(response)
                return response.json()
            except (RateLimitError, ServerError, NetworkError) as exc:
                last_exc = exc
                wait = self._should_retry(exc, attempt)
                if wait is not None:
                    time.sleep(wait)
                    continue
                raise
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_exc = NetworkError(str(exc))
                wait = self._should_retry(last_exc, attempt)
                if wait is not None:
                    time.sleep(wait)
                    continue
                raise last_exc from exc

        raise last_exc  # type: ignore[misc]

    def get(self, url: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", url, params=params)

    def post(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: list[tuple[str, tuple[str, bytes, str]]] | None = None,
    ) -> Any:
        return self.request("POST", url, json=json, data=data, files=files)


class AsyncHTTPClient(BaseClient):
    """Asynchronous HTTP client with retry logic."""

    def __init__(self, config: ClientConfig) -> None:
        super().__init__(config)
        self._http = httpx.AsyncClient(
            timeout=config.timeout,
            headers=self._default_headers(),
        )

    async def close(self) -> None:
        await self._http.aclose()

    async def request(
        self,
        method: str,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: list[tuple[str, tuple[str, bytes, str]]] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        last_exc: Exception | None = None

        for attempt in range(self._config.max_retries + 1):
            try:
                response = await self._http.request(
                    method,
                    url,
                    json=json,
                    data=data,
                    files=files,
                    params=params,
                )
                self._raise_for_status(response)
                return response.json()
            except (RateLimitError, ServerError, NetworkError) as exc:
                last_exc = exc
                wait = self._should_retry(exc, attempt)
                if wait is not None:
                    await asyncio.sleep(wait)
                    continue
                raise
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_exc = NetworkError(str(exc))
                wait = self._should_retry(last_exc, attempt)
                if wait is not None:
                    await asyncio.sleep(wait)
                    continue
                raise last_exc from exc

        raise last_exc  # type: ignore[misc]

    async def get(self, url: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", url, params=params)

    async def post(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: list[tuple[str, tuple[str, bytes, str]]] | None = None,
    ) -> Any:
        return await self.request("POST", url, json=json, data=data, files=files)
