from __future__ import annotations

from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput, normalize_file
from deapi._polling import AsyncJob, Job
from deapi.types.common import PriceResult


class Video:
    """Sync video resource — generation, animation, audio-to-video, replace, upscale, and background removal (v1)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def generate(
        self,
        *,
        prompt: str,
        model: str,
        width: int,
        height: int,
        steps: int,
        seed: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        guidance: float | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a text-to-video generation job."""
        url = self._client._resolve_endpoint("txt2video")
        payload = _build_txt2video_payload(
            prompt=prompt, model=model, width=width, height=height,
            steps=steps, seed=seed, frames=frames, fps=fps,
            negative_prompt=negative_prompt, guidance=guidance,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def generate_price(
        self,
        *,
        prompt: str,
        model: str,
        width: int,
        height: int,
        steps: int,
        seed: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        guidance: float | None = None,
    ) -> PriceResult:
        """Calculate price for text-to-video generation."""
        url = self._client._resolve_endpoint("txt2video_price")
        payload = _build_txt2video_payload(
            prompt=prompt, model=model, width=width, height=height,
            steps=steps, seed=seed, frames=frames, fps=fps,
            negative_prompt=negative_prompt, guidance=guidance,
        )
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def animate(
        self,
        *,
        prompt: str,
        model: str,
        first_frame_image: FileInput,
        seed: int,
        width: int,
        height: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        last_frame_image: FileInput | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an image-to-video animation job."""
        url = self._client._resolve_endpoint("img2video")
        data, files = _build_img2video_multipart(
            prompt=prompt, model=model, first_frame_image=first_frame_image,
            seed=seed, width=width, height=height, frames=frames, fps=fps,
            negative_prompt=negative_prompt, last_frame_image=last_frame_image,
            guidance=guidance, steps=steps, webhook_url=webhook_url,
        )
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def animate_price(
        self,
        *,
        model: str,
        width: int,
        height: int,
        frames: int,
        fps: int,
        steps: int | None = None,
        guidance: float | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-video animation."""
        url = self._client._resolve_endpoint("img2video_price")
        payload: dict[str, Any] = {
            "model": model, "width": width, "height": height,
            "frames": frames, "fps": fps,
        }
        if steps is not None:
            payload["steps"] = steps
        if guidance is not None:
            payload["guidance"] = guidance
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def generate_from_audio(
        self,
        *,
        prompt: str,
        audio: FileInput,
        model: str,
        width: int,
        height: int,
        seed: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        first_frame_image: FileInput | None = None,
        last_frame_image: FileInput | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an audio-to-video generation job."""
        url = self._client._resolve_endpoint("aud2video")
        data, files = _build_aud2video_multipart(
            prompt=prompt, audio=audio, model=model, width=width, height=height,
            seed=seed, frames=frames, fps=fps, negative_prompt=negative_prompt,
            first_frame_image=first_frame_image, last_frame_image=last_frame_image,
            guidance=guidance, steps=steps, webhook_url=webhook_url,
        )
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def generate_from_audio_price(
        self,
        *,
        model: str,
        width: int,
        height: int,
        frames: int,
        fps: int,
        guidance: float | None = None,
        steps: int | None = None,
    ) -> PriceResult:
        """Calculate price for audio-to-video generation."""
        url = self._client._resolve_endpoint("aud2video_price")
        payload: dict[str, Any] = {
            "model": model, "width": width, "height": height,
            "frames": frames, "fps": fps,
        }
        if guidance is not None:
            payload["guidance"] = guidance
        if steps is not None:
            payload["steps"] = steps
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def replace(
        self,
        *,
        video: FileInput,
        ref_image: FileInput,
        model: str,
        prompt: str | None = None,
        width: int | None = None,
        height: int | None = None,
        steps: int | None = None,
        seed: int | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a video replace job."""
        url = self._client._resolve_endpoint("vid_replace")
        data, files = _build_vid_replace_multipart(
            video=video, ref_image=ref_image, model=model, prompt=prompt,
            width=width, height=height, steps=steps, seed=seed,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def replace_price(
        self,
        *,
        model: str,
        video: FileInput | None = None,
        duration: float | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for video replace.

        Provide either ``video`` (file) or ``duration`` (seconds).
        If ``video`` is given without explicit dimensions, the server reads them from the file.
        """
        if video is None and duration is None:
            raise ValueError("Either 'video' (file) or 'duration' (seconds) must be provided.")
        url = self._client._resolve_endpoint("vid_replace_price")
        if video is not None:
            data: dict[str, Any] = {"model": model}
            if width is not None:
                data["width"] = width
            if height is not None:
                data["height"] = height
            files = [("video", normalize_file(video, "video"))]
            resp = self._client.post(url, data=data, files=files)
        else:
            data_mp: dict[str, Any] = {"model": model}
            if duration is not None:
                data_mp["duration"] = str(duration)
            if width is not None:
                data_mp["width"] = str(width)
            if height is not None:
                data_mp["height"] = str(height)
            resp = self._client.post(url, data=data_mp)
        return PriceResult.model_validate(resp.get("data", resp))

    def upscale(
        self,
        *,
        video: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a video upscale job."""
        url = self._client._resolve_endpoint("vid_upscale")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("video", normalize_file(video, "video"))]
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def upscale_price(
        self,
        *,
        model: str,
        video: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for video upscale."""
        url = self._client._resolve_endpoint("vid_upscale_price")
        if video is not None:
            data: dict[str, Any] = {"model": model}
            files = [("video", normalize_file(video, "video"))]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"model": model}
            if width is not None:
                payload["width"] = width
            if height is not None:
                payload["height"] = height
            resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def remove_background(
        self,
        *,
        video: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a video background removal job."""
        url = self._client._resolve_endpoint("vid_rmbg")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("video", normalize_file(video, "video"))]
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def remove_background_price(
        self,
        *,
        model: str,
        video: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for video background removal."""
        url = self._client._resolve_endpoint("vid_rmbg_price")
        if video is not None:
            data: dict[str, Any] = {"model": model}
            files = [("video", normalize_file(video, "video"))]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"model": model}
            if width is not None:
                payload["width"] = width
            if height is not None:
                payload["height"] = height
            resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


class AsyncVideo:
    """Async video resource — generation, animation, audio-to-video, replace, upscale, and background removal (v1)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def generate(
        self,
        *,
        prompt: str,
        model: str,
        width: int,
        height: int,
        steps: int,
        seed: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        guidance: float | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a text-to-video generation job."""
        url = self._client._resolve_endpoint("txt2video")
        payload = _build_txt2video_payload(
            prompt=prompt, model=model, width=width, height=height,
            steps=steps, seed=seed, frames=frames, fps=fps,
            negative_prompt=negative_prompt, guidance=guidance,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def generate_price(
        self,
        *,
        prompt: str,
        model: str,
        width: int,
        height: int,
        steps: int,
        seed: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        guidance: float | None = None,
    ) -> PriceResult:
        """Calculate price for text-to-video generation."""
        url = self._client._resolve_endpoint("txt2video_price")
        payload = _build_txt2video_payload(
            prompt=prompt, model=model, width=width, height=height,
            steps=steps, seed=seed, frames=frames, fps=fps,
            negative_prompt=negative_prompt, guidance=guidance,
        )
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def animate(
        self,
        *,
        prompt: str,
        model: str,
        first_frame_image: FileInput,
        seed: int,
        width: int,
        height: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        last_frame_image: FileInput | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an image-to-video animation job."""
        url = self._client._resolve_endpoint("img2video")
        data, files = _build_img2video_multipart(
            prompt=prompt, model=model, first_frame_image=first_frame_image,
            seed=seed, width=width, height=height, frames=frames, fps=fps,
            negative_prompt=negative_prompt, last_frame_image=last_frame_image,
            guidance=guidance, steps=steps, webhook_url=webhook_url,
        )
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def animate_price(
        self,
        *,
        model: str,
        width: int,
        height: int,
        frames: int,
        fps: int,
        steps: int | None = None,
        guidance: float | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-video animation."""
        url = self._client._resolve_endpoint("img2video_price")
        payload: dict[str, Any] = {
            "model": model, "width": width, "height": height,
            "frames": frames, "fps": fps,
        }
        if steps is not None:
            payload["steps"] = steps
        if guidance is not None:
            payload["guidance"] = guidance
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def generate_from_audio(
        self,
        *,
        prompt: str,
        audio: FileInput,
        model: str,
        width: int,
        height: int,
        seed: int,
        frames: int,
        fps: int,
        negative_prompt: str | None = None,
        first_frame_image: FileInput | None = None,
        last_frame_image: FileInput | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an audio-to-video generation job."""
        url = self._client._resolve_endpoint("aud2video")
        data, files = _build_aud2video_multipart(
            prompt=prompt, audio=audio, model=model, width=width, height=height,
            seed=seed, frames=frames, fps=fps, negative_prompt=negative_prompt,
            first_frame_image=first_frame_image, last_frame_image=last_frame_image,
            guidance=guidance, steps=steps, webhook_url=webhook_url,
        )
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def generate_from_audio_price(
        self,
        *,
        model: str,
        width: int,
        height: int,
        frames: int,
        fps: int,
        guidance: float | None = None,
        steps: int | None = None,
    ) -> PriceResult:
        """Calculate price for audio-to-video generation."""
        url = self._client._resolve_endpoint("aud2video_price")
        payload: dict[str, Any] = {
            "model": model, "width": width, "height": height,
            "frames": frames, "fps": fps,
        }
        if guidance is not None:
            payload["guidance"] = guidance
        if steps is not None:
            payload["steps"] = steps
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def replace(
        self,
        *,
        video: FileInput,
        ref_image: FileInput,
        model: str,
        prompt: str | None = None,
        width: int | None = None,
        height: int | None = None,
        steps: int | None = None,
        seed: int | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a video replace job."""
        url = self._client._resolve_endpoint("vid_replace")
        data, files = _build_vid_replace_multipart(
            video=video, ref_image=ref_image, model=model, prompt=prompt,
            width=width, height=height, steps=steps, seed=seed,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def replace_price(
        self,
        *,
        model: str,
        video: FileInput | None = None,
        duration: float | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for video replace.

        Provide either ``video`` (file) or ``duration`` (seconds).
        If ``video`` is given without explicit dimensions, the server reads them from the file.
        """
        if video is None and duration is None:
            raise ValueError("Either 'video' (file) or 'duration' (seconds) must be provided.")
        url = self._client._resolve_endpoint("vid_replace_price")
        if video is not None:
            data: dict[str, Any] = {"model": model}
            if width is not None:
                data["width"] = width
            if height is not None:
                data["height"] = height
            files = [("video", normalize_file(video, "video"))]
            resp = await self._client.post(url, data=data, files=files)
        else:
            data_mp: dict[str, Any] = {"model": model}
            if duration is not None:
                data_mp["duration"] = str(duration)
            if width is not None:
                data_mp["width"] = str(width)
            if height is not None:
                data_mp["height"] = str(height)
            resp = await self._client.post(url, data=data_mp)
        return PriceResult.model_validate(resp.get("data", resp))

    async def upscale(
        self,
        *,
        video: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a video upscale job."""
        url = self._client._resolve_endpoint("vid_upscale")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("video", normalize_file(video, "video"))]
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def upscale_price(
        self,
        *,
        model: str,
        video: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for video upscale."""
        url = self._client._resolve_endpoint("vid_upscale_price")
        if video is not None:
            data: dict[str, Any] = {"model": model}
            files = [("video", normalize_file(video, "video"))]
            resp = await self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"model": model}
            if width is not None:
                payload["width"] = width
            if height is not None:
                payload["height"] = height
            resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def remove_background(
        self,
        *,
        video: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a video background removal job."""
        url = self._client._resolve_endpoint("vid_rmbg")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("video", normalize_file(video, "video"))]
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def remove_background_price(
        self,
        *,
        model: str,
        video: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for video background removal."""
        url = self._client._resolve_endpoint("vid_rmbg_price")
        if video is not None:
            data: dict[str, Any] = {"model": model}
            files = [("video", normalize_file(video, "video"))]
            resp = await self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"model": model}
            if width is not None:
                payload["width"] = width
            if height is not None:
                payload["height"] = height
            resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


# --- Private helpers ---

def _build_txt2video_payload(
    *,
    prompt: str,
    model: str,
    width: int,
    height: int,
    steps: int,
    seed: int,
    frames: int,
    fps: int,
    negative_prompt: str | None = None,
    guidance: float | None = None,
    webhook_url: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "width": width,
        "height": height,
        "steps": steps,
        "seed": seed,
        "frames": frames,
        "fps": fps,
    }
    if negative_prompt is not None:
        payload["negative_prompt"] = negative_prompt
    if guidance is not None:
        payload["guidance"] = guidance
    if webhook_url is not None:
        payload["webhook_url"] = webhook_url
    return payload


def _build_img2video_multipart(
    *,
    prompt: str,
    model: str,
    first_frame_image: FileInput,
    seed: int,
    width: int,
    height: int,
    frames: int,
    fps: int,
    negative_prompt: str | None = None,
    last_frame_image: FileInput | None = None,
    guidance: float | None = None,
    steps: int | None = None,
    webhook_url: str | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    """Build multipart form data and files list for img2video."""
    data: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "seed": seed,
        "width": width,
        "height": height,
        "frames": frames,
        "fps": fps,
    }
    if negative_prompt is not None:
        data["negative_prompt"] = negative_prompt
    if guidance is not None:
        data["guidance"] = guidance
    if steps is not None:
        data["steps"] = steps
    if webhook_url is not None:
        data["webhook_url"] = webhook_url

    file_tuples: list[tuple[str, tuple[str, bytes, str]]] = []
    file_tuples.append(("first_frame_image", normalize_file(first_frame_image, "first_frame_image")))
    if last_frame_image is not None:
        file_tuples.append(("last_frame_image", normalize_file(last_frame_image, "last_frame_image")))

    return data, file_tuples


def _build_aud2video_multipart(
    *,
    prompt: str,
    audio: FileInput,
    model: str,
    width: int,
    height: int,
    seed: int,
    frames: int,
    fps: int,
    negative_prompt: str | None = None,
    first_frame_image: FileInput | None = None,
    last_frame_image: FileInput | None = None,
    guidance: float | None = None,
    steps: int | None = None,
    webhook_url: str | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    """Build multipart form data and files list for aud2video."""
    data: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "width": width,
        "height": height,
        "seed": seed,
        "frames": frames,
        "fps": fps,
    }
    if negative_prompt is not None:
        data["negative_prompt"] = negative_prompt
    if guidance is not None:
        data["guidance"] = guidance
    if steps is not None:
        data["steps"] = steps
    if webhook_url is not None:
        data["webhook_url"] = webhook_url

    file_tuples: list[tuple[str, tuple[str, bytes, str]]] = []
    file_tuples.append(("audio", normalize_file(audio, "audio")))
    if first_frame_image is not None:
        file_tuples.append(("first_frame_image", normalize_file(first_frame_image, "first_frame_image")))
    if last_frame_image is not None:
        file_tuples.append(("last_frame_image", normalize_file(last_frame_image, "last_frame_image")))

    return data, file_tuples


def _build_vid_replace_multipart(
    *,
    video: FileInput,
    ref_image: FileInput,
    model: str,
    prompt: str | None = None,
    width: int | None = None,
    height: int | None = None,
    steps: int | None = None,
    seed: int | None = None,
    webhook_url: str | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    """Build multipart form data and files list for video replace."""
    data: dict[str, Any] = {"model": model}
    if prompt is not None:
        data["prompt"] = prompt
    if width is not None:
        data["width"] = width
    if height is not None:
        data["height"] = height
    if steps is not None:
        data["steps"] = steps
    if seed is not None:
        data["seed"] = seed
    if webhook_url is not None:
        data["webhook_url"] = webhook_url

    file_tuples: list[tuple[str, tuple[str, bytes, str]]] = [
        ("video", normalize_file(video, "video")),
        ("ref_image", normalize_file(ref_image, "ref_image")),
    ]

    return data, file_tuples
