import requests
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
import sys


def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename


def fit_video_to_audio(video_clip, target_duration):
    video_duration = video_clip.duration

    # Trim
    if video_duration > target_duration:
        return video_clip.subclip(0, target_duration)

    # Loop
    clips = []
    current = 0

    while current < target_duration:
        remaining = target_duration - current
        clip_duration = min(video_duration, remaining)
        clips.append(video_clip.subclip(0, clip_duration))
        current += clip_duration

    return concatenate_videoclips(clips)


def merge(video_url, audio_url, output="final.mp4"):
    video_path = download_file(video_url, "video.mp4")
    audio_path = download_file(audio_url, "audio.wav")

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final_video = fit_video_to_audio(video, audio.duration)
    final_video = final_video.set_audio(audio)

    final_video.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=video.fps
    )

    video.close()
    audio.close()
    final_video.close()

    os.remove(video_path)
    os.remove(audio_path)

    print("Done:", output)


# ---------------------------
# CLI INPUT (sys.argv FIX)
# ---------------------------

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <video_url> <audio_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    audio_url = sys.argv[2]

    merge(video_url, audio_url)