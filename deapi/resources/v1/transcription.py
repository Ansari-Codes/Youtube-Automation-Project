from __future__ import annotations

from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput, normalize_file
from deapi._polling import AsyncJob, Job
from deapi.types.common import PriceResult


class Transcription:
    """Sync transcription resource (v1).

    Provides the unified ``create()`` endpoint (preferred) and legacy
    per-type methods for backward compatibility.
    """

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    # --- Unified endpoint ---

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
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if return_result_in_response is not None:
                data["return_result_in_response"] = "1" if return_result_in_response else "0"
            if webhook_url is not None:
                data["webhook_url"] = webhook_url
            normalized = normalize_file(source_file, "source_file")
            files = [("source_file", normalized)]
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
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            normalized = normalize_file(source_file, "source_file")
            files = [("source_file", normalized)]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
            if source_url is not None:
                payload["source_url"] = source_url
            if duration_seconds is not None:
                payload["duration_seconds"] = duration_seconds
            resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    # --- Legacy: video URL transcription ---

    def from_video_url(
        self,
        *,
        video_url: str,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a video URL transcription job (vid2txt)."""
        url = self._client._resolve_endpoint("vid2txt")
        payload = _build_url_transcription_payload(
            url_field="video_url", url_value=video_url, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def from_video_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for video URL transcription."""
        url = self._client._resolve_endpoint("vid2txt_price")
        payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
        if video_url is not None:
            payload["video_url"] = video_url
        if duration_seconds is not None:
            payload["duration_seconds"] = duration_seconds
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    # --- Legacy: audio URL transcription (Twitter Spaces) ---

    def from_audio_url(
        self,
        *,
        audio_url: str,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an audio URL transcription job (aud2txt — Twitter Spaces only)."""
        url = self._client._resolve_endpoint("aud2txt")
        payload = _build_url_transcription_payload(
            url_field="audio_url", url_value=audio_url, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def from_audio_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for audio URL transcription."""
        url = self._client._resolve_endpoint("aud2txt_price")
        payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
        if audio_url is not None:
            payload["audio_url"] = audio_url
        if duration_seconds is not None:
            payload["duration_seconds"] = duration_seconds
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    # --- Legacy: audio file upload transcription ---

    def from_audio_file(
        self,
        *,
        audio: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an audio file transcription job (audiofile2txt)."""
        url = self._client._resolve_endpoint("audiofile2txt")
        data, files = _build_file_transcription_multipart(
            file_field="audio", file=audio, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def from_audio_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for audio file transcription."""
        url = self._client._resolve_endpoint("audiofile2txt_price")
        if audio is not None:
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            normalized = normalize_file(audio, "audio")
            files = [("audio", normalized)]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
            if duration_seconds is not None:
                payload["duration_seconds"] = duration_seconds
            resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    # --- Legacy: video file upload transcription ---

    def from_video_file(
        self,
        *,
        video: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a video file transcription job (videofile2txt)."""
        url = self._client._resolve_endpoint("videofile2txt")
        data, files = _build_file_transcription_multipart(
            file_field="video", file=video, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def from_video_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for video file transcription."""
        url = self._client._resolve_endpoint("videofile2txt_price")
        if video is not None:
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            normalized = normalize_file(video, "video")
            files = [("video", normalized)]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
            if duration_seconds is not None:
                payload["duration_seconds"] = duration_seconds
            resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


class AsyncTranscription:
    """Async transcription resource (v1)."""

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
        """Submit a transcription job via the unified endpoint."""
        if source_url is not None and source_file is not None:
            raise ValueError("Provide either 'source_url' or 'source_file', not both.")
        if source_url is None and source_file is None:
            raise ValueError("Either 'source_url' or 'source_file' is required.")

        url = self._client._resolve_endpoint("transcribe")

        if source_file is not None:
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if return_result_in_response is not None:
                data["return_result_in_response"] = "1" if return_result_in_response else "0"
            if webhook_url is not None:
                data["webhook_url"] = webhook_url
            normalized = normalize_file(source_file, "source_file")
            files = [("source_file", normalized)]
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
        """Calculate price for unified transcription."""
        url = self._client._resolve_endpoint("transcribe_price")
        if source_file is not None:
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            normalized = normalize_file(source_file, "source_file")
            files = [("source_file", normalized)]
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
        """Submit a video URL transcription job (vid2txt)."""
        url = self._client._resolve_endpoint("vid2txt")
        payload = _build_url_transcription_payload(
            url_field="video_url", url_value=video_url, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def from_video_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for video URL transcription."""
        url = self._client._resolve_endpoint("vid2txt_price")
        payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
        if video_url is not None:
            payload["video_url"] = video_url
        if duration_seconds is not None:
            payload["duration_seconds"] = duration_seconds
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def from_audio_url(
        self,
        *,
        audio_url: str,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an audio URL transcription job (aud2txt — Twitter Spaces only)."""
        url = self._client._resolve_endpoint("aud2txt")
        payload = _build_url_transcription_payload(
            url_field="audio_url", url_value=audio_url, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def from_audio_url_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio_url: str | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for audio URL transcription."""
        url = self._client._resolve_endpoint("aud2txt_price")
        payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
        if audio_url is not None:
            payload["audio_url"] = audio_url
        if duration_seconds is not None:
            payload["duration_seconds"] = duration_seconds
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def from_audio_file(
        self,
        *,
        audio: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an audio file transcription job (audiofile2txt)."""
        url = self._client._resolve_endpoint("audiofile2txt")
        data, files = _build_file_transcription_multipart(
            file_field="audio", file=audio, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def from_audio_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        audio: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for audio file transcription."""
        url = self._client._resolve_endpoint("audiofile2txt_price")
        if audio is not None:
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            normalized = normalize_file(audio, "audio")
            files = [("audio", normalized)]
            resp = await self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
            if duration_seconds is not None:
                payload["duration_seconds"] = duration_seconds
            resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def from_video_file(
        self,
        *,
        video: FileInput,
        include_ts: bool,
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a video file transcription job (videofile2txt)."""
        url = self._client._resolve_endpoint("videofile2txt")
        data, files = _build_file_transcription_multipart(
            file_field="video", file=video, include_ts=include_ts,
            model=model, return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def from_video_file_price(
        self,
        *,
        include_ts: bool,
        model: str,
        video: FileInput | None = None,
        duration_seconds: float | None = None,
    ) -> PriceResult:
        """Calculate price for video file transcription."""
        url = self._client._resolve_endpoint("videofile2txt_price")
        if video is not None:
            data: dict[str, Any] = {"include_ts": "1" if include_ts else "0", "model": model}
            if duration_seconds is not None:
                data["duration_seconds"] = duration_seconds
            normalized = normalize_file(video, "video")
            files = [("video", normalized)]
            resp = await self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"include_ts": include_ts, "model": model}
            if duration_seconds is not None:
                payload["duration_seconds"] = duration_seconds
            resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


# --- Private helpers ---

def _build_url_transcription_payload(
    *,
    url_field: str,
    url_value: str,
    include_ts: bool,
    model: str,
    return_result_in_response: bool | None = None,
    webhook_url: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        url_field: url_value, "include_ts": include_ts, "model": model,
    }
    if return_result_in_response is not None:
        payload["return_result_in_response"] = return_result_in_response
    if webhook_url is not None:
        payload["webhook_url"] = webhook_url
    return payload


def _build_file_transcription_multipart(
    *,
    file_field: str,
    file: FileInput,
    include_ts: bool,
    model: str,
    return_result_in_response: bool | None = None,
    webhook_url: str | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    data: dict[str, Any] = {
        "include_ts": "1" if include_ts else "0",
        "model": model,
    }
    if return_result_in_response is not None:
        data["return_result_in_response"] = "1" if return_result_in_response else "0"
    if webhook_url is not None:
        data["webhook_url"] = webhook_url

    normalized = normalize_file(file, file_field)
    files = [(file_field, normalized)]
    return data, files
