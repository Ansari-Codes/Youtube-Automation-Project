from __future__ import annotations

from typing import Any, Union

from deapi._client import AsyncHTTPClient, SyncHTTPClient
from deapi._polling import AsyncJob, Job
from deapi.types.common import PriceResult


class Embeddings:
    """Sync embeddings resource (v1)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def create(
        self,
        *,
        input: Union[str, list[str]],
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """Submit a text-to-embedding job."""
        url = self._client._resolve_endpoint("txt2embedding")
        payload = _build_embedding_payload(
            input=input, model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return Job(request_id, self._client, status_url)

    def create_price(
        self,
        *,
        input: Union[str, list[str]],
        model: str,
        return_result_in_response: bool | None = None,
    ) -> PriceResult:
        """Calculate price for text-to-embedding."""
        url = self._client._resolve_endpoint("txt2embedding_price")
        payload = _build_embedding_payload(
            input=input, model=model,
            return_result_in_response=return_result_in_response,
        )
        resp = self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


class AsyncEmbeddings:
    """Async embeddings resource (v1)."""

    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        input: Union[str, list[str]],
        model: str,
        return_result_in_response: bool | None = None,
        webhook_url: str | None = None,
    ) -> AsyncJob:
        """Submit a text-to-embedding job."""
        url = self._client._resolve_endpoint("txt2embedding")
        payload = _build_embedding_payload(
            input=input, model=model,
            return_result_in_response=return_result_in_response,
            webhook_url=webhook_url,
        )
        resp = await self._client.post(url, json=payload)
        request_id = resp["data"]["request_id"]
        status_url = self._client._resolve_endpoint("request_status")
        return AsyncJob(request_id, self._client, status_url)

    async def create_price(
        self,
        *,
        input: Union[str, list[str]],
        model: str,
        return_result_in_response: bool | None = None,
    ) -> PriceResult:
        """Calculate price for text-to-embedding."""
        url = self._client._resolve_endpoint("txt2embedding_price")
        payload = _build_embedding_payload(
            input=input, model=model,
            return_result_in_response=return_result_in_response,
        )
        resp = await self._client.post(url, json=payload)
        return PriceResult.model_validate(resp.get("data", resp))


# --- Private helpers ---

def _build_embedding_payload(
    *,
    input: Union[str, list[str]],
    model: str,
    return_result_in_response: bool | None = None,
    webhook_url: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "input": input,
        "model": model,
    }
    if return_result_in_response is not None:
        payload["return_result_in_response"] = return_result_in_response
    if webhook_url is not None:
        payload["webhook_url"] = webhook_url
    return payload
