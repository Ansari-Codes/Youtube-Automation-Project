from __future__ import annotations

from deapi.resources.v1.audio import AsyncAudio, Audio
from deapi.resources.v1.embeddings import AsyncEmbeddings, Embeddings
from deapi.resources.v1.images import AsyncImages, Images
from deapi.resources.v1.models import AsyncModels, Models
from deapi.resources.v1.ocr import AsyncOCR, OCR
from deapi.resources.v1.prompts import AsyncPrompts, Prompts
from deapi.resources.v1.transcription import AsyncTranscription, Transcription
from deapi.resources.v1.video import AsyncVideo, Video

__all__ = [
    "AsyncAudio",
    "AsyncEmbeddings",
    "AsyncImages",
    "AsyncModels",
    "AsyncOCR",
    "AsyncPrompts",
    "AsyncTranscription",
    "AsyncVideo",
    "Audio",
    "Embeddings",
    "Images",
    "Models",
    "OCR",
    "Prompts",
    "Transcription",
    "Video",
]
