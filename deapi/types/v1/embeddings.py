from __future__ import annotations

from pydantic import BaseModel


class Text2EmbeddingParams(BaseModel):
    input: str | list[str]
    model: str
    return_result_in_response: bool | None = None
    webhook_url: str | None = None
