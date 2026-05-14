from __future__ import annotations

from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput, normalize_file
from deapi._polling import AsyncJob, Job
from deapi.types.common import PriceResult


class Audio:
    """Sync audio resource — TTS and music generation (v1)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def synthesize(
        self,
        *,
        text: str,
        model: str,
        lang: str,
        format: str,
        speed: float,
        sample_rate: float,
        mode: str | None = None,
        voice: str | None = None,
        ref_audio: FileInput | None = None,
        ref_text: str | None = None,
        instruct: str | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a text-to-audio (TTS) job."""
        url = self._client._resolve_endpoint("txt2audio")
        data, files = _build_tts_multipart(
            text=text, model=model, lang=lang, format=format, speed=speed,
            sample_rate=sample_rate, mode=mode, voice=voice, ref_audio=ref_audio,
            ref_text=ref_text, instruct=instruct, webhook_url=webhook_url,
        )
        if files:
            resp = self._client.post(url, data=data, files=files)
        else:
            resp = self._client.post(url, json=data)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def synthesize_price(
        self,
        *,
        model: str,
        lang: str,
        format: str,
        speed: float,
        sample_rate: float,
        text: str | None = None,
        count_text: int | None = None,
        mode: str | None = None,
        voice: str | None = None,
        instruct: str | None = None,
    ) -> PriceResult:
        """Calculate price for TTS."""
        url = self._client._resolve_endpoint("txt2audio_price")
        payload: dict[str, Any] = {
            "model": model, "lang": lang, "format": format,
            "speed": speed, "sample_rate": sample_rate,
        }
        if text is not None:
            payload["text"] = text
        if count_text is not None:
            payload["count_text"] = count_text
        if mode is not None:
            payload["mode"] = mode
        if voice is not None:
            payload["voice"] = voice
        if instruct is not None:
            payload["instruct"] = instruct
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def compose(
        self,
        *,
        caption: str,
        model: str,
        duration: float,
        inference_steps: int,
        guidance_scale: float,
        seed: int,
        format: str,
        lyrics: str | None = None,
        bpm: int | None = None,
        keyscale: str | None = None,
        timesignature: int | None = None,
        vocal_language: str | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a text-to-music generation job."""
        url = self._client._resolve_endpoint("txt2music")
        payload = _build_music_payload(
            caption=caption, model=model, duration=duration,
            inference_steps=inference_steps, guidance_scale=guidance_scale,
            seed=seed, format=format, lyrics=lyrics, bpm=bpm,
            keyscale=keyscale, timesignature=timesignature,
            vocal_language=vocal_language, webhook_url=webhook_url,
        )
        resp = self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def compose_price(
        self,
        *,
        model: str,
        duration: float,
        inference_steps: int,
    ) -> PriceResult:
        """Calculate price for music generation."""
        url = self._client._resolve_endpoint("txt2music_price")
        payload: dict[str, Any] = {
            "model": model, "duration": duration, "inference_steps": inference_steps,
        }
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


class AsyncAudio:
    """Async audio resource — TTS and music generation (v1)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def synthesize(
        self,
        *,
        text: str,
        model: str,
        lang: str,
        format: str,
        speed: float,
        sample_rate: float,
        mode: str | None = None,
        voice: str | None = None,
        ref_audio: FileInput | None = None,
        ref_text: str | None = None,
        instruct: str | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a text-to-audio (TTS) job."""
        url = self._client._resolve_endpoint("txt2audio")
        data, files = _build_tts_multipart(
            text=text, model=model, lang=lang, format=format, speed=speed,
            sample_rate=sample_rate, mode=mode, voice=voice, ref_audio=ref_audio,
            ref_text=ref_text, instruct=instruct, webhook_url=webhook_url,
        )
        if files:
            resp = await self._client.post(url, data=data, files=files)
        else:
            resp = await self._client.post(url, json=data)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def synthesize_price(
        self,
        *,
        model: str,
        lang: str,
        format: str,
        speed: float,
        sample_rate: float,
        text: str | None = None,
        count_text: int | None = None,
        mode: str | None = None,
        voice: str | None = None,
        instruct: str | None = None,
    ) -> PriceResult:
        """Calculate price for TTS."""
        url = self._client._resolve_endpoint("txt2audio_price")
        payload: dict[str, Any] = {
            "model": model, "lang": lang, "format": format,
            "speed": speed, "sample_rate": sample_rate,
        }
        if text is not None:
            payload["text"] = text
        if count_text is not None:
            payload["count_text"] = count_text
        if mode is not None:
            payload["mode"] = mode
        if voice is not None:
            payload["voice"] = voice
        if instruct is not None:
            payload["instruct"] = instruct
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def compose(
        self,
        *,
        caption: str,
        model: str,
        duration: float,
        inference_steps: int,
        guidance_scale: float,
        seed: int,
        format: str,
        lyrics: str | None = None,
        bpm: int | None = None,
        keyscale: str | None = None,
        timesignature: int | None = None,
        vocal_language: str | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a text-to-music generation job."""
        url = self._client._resolve_endpoint("txt2music")
        payload = _build_music_payload(
            caption=caption, model=model, duration=duration,
            inference_steps=inference_steps, guidance_scale=guidance_scale,
            seed=seed, format=format, lyrics=lyrics, bpm=bpm,
            keyscale=keyscale, timesignature=timesignature,
            vocal_language=vocal_language, webhook_url=webhook_url,
        )
        resp = await self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def compose_price(
        self,
        *,
        model: str,
        duration: float,
        inference_steps: int,
    ) -> PriceResult:
        """Calculate price for music generation."""
        url = self._client._resolve_endpoint("txt2music_price")
        payload: dict[str, Any] = {
            "model": model, "duration": duration, "inference_steps": inference_steps,
        }
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


# --- Private helpers ---

def _build_tts_multipart(
    *,
    text: str,
    model: str,
    lang: str,
    format: str,
    speed: float,
    sample_rate: float,
    mode: str | None = None,
    voice: str | None = None,
    ref_audio: FileInput | None = None,
    ref_text: str | None = None,
    instruct: str | None = None,
    webhook_url: str | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    """Build form data for TTS. Returns (data_dict, file_tuples).

    When ref_audio is provided, the request must be multipart/form-data.
    Otherwise, the caller should send as JSON.
    """
    data: dict[str, Any] = {
        "text": text, "model": model, "lang": lang,
        "format": format, "speed": speed, "sample_rate": sample_rate,
    }
    if mode is not None:
        data["mode"] = mode
    if voice is not None:
        data["voice"] = voice
    if ref_text is not None:
        data["ref_text"] = ref_text
    if instruct is not None:
        data["instruct"] = instruct
    if webhook_url is not None:
        data["webhook_url"] = webhook_url

    file_tuples: list[tuple[str, tuple[str, bytes, str]]] = []
    if ref_audio is not None:
        normalized = normalize_file(ref_audio, "ref_audio")
        file_tuples.append(("ref_audio", normalized))

    return data, file_tuples


def _build_music_payload(
    *,
    caption: str,
    model: str,
    duration: float,
    inference_steps: int,
    guidance_scale: float,
    seed: int,
    format: str,
    lyrics: str | None = None,
    bpm: int | None = None,
    keyscale: str | None = None,
    timesignature: int | None = None,
    vocal_language: str | None = None,
    webhook_url: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "caption": caption, "model": model, "duration": duration,
        "inference_steps": inference_steps, "guidance_scale": guidance_scale,
        "seed": seed, "format": format,
    }
    if lyrics is not None:
        payload["lyrics"] = lyrics
    if bpm is not None:
        payload["bpm"] = bpm
    if keyscale is not None:
        payload["keyscale"] = keyscale
    if timesignature is not None:
        payload["timesignature"] = timesignature
    if vocal_language is not None:
        payload["vocal_language"] = vocal_language
    if webhook_url is not None:
        payload["webhook_url"] = webhook_url
    return payload
