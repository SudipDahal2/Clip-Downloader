import glob
import os
import shutil
import tempfile

import yt_dlp
from .progress_tracker import set_progress, is_cancelled, get_progress

# ===============================
# Base downloads folder
# ===============================
BASE_DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "yt_downloads")
os.makedirs(BASE_DOWNLOAD_DIR, exist_ok=True)

# ===============================
# YouTube auth/runtime settings
# ===============================
COOKIE_FILE = os.environ.get("YTDLP_COOKIE_FILE", "/app/cookies.txt")
YOUTUBE_PLAYER_CLIENT = os.environ.get("YOUTUBE_PLAYER_CLIENT", "mweb").strip()
YOUTUBE_PO_TOKEN = os.environ.get("YOUTUBE_PO_TOKEN", "").strip()


def _youtube_extractor_args():
    args = {
        "player_client": [YOUTUBE_PLAYER_CLIENT],
    }

    if YOUTUBE_PO_TOKEN:
        args["po_token"] = [f"{YOUTUBE_PLAYER_CLIENT}+{YOUTUBE_PO_TOKEN}"]

    return {"youtube": args}


def _base_ydl_opts():
    opts = {
        "cookiefile": COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
        "noplaylist": True,
        "quiet": False,
        "verbose": True,
        "nocheckcertificate": True,
        "extractor_args": _youtube_extractor_args(),
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": 1,
    }

    if not opts["cookiefile"]:
        opts.pop("cookiefile", None)

    return opts


# =====================================================
# GET VIDEO INFORMATION
# =====================================================
def extract_info(url):
    ydl_opts = {
        **_base_ydl_opts(),
        "skip_download": True,
        "quiet": True,
        "verbose": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return info.get("title", "Unknown"), info.get("thumbnail", "")


# =====================================================
# DOWNLOAD MEDIA
# Each task gets its own isolated folder: /tmp/yt_downloads/<task_id>/
# =====================================================
def download_media(task_id, urls, file_format, quality="192"):
    task_dir = os.path.join(BASE_DOWNLOAD_DIR, task_id)
    os.makedirs(task_dir, exist_ok=True)

    def progress_hook(d):
        if is_cancelled(task_id):
            raise Exception("Download cancelled by user")

        status = d.get("status")

        if status == "downloading":
            set_progress(task_id, {
                "status": "downloading",
                "percent": d.get("_percent_str", "0%").strip(),
                "speed": d.get("_speed_str", "").strip(),
                "eta": d.get("_eta_str", "").strip(),
            })

        elif status == "finished":
            set_progress(task_id, {
                "status": "processing",
                "percent": "100%",
                "speed": "",
                "eta": "",
            })

    outtmpl = os.path.join(task_dir, "%(title)s.%(ext)s")

    common_opts = {
        **_base_ydl_opts(),
        "outtmpl": outtmpl,
        "progress_hooks": [progress_hook],
    }

    if file_format == "mp3":
        preferred_quality = str(quality) if str(quality).isdigit() else "192"

        ydl_opts = {
            **common_opts,
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": preferred_quality,
            }],
        }
        expected_exts = ("*.mp3",)
    else:
        max_height = str(quality) if str(quality).isdigit() else "1080"

        ydl_opts = {
            **common_opts,
            "format": (
                f"bestvideo[height<={max_height}]+bestaudio/"
                f"best[height<={max_height}]/best"
            ),
            "merge_output_format": "mp4",
        }
        expected_exts = ("*.mp4", "*.mkv", "*.webm")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

        if is_cancelled(task_id):
            return

        filepath = None
        for pattern in expected_exts:
            matches = glob.glob(os.path.join(task_dir, pattern))
            if matches:
                filepath = matches[0]
                break

        if not filepath:
            all_files = [
                f for f in glob.glob(os.path.join(task_dir, "*"))
                if os.path.isfile(f)
            ]
            filepath = all_files[0] if all_files else None

        if not filepath:
            raise Exception("Download finished but output file was not found")

        set_progress(task_id, {
            "status": "done",
            "percent": "100%",
            "speed": "",
            "eta": "",
            "filepath": filepath,
        })

    except Exception as e:
        err = str(e)

        if "cancelled" not in err.lower():
            set_progress(task_id, {
                "status": "error",
                "percent": "0%",
                "speed": "",
                "eta": "",
                "error": err,
            })

    finally:
        task = get_progress(task_id)
        if task.get("status") not in ("done", "completed"):
            shutil.rmtree(task_dir, ignore_errors=True)