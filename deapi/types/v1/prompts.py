from __future__ import annotations

from pydantic import BaseModel


class EnhancePromptResult(BaseModel):
    """Result from prompt enhancement endpoints (image, video, image2image)."""
    prompt: str
    negative_prompt: str | None = None


class EnhanceSpeechPromptResult(BaseModel):
    """Result from speech prompt enhancement (no negative_prompt)."""
    prompt: str


class SamplePromptResult(BaseModel):
    """Result from sample prompts endpoint."""
    type: str
    prompt: str
