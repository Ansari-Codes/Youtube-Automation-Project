from __future__ import annotations

from typing import Any

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi.types.common import ModelsResponse


class Models:
    """Sync models listing resource (v1)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def list(
        self,
        *,
        per_page: int = 15,
        page: int = 1,
        inference_types: list[str] | None = None,
    ) -> ModelsResponse:
        """List available models with optional filtering."""
        url = self._client._resolve_endpoint("models")
        params: dict[str, Any] = {"per_page": per_page, "page": page}
        if inference_types is not None:
            params["filter[inference_types]"] = ",".join(inference_types)
        resp = self._client.get(url, params=params)
        return ModelsResponse.model_validate(resp)


class AsyncModels:
    """Async models listing resource (v1)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        per_page: int = 15,
        page: int = 1,
        inference_types: list[str] | None = None,
    ) -> ModelsResponse:
        """List available models with optional filtering."""
        url = self._client._resolve_endpoint("models")
        params: dict[str, Any] = {"per_page": per_page, "page": page}
        if inference_types is not None:
            params["filter[inference_types]"] = ",".join(inference_types)
        resp = await self._client.get(url, params=params)
        return ModelsResponse.model_validate(resp)
