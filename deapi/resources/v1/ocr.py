from __future__ import annotations

from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._files import FileInput, normalize_file
from deapi._polling import AsyncJob, Job
from deapi.types.common import PriceResult


class OCR:
    """Sync image-to-text (OCR) resource (v1)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def extract(
        self,
        *,
        image: FileInput,
        model: str,
        language: str | None = None,
        format: str | None = None,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit an image-to-text (OCR) job."""
        url = self._client._resolve_endpoint("img2txt")
        data, files = _build_img2txt_multipart(
            image=image, model=model, language=language, format=format,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def extract_price(
        self,
        *,
        model: str,
        image: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-text (OCR)."""
        url = self._client._resolve_endpoint("img2txt_price")
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


class AsyncOCR:
    """Async image-to-text (OCR) resource (v1)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def extract(
        self,
        *,
        image: FileInput,
        model: str,
        language: str | None = None,
        format: str | None = None,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit an image-to-text (OCR) job."""
        url = self._client._resolve_endpoint("img2txt")
        data, files = _build_img2txt_multipart(
            image=image, model=model, language=language, format=format,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, data=data, files=files)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def extract_price(
        self,
        *,
        model: str,
        image: FileInput | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> PriceResult:
        """Calculate price for image-to-text (OCR)."""
        url = self._client._resolve_endpoint("img2txt_price")
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

def _build_img2txt_multipart(
    *,
    image: FileInput,
    model: str,
    language: str | None = None,
    format: str | None = None,
    return_result_in_response: bool | None = None,
    webhook_url: str | None = None,
) -> tuple[dict[str, Any], list[tuple[str, tuple[str, bytes, str]]]]:
    """Build multipart form data and files list for img2txt."""
    data: dict[str, Any] = {"model": model}
    if language is not None:
        data["language"] = language
    if format is not None:
        data["format"] = format
    if return_result_in_response is not None:
        data["return_result_in_response"] = "1" if return_result_in_response else "0"
    if webhook_url is not None:
        data["webhook_url"] = webhook_url

    files = [("image", normalize_file(image, "image"))]
    return data, files
