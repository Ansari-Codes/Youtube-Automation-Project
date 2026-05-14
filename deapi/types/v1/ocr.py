from __future__ import annotations

from pydantic import BaseModel


class Img2TextParams(BaseModel):
    """Parameters for image-to-text (OCR) requests."""

    model: str
    language: str | None = None
    format: str | None = None
    return_result_in_response: bool | None = None
    webhook_url: str | None = None
