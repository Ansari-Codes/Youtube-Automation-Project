"""DeAPI Python SDK — Official client for the DeAPI distributed AI inference platform."""

from __future__ import annotations

from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._config import ClientConfig
from deapi._exceptions import (
    AccountSuspendedError,
    AuthenticationError,
    DeapiError,
    InsufficientBalanceError,
    JobTimeoutError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from deapi._polling import AsyncJob, Job
from deapi._types import InferenceType, JobStatus
from deapi._version import __version__
from deapi.types.common import Balance, JobResult, JobSubmission, PriceResult
from deapi.webhook import InvalidSignatureError, WebhookEvent, WebhookEventData, construct_event, verify_signature


def _attach_v1_resources_sync(client: DeapiClient) -> None:
    from deapi.resources.v1 import Audio, Embeddings, Images, Models, OCR, Prompts, Transcription, Video
    client.images = Images(client._http_client)
    client.models = Models(client._http_client)
    client.audio = Audio(client._http_client)
    client.transcription = Transcription(client._http_client)
    client.video = Video(client._http_client)
    client.embeddings = Embeddings(client._http_client)
    client.prompts = Prompts(client._http_client)
    client.ocr = OCR(client._http_client)


def _attach_v1_resources_async(client: AsyncDeapiClient) -> None:
    from deapi.resources.v1 import (
        AsyncAudio, AsyncEmbeddings, AsyncImages, AsyncModels,
        AsyncOCR, AsyncPrompts, AsyncTranscription, AsyncVideo,
    )
    client.images = AsyncImages(client._http_client)
    client.models = AsyncModels(client._http_client)
    client.audio = AsyncAudio(client._http_client)
    client.transcription = AsyncTranscription(client._http_client)
    client.video = AsyncVideo(client._http_client)
    client.embeddings = AsyncEmbeddings(client._http_client)
    client.prompts = AsyncPrompts(client._http_client)
    client.ocr = AsyncOCR(client._http_client)


def _attach_v2_resources_sync(client: DeapiClient) -> None:
    from deapi.resources.v2 import Audio, Embeddings, Images, Models, OCR, Prompts, Transcription, Video
    client.images = Images(client._http_client)
    client.models = Models(client._http_client)
    client.audio = Audio(client._http_client)
    client.transcription = Transcription(client._http_client)
    client.video = Video(client._http_client)
    client.embeddings = Embeddings(client._http_client)
    client.prompts = Prompts(client._http_client)
    client.ocr = OCR(client._http_client)


def _attach_v2_resources_async(client: AsyncDeapiClient) -> None:
    from deapi.resources.v2 import (
        AsyncAudio, AsyncEmbeddings, AsyncImages, AsyncModels,
        AsyncOCR, AsyncPrompts, AsyncTranscription, AsyncVideo,
    )
    client.images = AsyncImages(client._http_client)
    client.models = AsyncModels(client._http_client)
    client.audio = AsyncAudio(client._http_client)
    client.transcription = AsyncTranscription(client._http_client)
    client.video = AsyncVideo(client._http_client)
    client.embeddings = AsyncEmbeddings(client._http_client)
    client.prompts = AsyncPrompts(client._http_client)
    client.ocr = AsyncOCR(client._http_client)


_RESOURCE_LOADERS: dict[str, dict[str, Any]] = {
    "v1": {
        "sync": _attach_v1_resources_sync,
        "async": _attach_v1_resources_async,
    },
    "v2": {
        "sync": _attach_v2_resources_sync,
        "async": _attach_v2_resources_async,
    },
}


class DeapiClient:
    """Synchronous DeAPI client.

    Usage::

        client = DeapiClient(api_key="sk-...")
        job = client.images.generate(prompt="a cat in space", model="sdxl", width=1024, height=1024, seed=42)
        result = job.wait()
        print(result.result_url)

    Or as a context manager::

        with DeapiClient(api_key="sk-...") as client:
            ...
    """

    images: Any
    models: Any
    audio: Any
    transcription: Any
    video: Any
    embeddings: Any
    prompts: Any
    ocr: Any

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        api_version: str | None = None,
    ) -> None:
        self._config = ClientConfig.from_env(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            api_version=api_version,
        )
        self._http_client = SyncHTTPClient(self._config)
        self._attach_resources()

    def _attach_resources(self) -> None:
        version = self._config.api_version
        loader = _RESOURCE_LOADERS.get(version)
        if loader is None:
            raise DeapiError(f"Unsupported API version: {version}")
        loader["sync"](self)

    def balance(self) -> Balance:
        """Get current account balance."""
        url = self._http_client._resolve_endpoint("balance")
        resp = self._http_client.get(url)
        return Balance.model_validate(resp.get("data", resp))

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http_client.close()

    def __enter__(self) -> DeapiClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncDeapiClient:
    """Asynchronous DeAPI client.

    Usage::

        async with AsyncDeapiClient(api_key="sk-...") as client:
            job = await client.images.generate(prompt="a cat in space", model="sdxl", width=1024, height=1024, seed=42)
            result = await job.wait()
            print(result.result_url)
    """

    images: Any
    models: Any
    audio: Any
    transcription: Any
    video: Any
    embeddings: Any
    prompts: Any
    ocr: Any

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        api_version: str | None = None,
    ) -> None:
        self._config = ClientConfig.from_env(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            api_version=api_version,
        )
        self._http_client = AsyncHTTPClient(self._config)
        self._attach_resources()

    def _attach_resources(self) -> None:
        version = self._config.api_version
        loader = _RESOURCE_LOADERS.get(version)
        if loader is None:
            raise DeapiError(f"Unsupported API version: {version}")
        loader["async"](self)

    async def balance(self) -> Balance:
        """Get current account balance."""
        url = self._http_client._resolve_endpoint("balance")
        resp = await self._http_client.get(url)
        return Balance.model_validate(resp.get("data", resp))

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http_client.close()

    async def __aenter__(self) -> AsyncDeapiClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


__all__ = [
    # Clients
    "DeapiClient",
    "AsyncDeapiClient",
    # Jobs
    "Job",
    "AsyncJob",
    # Types
    "Balance",
    "InferenceType",
    "JobResult",
    "JobStatus",
    "JobSubmission",
    "PriceResult",
    # Exceptions
    "AccountSuspendedError",
    "AuthenticationError",
    "NetworkError",
    "DeapiError",
    "InsufficientBalanceError",
    "JobTimeoutError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    # Webhook
    "InvalidSignatureError",
    "WebhookEvent",
    "WebhookEventData",
    "construct_event",
    "verify_signature",
    # Version
    "__version__",
]
