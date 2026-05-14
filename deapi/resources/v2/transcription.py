from __future__ import annotations

import warnings
from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput
from deapi._polling import AsyncJob, Job
from deapi.types.common import PriceResult


_LEGACY_DEPRECATION = (
    "v2 has a unified transcription endpoint — call `transcription.create(...)` "
    "with `source_url` or `source_file`. Legacy method '{name}' is deprecated and "
    "will route through the unified endpoint automatically."
)


class Transcription:
    """Sync transcription resource (v2).

    The v2 API has a single unified transcription endpoint. Legacy v1-style
    methods (``from_video_url``, ``from_audio_url``, ``from_audio_file``,
    ``from_video_file``) emit a ``DeprecationWarning`` and transparently
    route to ``create()``.
    """

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def create(
        self,
        *,
        include_ts: bool,
        model: str,
        source_url: str | None = None,
        source_file: FileInput | None = None,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a transcription job via the unified endpoint.

        Provide either ``source_url`` (video/audio URL) or ``source_file``
        (audio/video file upload), not both.
        """
        if source_url is not None and source_file is not None:
            raise ValueError("Provide either 'source_url' or 'source_file', not both.")
        if source_url is None and source_file is None:
            raise ValueError("Either 'source_url' or 'source_file' is required.")

        url = self._client._resolve_endpoint("transcribe")

        if source_file is not None:
            from deapi._files import normalize_file
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if return_result_in_response is not None:
                data["return_result_in_response"] = "1" if return_result_in_response else "0"
            if webhook_url is not None:
                data["webhook_url"] = webhook_url
            files = [("source_file", normalize_file(source_file, "source_file"))]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {
                "source_url": source_url, "include_ts": include_ts, "model": model,
            }
            if return_result_in_response is not None:
                payload["return_result_in_response"] = return_result_in_response
            if webhook_url is not None:
                payload["webhook_url"] = webhook_url
            resp = self._client.post(url, json=payload)

        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def create_price(
        self,
        *,
        include_ts: bool,
        model: str,
        source_url: str | None = None,
        source_file: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for unified transcription."""
        url = self._client._resolve_endpoint("transcribe_price")
        if source_file is not None:
            from deapi._files import normalize_file
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            files = [("source_file", normalize_file(source_file, "source_file"))]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
            if source_url is not None:
                payload["source_url"] = source_url
            if duration_seconds is not None:
                payload["duration_seconds"] = duration_seconds
            resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    # --- Legacy methods (deprecated, route to create) ---

    def from_video_url(
        self,
        *,
        video_url: str,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_url"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create(
            source_url=video_url,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    def from_video_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_url_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create_price(
            include_ts=include_ts,
            model=model,
            source_url=video_url,
            duration_seconds=duration_seconds,
        )

    def from_audio_url(
        self,
        *,
        audio_url: str,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_url"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create(
            source_url=audio_url,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    def from_audio_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_url_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create_price(
            include_ts=include_ts,
            model=model,
            source_url=audio_url,
            duration_seconds=duration_seconds,
        )

    def from_audio_file(
        self,
        *,
        audio: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_file"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create(
            source_file=audio,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    def from_audio_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_file_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create_price(
            include_ts=include_ts,
            model=model,
            source_file=audio,
            duration_seconds=duration_seconds,
        )

    def from_video_file(
        self,
        *,
        video: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_file"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create(
            source_file=video,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    def from_video_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_file_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create_price(
            include_ts=include_ts,
            model=model,
            source_file=video,
            duration_seconds=duration_seconds,
        )


class AsyncTranscription:
    """Async transcription resource (v2)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        include_ts: bool,
        model: str,
        source_url: str | None = None,
        source_file: FileInput | None = None,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        if source_url is not None and source_file is not None:
            raise ValueError("Provide either 'source_url' or 'source_file', not both.")
        if source_url is None and source_file is None:
            raise ValueError("Either 'source_url' or 'source_file' is required.")

        url = self._client._resolve_endpoint("transcribe")

        if source_file is not None:
            from deapi._files import normalize_file
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if return_result_in_response is not None:
                data["return_result_in_response"] = "1" if return_result_in_response else "0"
            if webhook_url is not None:
                data["webhook_url"] = webhook_url
            files = [("source_file", normalize_file(source_file, "source_file"))]
            resp = await self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {
                "source_url": source_url, "include_ts": include_ts, "model": model,
            }
            if return_result_in_response is not None:
                payload["return_result_in_response"] = return_result_in_response
            if webhook_url is not None:
                payload["webhook_url"] = webhook_url
            resp = await self._client.post(url, json=payload)

        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def create_price(
        self,
        *,
        include_ts: bool,
        model: str,
        source_url: str | None = None,
        source_file: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        url = self._client._resolve_endpoint("transcribe_price")
        if source_file is not None:
            from deapi._files import normalize_file
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            files = [("source_file", normalize_file(source_file, "source_file"))]
            resp = await self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
            if source_url is not None:
                payload["source_url"] = source_url
            if duration_seconds is not None:
                payload["duration_seconds"] = duration_seconds
            resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def from_video_url(
        self,
        *,
        video_url: str,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_url"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create(
            source_url=video_url,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    async def from_video_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_url_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create_price(
            include_ts=include_ts,
            model=model,
            source_url=video_url,
            duration_seconds=duration_seconds,
        )

    async def from_audio_url(
        self,
        *,
        audio_url: str,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_url"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create(
            source_url=audio_url,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    async def from_audio_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_url_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create_price(
            include_ts=include_ts,
            model=model,
            source_url=audio_url,
            duration_seconds=duration_seconds,
        )

    async def from_audio_file(
        self,
        *,
        audio: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_file"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create(
            source_file=audio,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    async def from_audio_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_audio_file_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create_price(
            include_ts=include_ts,
            model=model,
            source_file=audio,
            duration_seconds=duration_seconds,
        )

    async def from_video_file(
        self,
        *,
        video: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_file"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create(
            source_file=video,
            include_ts=include_ts,
            model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )

    async def from_video_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="from_video_file_price"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.create_price(
            include_ts=include_ts,
            model=model,
            source_file=video,
            duration_seconds=duration_seconds,
        )
