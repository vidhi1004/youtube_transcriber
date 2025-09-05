import os
import yt_dlp

def download_audio(youtube_url: str, output_dir: str = "data"):
    os.makedirs(output_dir, exist_ok=True)

    final_file = {}

    def hook(d):
        if d["status"] == "finished":
            final_file["path"] = d["filename"]

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "progress_hooks": [hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        video_id = info["id"]

    audio_path = final_file["path"]
    return audio_path, video_id
