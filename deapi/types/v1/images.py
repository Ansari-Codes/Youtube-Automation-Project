from __future__ import annotations

from pydantic import BaseModel


class LoraWeight(BaseModel):
    name: str
    weight: float


class Text2ImageParams(BaseModel):
    prompt: str
    model: str
    width: int
    height: int
    seed: int
    negative_prompt: str | None = None
    loras: list[LoraWeight] | None = None
    guidance: float | None = None
    steps: int | None = None
    webhook_url: str | None = None


class Img2ImgParams(BaseModel):
    prompt: str
    model: str
    steps: int
    seed: int
    negative_prompt: str | None = None
    loras: list[LoraWeight] | None = None
    width: int | None = None
    height: int | None = None
    guidance: float | None = None
    webhook_url: str | None = None
