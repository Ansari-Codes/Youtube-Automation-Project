from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

from deapi._exceptions import JobTimeoutError
from deapi._types import JobStatus
from deapi.types.common import JobResult

if TYPE_CHECKING:
    from deapi._client import AsyncHTTPClient, SyncHTTPClient


class Job:
    """A submitted job that can be polled for status."""

    def __init__(self, request_id: str, client: SyncHTTPClient, status_url: str) -> None:
        self.request_id = request_id
        self._client = client
        self._status_url = status_url

    def status(self) -> JobResult:
        """Poll once and return current status."""
        url = f"{self._status_url}/{self.request_id}"
        resp = self._client.get(url)
        return JobResult.model_validate(resp.get("data", resp))

    def wait(
        self,
        *,
        poll_interval: float = 1.0,
        max_wait: float = 300.0,
        backoff_factor: float = 1.5,
        max_interval: float = 10.0,
    ) -> JobResult:
        """Poll until done/error with exponential backoff.

        Raises JobTimeoutError if max_wait is exceeded.
        """
        deadline = time.monotonic() + max_wait
        interval = poll_interval

        while time.monotonic() < deadline:
            result = self.status()
            if result.status == JobStatus.DONE or result.status == JobStatus.ERROR:
                return result

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(interval, remaining))
            interval = min(interval * backoff_factor, max_interval)

        raise JobTimeoutError(
            f"Job {self.request_id} did not complete within {max_wait}s"
        )

    def is_done(self) -> bool:
        """Check if the job is done. Note: this makes an HTTP request each time."""
        return self.status().status == JobStatus.DONE

    def is_error(self) -> bool:
        """Check if the job errored. Note: this makes an HTTP request each time."""
        return self.status().status == JobStatus.ERROR

    def __repr__(self) -> str:
        return f"Job(request_id={self.request_id!r})"


class AsyncJob:
    """Async variant of Job."""

    def __init__(self, request_id: str, client: AsyncHTTPClient, status_url: str) -> None:
        self.request_id = request_id
        self._client = client
        self._status_url = status_url

    async def status(self) -> JobResult:
        """Poll once and return current status."""
        url = f"{self._status_url}/{self.request_id}"
        resp = await self._client.get(url)
        return JobResult.model_validate(resp.get("data", resp))

    async def wait(
        self,
        *,
        poll_interval: float = 1.0,
        max_wait: float = 300.0,
        backoff_factor: float = 1.5,
        max_interval: float = 10.0,
    ) -> JobResult:
        """Poll until done/error with exponential backoff."""
        deadline = time.monotonic() + max_wait
        interval = poll_interval

        while time.monotonic() < deadline:
            result = await self.status()
            if result.status == JobStatus.DONE or result.status == JobStatus.ERROR:
                return result

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            await asyncio.sleep(min(interval, remaining))
            interval = min(interval * backoff_factor, max_interval)

        raise JobTimeoutError(
            f"Job {self.request_id} did not complete within {max_wait}s"
        )

    async def is_done(self) -> bool:
        """Check if the job is done. Note: this makes an HTTP request each time."""
        return (await self.status()).status == JobStatus.DONE

    async def is_error(self) -> bool:
        """Check if the job errored. Note: this makes an HTTP request each time."""
        return (await self.status()).status == JobStatus.ERROR

    def __repr__(self) -> str:
        return f"AsyncJob(request_id={self.request_id!r})"
