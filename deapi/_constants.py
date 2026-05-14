from __future__ import annotations


# URL prefix per API version.
# v1 sits under /api/v1/client/* (legacy), v2 drops the /client/ segment.
PREFIXES: dict[str, str] = {
    "v1": "/api/v1/client",
    "v2": "/api/v2",
}


# Endpoint paths per API version.
# Resource classes resolve paths via ENDPOINTS[version][operation_name].
# Operation keys are stable across versions where possible so resource classes
# can be shared — only the path values differ.

ENDPOINTS: dict[str, dict[str, str]] = {
    "v1": {
        # Images
        "txt2img": "txt2img",
        "txt2img_price": "txt2img/price-calculation",
        "img2img": "img2img",
        "img2img_price": "img2img/price-calculation",
        "img_upscale": "img-upscale",
        "img_upscale_price": "img-upscale/price-calculation",
        "img_rmbg": "img-rmbg",
        "img_rmbg_price": "img-rmbg/price-calculation",
        # Audio
        "txt2audio": "txt2audio",
        "txt2audio_price": "txt2audio/price-calculation",
        "txt2music": "txt2music",
        "txt2music_price": "txt2music/price-calculation",
        # Video
        "txt2video": "txt2video",
        "txt2video_price": "txt2video/price-calculation",
        "img2video": "img2video",
        "img2video_price": "img2video/price-calculation",
        "vid_upscale": "vid-upscale",
        "vid_upscale_price": "vid-upscale/price-calculation",
        "vid_rmbg": "vid-rmbg",
        "vid_rmbg_price": "vid-rmbg/price-calculation",
        "aud2video": "aud2video",
        "aud2video_price": "aud2video/price-calculation",
        "vid_replace": "videos/replace",
        "vid_replace_price": "videos/replace/price",
        # Transcription
        "transcribe": "transcribe",
        "transcribe_price": "transcribe/price-calculation",
        "vid2txt": "vid2txt",
        "vid2txt_price": "vid2txt/price-calculation",
        "aud2txt": "aud2txt",
        "aud2txt_price": "aud2txt/price-calculation",
        "audiofile2txt": "audiofile2txt",
        "audiofile2txt_price": "audiofile2txt/price-calculation",
        "videofile2txt": "videofile2txt",
        "videofile2txt_price": "videofile2txt/price-calculation",
        # Embeddings
        "txt2embedding": "txt2embedding",
        "txt2embedding_price": "txt2embedding/price-calculation",
        # Image-to-text (OCR)
        "img2txt": "img2txt",
        "img2txt_price": "img2txt/price-calculation",
        # Prompts
        "prompt_image": "prompt/image",
        "prompt_image_price": "prompt/image/price-calculation",
        "prompt_video": "prompt/video",
        "prompt_video_price": "prompt/video/price-calculation",
        "prompt_speech": "prompt/speech",
        "prompt_speech_price": "prompt/speech/price-calculation",
        "prompt_image2image": "prompt/image2image",
        "prompt_image2image_price": "prompt/image2image/price-calculation",
        "prompt_samples": "prompts/samples",
        "prompt_samples_price": "prompts/samples/price-calculation",
        # Account
        "balance": "balance",
        "models": "models",
        "request_status": "request-status",
    },
    "v2": {
        # Images
        "txt2img": "images/generations",
        "txt2img_price": "images/generations/price",
        "img2img": "images/edits",
        "img2img_price": "images/edits/price",
        "img_upscale": "images/upscales",
        "img_upscale_price": "images/upscales/price",
        "img_rmbg": "images/background-removals",
        "img_rmbg_price": "images/background-removals/price",
        # Audio
        "txt2audio": "audio/speech",
        "txt2audio_price": "audio/speech/price",
        "txt2music": "audio/music",
        "txt2music_price": "audio/music/price",
        # Video
        "txt2video": "videos/generations",
        "txt2video_price": "videos/generations/price",
        "img2video": "videos/animations",
        "img2video_price": "videos/animations/price",
        "vid_upscale": "videos/upscales",
        "vid_upscale_price": "videos/upscales/price",
        "vid_rmbg": "videos/background-removals",
        "vid_rmbg_price": "videos/background-removals/price",
        "aud2video": "videos/audio-syncs",
        "aud2video_price": "videos/audio-syncs/price",
        "vid_replace": "videos/replacements",
        "vid_replace_price": "videos/replacements/price",
        # Transcription (unified — single endpoint replaces all v1 transcription routes)
        "transcribe": "audio/transcriptions",
        "transcribe_price": "audio/transcriptions/price",
        # Embeddings
        "txt2embedding": "embeddings",
        "txt2embedding_price": "embeddings/price",
        # Image-to-text (OCR)
        "img2txt": "images/ocr",
        "img2txt_price": "images/ocr/price",
        # Prompts (unified enhancer — replaces all v1 prompt booster routes)
        "prompts_enhance": "prompts/enhancements",
        "prompts_enhance_price": "prompts/enhancements/price",
        # Account
        "balance": "account/balance",
        "models": "models",
        "request_status": "jobs",
    },
}
