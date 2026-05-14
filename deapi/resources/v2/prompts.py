from __future__ import annotations

import warnings
from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput, normalize_file
from deapi.types.common import PriceResult
from deapi.types.v1.prompts import EnhancePromptResult


_LEGACY_DEPRECATION = (
    "v2 has a single unified prompt enhancer — call `prompts.enhance(prompt=..., "
    "type=..., model_slug=...)` instead. Legacy method '{name}' is deprecated and "
    "will route through the unified endpoint with type={type!r}."
)

_SAMPLES_REMOVED = (
    "The samples endpoint was removed in v2 with no direct replacement. "
    "Use `prompts.enhance(...)` with your own prompt seed instead."
)


class Prompts:
    """Sync prompt booster resource (v2).

    The v2 API consolidates all prompt boosting into a single unified
    endpoint that takes a ``type`` discriminator (e.g. ``"images.generations"``,
    ``"videos.animations"``, ``"audio.speech"``).

    Legacy v1-style methods are preserved for backward compatibility — they
    require a new ``model_slug`` kwarg, emit a ``DeprecationWarning``, and
    route to the unified endpoint with the appropriate ``type``.
    """

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def enhance(
        self,
        *,
        prompt: str,
        type: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> EnhancePromptResult:
        """Enhance a prompt via the unified v2 endpoint.

        ``type`` uses dot-notation matching the API resource (e.g.
        ``"images.generations"``, ``"images.edits"``, ``"videos.animations"``,
        ``"videos.generations"``, ``"audio.speech"``, ``"audio.music"``).
        ``image`` is required for ``images.edits`` and ``videos.animations``.
        """
        url = self._client._resolve_endpoint("prompts_enhance")
        files = _build_enhance_parts(
            prompt=prompt, type=type, model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )
        resp = self._client.post(url, files=files)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    def enhance_price(
        self,
        *,
        prompt: str,
        type: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> PriceResult:
        """Calculate price for prompt enhancement."""
        url = self._client._resolve_endpoint("prompts_enhance_price")
        files = _build_enhance_parts(
            prompt=prompt, type=type, model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )
        resp = self._client.post(url, files=files)
        return PriceResult.model_validate(resp.get("data", resp))

    # --- Legacy methods (deprecated, route to unified enhance) ---

    def enhance_image(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image", type="images.generations"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance(
            prompt=prompt, type="images.generations",
            model_slug=model_slug, negative_prompt=negative_prompt,
        )

    def enhance_image_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image_price", type="images.generations"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance_price(
            prompt=prompt, type="images.generations",
            model_slug=model_slug, negative_prompt=negative_prompt,
        )

    def enhance_video(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> EnhancePromptResult:
        # If an image is provided, route to videos.animations; otherwise
        # videos.generations.
        type_ = "videos.animations" if image is not None else "videos.generations"
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_video", type=type_),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance(
            prompt=prompt, type=type_, model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )

    def enhance_video_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_video_price", type="videos.generations"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance_price(
            prompt=prompt, type="videos.generations",
            model_slug=model_slug, negative_prompt=negative_prompt,
        )

    def enhance_speech(
        self,
        *,
        prompt: str,
        model_slug: str,
        lang_code: str | None = None,  # noqa: ARG002 — kept for v1 surface compat
    ) -> EnhancePromptResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_speech", type="audio.speech"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance(
            prompt=prompt, type="audio.speech", model_slug=model_slug,
        )

    def enhance_speech_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        lang_code: str | None = None,  # noqa: ARG002 — kept for v1 surface compat
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_speech_price", type="audio.speech"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance_price(
            prompt=prompt, type="audio.speech", model_slug=model_slug,
        )

    def enhance_image2image(
        self,
        *,
        prompt: str,
        image: FileInput,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image2image", type="images.edits"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance(
            prompt=prompt, type="images.edits", model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )

    def enhance_image2image_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image2image_price", type="images.edits"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.enhance_price(
            prompt=prompt, type="images.edits", model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )

    def samples(self, *, type: str, topic: str | None = None, lang_code: str | None = None) -> Any:  # noqa: ARG002
        raise NotImplementedError(_SAMPLES_REMOVED)

    def samples_price(self, *, type: str, topic: str | None = None, lang_code: str | None = None) -> Any:  # noqa: ARG002
        raise NotImplementedError(_SAMPLES_REMOVED)


