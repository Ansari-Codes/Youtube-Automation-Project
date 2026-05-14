from __future__ import annotations

from typing import Any, Union

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput, normalize_file, normalize_files
from deapi._polling import AsyncJob, Job
from deapi.types.common import PriceResult
from deapi.types.v1.images import LoraWeight


class Images:
    """Sync image generation and transformation resource (v1)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def generate(
        self,
        *,
        prompt: str,
        model: str,
        width: int,
        height: int,
        seed: int,
        negative_prompt: str | None = None,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a text-to-image generation job."""
        url = self._client._resolve_endpoint("txt2img")
        payload = _build_txt2img_payload(
            prompt=prompt, model=model, width=width, height=height, seed=seed,
            negative_prompt=negative_prompt, loras=loras, guidance=guidance,
            steps=steps, webhook_url=webhook_url,
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
        seed: int,
        negative_prompt: str | None = None,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        guidance: float | None = None,
        steps: int | None = None,
    ) -> PriceResult:
        """Calculate price for text-to-image generation."""
        url = self._client._resolve_endpoint("txt2img_price")
        payload = _build_txt2img_payload(
            prompt=prompt, model=model, width=width, height=height, seed=seed,
            negative_prompt=negative_prompt, loras=loras, guidance=guidance,
            steps=steps,
        )
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def transform(
        self,
        *,
        prompt: str,
        model: str,
        steps: int,
        seed: int,
        image: FileInput | None = None,
        images: list[FileInput] | None = None,
        negative_prompt: str | None = None,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        width: int | None = None,
        height: int | None = None,
        guidance: float | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an image-to-image transformation job."""
        url = self._client._resolve_endpoint("img2img")
        data, files = _build_img2img_multipart(
            prompt=prompt, model=model, steps=steps, seed=seed,
            image=image, images=images, negative_prompt=negative_prompt,
            loras=loras, width=width, height=height, guidance=guidance,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def transform_price(
        self,
        *,
        prompt: str,
        model: str,
        steps: int,
        seed: int,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        guidance: float | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-image transformation."""
        url = self._client._resolve_endpoint("img2img_price")
        payload: dict[str, Any] = {
            "prompt": prompt, "model": model, "steps": steps, "seed": seed,
        }
        if loras is not None:
            payload["loras"] = _serialize_loras(loras)
        if guidance is not None:
            payload["guidance"] = guidance
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    def upscale(
        self,
        *,
        image: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an image upscale job."""
        url = self._client._resolve_endpoint("img_upscale")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("image", normalize_file(image, "image"))]
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def upscale_price(
        self,
        *,
        model: str,
        image: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for image upscale."""
        url = self._client._resolve_endpoint("img_upscale_price")
        if image is not None:
            data: dict[str, Any] = {"model": model}
            files = [("image", normalize_file(image, "image"))]
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
        image: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an image background removal job."""
        url = self._client._resolve_endpoint("img_rmbg")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("image", normalize_file(image, "image"))]
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def remove_background_price(
        self,
        *,
        model: str,
        image: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for image background removal."""
        url = self._client._resolve_endpoint("img_rmbg_price")
        if image is not None:
            data: dict[str, Any] = {"model": model}
            files = [("image", normalize_file(image, "image"))]
            resp = self._client.post(url, data=data, files=files)
        else:
            payload: dict[str, Any] = {"model": model}
            if width is not None:
                payload["width"] = width
            if height is not None:
                payload["height"] = height
            resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


class AsyncImages:
    """Async image generation and transformation resource (v1)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def generate(
        self,
        *,
        prompt: str,
        model: str,
        width: int,
        height: int,
        seed: int,
        negative_prompt: str | None = None,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a text-to-image generation job."""
        url = self._client._resolve_endpoint("txt2img")
        payload = _build_txt2img_payload(
            prompt=prompt, model=model, width=width, height=height, seed=seed,
            negative_prompt=negative_prompt, loras=loras, guidance=guidance,
            steps=steps, webhook_url=webhook_url,
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
        seed: int,
        negative_prompt: str | None = None,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        guidance: float | None = None,
        steps: int | None = None,
    ) -> PriceResult:
        """Calculate price for text-to-image generation."""
        url = self._client._resolve_endpoint("txt2img_price")
        payload = _build_txt2img_payload(
            prompt=prompt, model=model, width=width, height=height, seed=seed,
            negative_prompt=negative_prompt, loras=loras, guidance=guidance,
            steps=steps,
        )
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def transform(
        self,
        *,
        prompt: str,
        model: str,
        steps: int,
        seed: int,
        image: FileInput | None = None,
        images: list[FileInput] | None = None,
        negative_prompt: str | None = None,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        width: int | None = None,
        height: int | None = None,
        guidance: float | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an image-to-image transformation job."""
        url = self._client._resolve_endpoint("img2img")
        data, files = _build_img2img_multipart(
            prompt=prompt, model=model, steps=steps, seed=seed,
            image=image, images=images, negative_prompt=negative_prompt,
            loras=loras, width=width, height=height, guidance=guidance,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def transform_price(
        self,
        *,
        prompt: str,
        model: str,
        steps: int,
        seed: int,
        loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
        guidance: float | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-image transformation."""
        url = self._client._resolve_endpoint("img2img_price")
        payload: dict[str, Any] = {
            "prompt": prompt, "model": model, "steps": steps, "seed": seed,
        }
        if loras is not None:
            payload["loras"] = _serialize_loras(loras)
        if guidance is not None:
            payload["guidance"] = guidance
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))

    async def upscale(
        self,
        *,
        image: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an image upscale job."""
        url = self._client._resolve_endpoint("img_upscale")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("image", normalize_file(image, "image"))]
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def upscale_price(
        self,
        *,
        model: str,
        image: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for image upscale."""
        url = self._client._resolve_endpoint("img_upscale_price")
        if image is not None:
            data: dict[str, Any] = {"model": model}
            files = [("image", normalize_file(image, "image"))]
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
        image: FileInput,
        model: str,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an image background removal job."""
        url = self._client._resolve_endpoint("img_rmbg")
        data: dict[str, Any] = {"model": model}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        files = [("image", normalize_file(image, "image"))]
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def remove_background_price(
        self,
        *,
        model: str,
        image: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for image background removal."""
        url = self._client._resolve_endpoint("img_rmbg_price")
        if image is not None:
            data: dict[str, Any] = {"model": model}
            files = [("image", normalize_file(image, "image"))]
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

def _serialize_loras(
    loras: list[Union[LoraWeight, dict[str, Any]]],
) -> list[dict[str, Any]]:
    return [
        lora.model_dump() if isinstance(lora, LoraWeight) else lora
        for lora in loras
    ]


def _build_txt2img_payload(
    *,
    prompt: str,
    model: str,
    width: int,
    height: int,
    seed: int,
    negative_prompt: str | None = None,
    loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
    guidance: float | None = None,
    steps: int | None = None,
    webhook_url: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "width": width,
        "height": height,
        "seed": seed,
    }
    if negative_prompt is not None:
        payload["negative_prompt"] = negative_prompt
    if loras is not None:
        payload["loras"] = _serialize_loras(loras)
    if guidance is not None:
        payload["guidance"] = guidance
    if steps is not None:
        payload["steps"] = steps
    if webhook_url is not None:
        payload["webhook_url"] = webhook_url
    return payload


def _build_img2img_multipart(
    *,
    prompt: str,
    model: str,
    steps: int,
    seed: int,
    image: FileInput | None = None,
    images: list[FileInput] | None = None,
    negative_prompt: str | None = None,
    loras: list[Union[LoraWeight, dict[str, Any]]] | None = None,
    width: int | None = None,
    height: int | None = None,
    guidance: float | None = None,
    webhook_url: str | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    """Build multipart form data and files list for img2img."""
    if image is not None and images is not None:
        raise ValueError("Provide either 'image' or 'images', not both.")
    if image is None and images is None:
        raise ValueError("Either 'image' or 'images' is required.")

    data: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "steps": steps,
        "seed": seed,
    }
    if negative_prompt is not None:
        data["negative_prompt"] = negative_prompt
    if width is not None:
        data["width"] = width
    if height is not None:
        data["height"] = height
    if guidance is not None:
        data["guidance"] = guidance
    if webhook_url is not None:
        data["webhook_url"] = webhook_url
    if loras is not None:
        serialized = _serialize_loras(loras)
        for i, lora in enumerate(serialized):
            data[f"loras[{i}][name]"] = lora["name"]
            data[f"loras[{i}][weight]"] = lora["weight"]

    file_tuples: list[tuple[str, tuple[str, bytes, str]]] = []
    if image is not None:
        normalized = normalize_file(image, "image")
        file_tuples.append(("image", normalized))
    elif images is not None:
        for f in normalize_files(images, "image"):
            file_tuples.append(("images[]", f))

    return data, file_tuples
