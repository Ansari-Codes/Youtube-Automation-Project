from __future__ import annotations

from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput, normalize_file
from deapi.types.common import PriceResult
from deapi.types.v1.prompts import EnhancePromptResult, EnhanceSpeechPromptResult, SamplePromptResult


class Prompts:
    """Sync prompt booster resource (v1)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def enhance_image(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        """Enhance a text-to-image prompt."""
        url = self._client._resolve_endpoint("prompt_image")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = self._client.post(url, json=payload)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    def enhance_image_price(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        """Calculate price for image prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_image_price")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def enhance_video(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> EnhancePromptResult:
        """Enhance a video prompt, optionally with a reference image."""
        url = self._client._resolve_endpoint("prompt_video")
        data, files = _build_video_prompt_multipart(
            prompt=prompt, negative_prompt=negative_prompt, image=image,
        )
        if files:
            resp = self._client.post(url, data=data, files=files)
        else:
            resp = self._client.post(url, json=data)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    def enhance_video_price(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        """Calculate price for video prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_video_price")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def enhance_speech(
        self,
        *,
        prompt: str,
        lang_code: str | None = None,
    ) -> EnhanceSpeechPromptResult:
        """Enhance a text-to-speech prompt."""
        url = self._client._resolve_endpoint("prompt_speech")
        payload: dict[str, Any] = {"prompt": prompt}
        if lang_code is not None:
            payload["lang_code"] = lang_code
        resp = self._client.post(url, json=payload)
        return EnhanceSpeechPromptResult.model_validate(resp.get("data", resp))

    def enhance_speech_price(
        self,
        *,
        prompt: str,
        lang_code: str | None = None,
    ) -> PriceResult:
        """Calculate price for speech prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_speech_price")
        payload: dict[str, Any] = {"prompt": prompt}
        if lang_code is not None:
            payload["lang_code"] = lang_code
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def enhance_image2image(
        self,
        *,
        prompt: str,
        image: FileInput,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        """Enhance an image-to-image prompt with a reference image."""
        url = self._client._resolve_endpoint("prompt_image2image")
        data: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt if negative_prompt is not None else "",
        }
        files = [("image", normalize_file(image, "image"))]
        resp = self._client.post(url, data=data, files=files)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    def enhance_image2image_price(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-image prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_image2image_price")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def samples(
        self,
        *,
        type: str,
        topic: str | None = None,
        lang_code: str | None = None,
    ) -> SamplePromptResult:
        """Get a sample prompt for image or speech generation."""
        url = self._client._resolve_endpoint("prompt_samples")
        params: dict[str, Any] = {"type": type}
        if topic is not None:
            params["topic"] = topic
        if lang_code is not None:
            params["lang_code"] = lang_code
        resp = self._client.get(url, params=params)
        return SamplePromptResult.model_validate(resp.get("data", resp))

    def samples_price(
        self,
        *,
        type: str,
        topic: str | None = None,
        lang_code: str | None = None,
    ) -> PriceResult:
        """Calculate price for getting a sample prompt."""
        url = self._client._resolve_endpoint("prompt_samples_price")
        params: dict[str, Any] = {"type": type}
        if topic is not None:
            params["topic"] = topic
        if lang_code is not None:
            params["lang_code"] = lang_code
        resp = self._client.get(url, params=params)
        return PriceResult.model_validate(resp.get("data", resp))


class AsyncPrompts:
    """Async prompt booster resource (v1)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def enhance_image(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        """Enhance a text-to-image prompt."""
        url = self._client._resolve_endpoint("prompt_image")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = await self._client.post(url, json=payload)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    async def enhance_image_price(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        """Calculate price for image prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_image_price")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def enhance_video(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> EnhancePromptResult:
        """Enhance a video prompt, optionally with a reference image."""
        url = self._client._resolve_endpoint("prompt_video")
        data, files = _build_video_prompt_multipart(
            prompt=prompt, negative_prompt=negative_prompt, image=image,
        )
        if files:
            resp = await self._client.post(url, data=data, files=files)
        else:
            resp = await self._client.post(url, json=data)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    async def enhance_video_price(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        """Calculate price for video prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_video_price")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def enhance_speech(
        self,
        *,
        prompt: str,
        lang_code: str | None = None,
    ) -> EnhanceSpeechPromptResult:
        """Enhance a text-to-speech prompt."""
        url = self._client._resolve_endpoint("prompt_speech")
        payload: dict[str, Any] = {"prompt": prompt}
        if lang_code is not None:
            payload["lang_code"] = lang_code
        resp = await self._client.post(url, json=payload)
        return EnhanceSpeechPromptResult.model_validate(resp.get("data", resp))

    async def enhance_speech_price(
        self,
        *,
        prompt: str,
        lang_code: str | None = None,
    ) -> PriceResult:
        """Calculate price for speech prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_speech_price")
        payload: dict[str, Any] = {"prompt": prompt}
        if lang_code is not None:
            payload["lang_code"] = lang_code
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def enhance_image2image(
        self,
        *,
        prompt: str,
        image: FileInput,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        """Enhance an image-to-image prompt with a reference image."""
        url = self._client._resolve_endpoint("prompt_image2image")
        data: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt if negative_prompt is not None else "",
        }
        files = [("image", normalize_file(image, "image"))]
        resp = await self._client.post(url, data=data, files=files)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    async def enhance_image2image_price(
        self,
        *,
        prompt: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-image prompt enhancement."""
        url = self._client._resolve_endpoint("prompt_image2image_price")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def samples(
        self,
        *,
        type: str,
        topic: str | None = None,
        lang_code: str | None = None,
    ) -> SamplePromptResult:
        """Get a sample prompt for image or speech generation."""
        url = self._client._resolve_endpoint("prompt_samples")
        params: dict[str, Any] = {"type": type}
        if topic is not None:
            params["topic"] = topic
        if lang_code is not None:
            params["lang_code"] = lang_code
        resp = await self._client.get(url, params=params)
        return SamplePromptResult.model_validate(resp.get("data", resp))

    async def samples_price(
        self,
        *,
        type: str,
        topic: str | None = None,
        lang_code: str | None = None,
    ) -> PriceResult:
        """Calculate price for getting a sample prompt."""
        url = self._client._resolve_endpoint("prompt_samples_price")
        params: dict[str, Any] = {"type": type}
        if topic is not None:
            params["topic"] = topic
        if lang_code is not None:
            params["lang_code"] = lang_code
        resp = await self._client.get(url, params=params)
        return PriceResult.model_validate(resp.get("data", resp))


# --- Private helpers ---

def _build_video_prompt_multipart(
    *,
    prompt: str,
    negative_prompt: str | None = None,
    image: FileInput | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    """Build form data for video prompt enhancement.

    ``negative_prompt`` is always included (API requires ``present`` validation).
    When sending as multipart, None is serialised as empty string; when sent as
    JSON by the caller, the value is kept as-is (``null`` in JSON).
    """
    file_tuples: list[tuple[str, tuple[str, bytes, str]]] = []
    if image is not None:
        file_tuples.append(("image", normalize_file(image, "image")))

    data: dict[str, Any] = {"prompt": prompt}
    # Always include negative_prompt for the API's `present` validation rule.
    # For multipart, use empty string to represent null; for JSON, use None.
    if file_tuples:
        data["negative_prompt"] = negative_prompt if negative_prompt is not None else ""
    else:
        data["negative_prompt"] = negative_prompt
    return data, file_tuples
