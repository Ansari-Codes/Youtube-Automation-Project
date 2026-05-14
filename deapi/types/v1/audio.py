from __future__ import annotations

from pydantic import BaseModel


class Text2AudioParams(BaseModel):
    text: str
    model: str
    lang: str
    format: str
    speed: float
    sample_rate: float
    mode: str | None = None
    voice: str | None = None
    ref_text: str | None = None
    instruct: str | None = None
    webhook_url: str | None = None


class Text2MusicParams(BaseModel):
    caption: str
    model: str
    duration: float
    inference_steps: int
    guidance_scale: float
    seed: int
    format: str
    lyrics: str | None = None
    bpm: int | None = None
    keyscale: str | None = None
    timesignature: int | None = None
    vocal_language: str | None = None
    webhook_url: str | None = None