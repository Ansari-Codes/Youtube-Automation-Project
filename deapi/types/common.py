from __future__ import annotations

from typing import Any

from pydantic import BaseModel, field_validator

from deapi._types import JobStatus


class JobSubmission(BaseModel):
    request_id: str


class JobResult(BaseModel):
    status: JobStatus
    preview: str | None = None
    result_url: str | None = None
    results_alt_formats: dict[str, str] | None = None
    result: str | None = None
    progress: float = 0.0


class PriceResult(BaseModel):
    price: float


class Balance(BaseModel):
    balance: float


class PaginationLinks(BaseModel):
    first: str | None = None
    last: str | None = None
    prev: str | None = None
    next: str | None = None


class PaginationMeta(BaseModel):
    current_page: int
    last_page: int
    per_page: int
    total: int


class ModelInfo(BaseModel):
    name: str
    slug: str
    inference_types: list[str]
    info: dict[str, Any] | None = None
    loras: list[dict[str, Any]] | None = None
    languages: list[dict[str, Any]] | None = None

    model_config = {"extra": "allow"}

    @field_validator("info", mode="before")
    @classmethod
    def _normalize_info(cls, v: Any) -> dict[str, Any] | None:
        # PHP/Laravel returns empty arrays as [] instead of {}
        if isinstance(v, list):
            return {} if len(v) == 0 else None
        return v


class ModelsResponse(BaseModel):
    data: list[ModelInfo]
    links: PaginationLinks
    meta: PaginationMeta
