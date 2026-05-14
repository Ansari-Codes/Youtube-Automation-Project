from __future__ import annotations

from pydantic import BaseModel


class TranscribeParams(BaseModel):
    """Params for the unified transcribe endpoint."""
    include_ts: bool
    model: str
    source_url: str | None = None
    source_file: str | None = None
    return_result_in_response: bool | None = None
    webhook_url: str | None = None


class VideoToTextParams(BaseModel):
    video_url: str
    include_ts: bool
    model: str
    return_result_in_response: bool | None = None
    webhook_url: str | None = None


class AudioToTextParams(BaseModel):
    audio_url: str
    include_ts: bool
    model: str
    return_result_in_response: bool | None = None
    webhook_url: str | None = None


class AudioFileToTextParams(BaseModel):
    include_ts: bool
    model: str
    return_result_in_response: bool | None = None
    webhook_url: str | None = None


class VideoFileToTextParams(BaseModel):
    include_ts: bool
    model: str
    return_result_in_response: bool | None = None
    webhook_url: str | None = None
