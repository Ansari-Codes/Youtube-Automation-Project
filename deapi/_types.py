from __future__ import annotations

from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"


class InferenceType(str, Enum):
    TXT2IMG = "txt2img"
    IMG2IMG = "img2img"
    TXT2AUDIO = "txt2audio"
    TXT2MUSIC = "txt2music"
    VIDEO2TEXT = "video2text"
    AUDIO2TEXT = "audio2text"
    IMG2TXT = "img2txt"
    IMG2VIDEO = "img2video"
    TXT2VIDEO = "txt2video"
    TXT2EMBEDDING = "txt2embedding"
    VIDEO_FILE2TEXT = "video_file2text"
    AUDIO_FILE2TEXT = "audio_file2text"
    IMAGE_UPSCALE = "img-upscale"
    IMAGE_REMOVE_BG = "img-rmbg"
    VIDEO_UPSCALE = "vid-upscale"
    VIDEO_REMOVE_BG = "vid-rmbg"