class AsyncPrompts:
    """Async prompt booster resource (v2)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def enhance(
        self,
        *,
        prompt: str,
        type: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> EnhancePromptResult:
        url = self._client._resolve_endpoint("prompts_enhance")
        files = _build_enhance_parts(
            prompt=prompt, type=type, model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )
        resp = await self._client.post(url, files=files)
        return EnhancePromptResult.model_validate(resp.get("data", resp))

    async def enhance_price(
        self,
        *,
        prompt: str,
        type: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> PriceResult:
        url = self._client._resolve_endpoint("prompts_enhance_price")
        files = _build_enhance_parts(
            prompt=prompt, type=type, model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )
        resp = await self._client.post(url, files=files)
        return PriceResult.model_validate(resp.get("data", resp))

    async def enhance_image(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image", type="images.generations"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance(
            prompt=prompt, type="images.generations",
            model_slug=model_slug, negative_prompt=negative_prompt,
        )

    async def enhance_image_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image_price", type="images.generations"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance_price(
            prompt=prompt, type="images.generations",
            model_slug=model_slug, negative_prompt=negative_prompt,
        )

    async def enhance_video(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> EnhancePromptResult:
        type_ = "videos.animations" if image is not None else "videos.generations"
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_video", type=type_),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance(
            prompt=prompt, type=type_, model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )

    async def enhance_video_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_video_price", type="videos.generations"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance_price(
            prompt=prompt, type="videos.generations",
            model_slug=model_slug, negative_prompt=negative_prompt,
        )

    async def enhance_speech(
        self,
        *,
        prompt: str,
        model_slug: str,
        lang_code: str | None = None,  # noqa: ARG002
    ) -> EnhancePromptResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_speech", type="audio.speech"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance(
            prompt=prompt, type="audio.speech", model_slug=model_slug,
        )

    async def enhance_speech_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        lang_code: str | None = None,  # noqa: ARG002
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_speech_price", type="audio.speech"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance_price(
            prompt=prompt, type="audio.speech", model_slug=model_slug,
        )

    async def enhance_image2image(
        self,
        *,
        prompt: str,
        image: FileInput,
        model_slug: str,
        negative_prompt: str | None = None,
    ) -> EnhancePromptResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image2image", type="images.edits"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance(
            prompt=prompt, type="images.edits", model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )

    async def enhance_image2image_price(
        self,
        *,
        prompt: str,
        model_slug: str,
        negative_prompt: str | None = None,
        image: FileInput | None = None,
    ) -> PriceResult:
        warnings.warn(
            _LEGACY_DEPRECATION.format(name="enhance_image2image_price", type="images.edits"),
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.enhance_price(
            prompt=prompt, type="images.edits", model_slug=model_slug,
            negative_prompt=negative_prompt, image=image,
        )

    async def samples(self, *, type: str, topic: str | None = None, lang_code: str | None = None) -> Any:  # noqa: ARG002
        raise NotImplementedError(_SAMPLES_REMOVED)

    async def samples_price(self, *, type: str, topic: str | None = None, lang_code: str | None = None) -> Any:  # noqa: ARG002
        raise NotImplementedError(_SAMPLES_REMOVED)


# --- Private helpers ---

def _build_enhance_parts(
    *,
    prompt: str,
    type: str,
    model_slug: str,
    negative_prompt: str | None = None,
    image: FileInput | None = None,
) -> list[tuple[str, Any]]:
    """Build the multipart form parts for the unified prompt enhancer.

    The v2 ``prompts/enhancements`` endpoint declares ``multipart/form-data``
    as its only content type in the OpenAPI spec, so we must force multipart
    encoding even when no image is sent. httpx triggers multipart encoding
    when ``files=`` is non-empty — passing text fields as ``(name, (None, value))``
    tuples in ``files=`` is the documented httpx pattern for mixing text parts
    with file parts in a single multipart request.
    """
    parts: list[tuple[str, Any]] = [
        ("prompt", (None, prompt)),
        ("type", (None, type)),
        ("model_slug", (None, model_slug)),
    ]
    if negative_prompt is not None:
        parts.append(("negative_prompt", (None, negative_prompt)))
    if image is not None:
        parts.append(("image", normalize_file(image, "image")))
    return parts
