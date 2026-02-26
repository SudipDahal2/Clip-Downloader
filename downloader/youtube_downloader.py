import yt_dlp
import os
import glob
import tempfile
from django.conf import settings
from .progress_tracker import set_progress, is_cancelled, get_progress

# ===============================
# Base downloads folder
# ===============================
# We use the system's temporary directory so no files are saved in the project folder
BASE_DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "yt_downloads")
os.makedirs(BASE_DOWNLOAD_DIR, exist_ok=True)


# =====================================================
# GET VIDEO INFORMATION
# =====================================================
def extract_info(url):
    ydl_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info.get("title", "Unknown"), info.get("thumbnail", "")


# =====================================================
# DOWNLOAD MEDIA
# Each task gets its own isolated folder: downloads/<task_id>/
# so multiple users never collide.
# =====================================================
def download_media(task_id, urls, file_format, quality="192"):

    # Isolated folder per task — no collisions between users
    task_dir = os.path.join(BASE_DOWNLOAD_DIR, task_id)
    os.makedirs(task_dir, exist_ok=True)

    # ---------------------------
    # Progress Hook
    # ---------------------------
    def progress_hook(d):
        if is_cancelled(task_id):
            raise Exception("Download cancelled by user")

        if d["status"] == "downloading":
            set_progress(task_id, {
                "status":  "downloading",
                "percent": d.get("_percent_str", "0%").strip(),
                "speed":   d.get("_speed_str", "").strip(),
                "eta":     d.get("_eta_str", "").strip(),
            })

        elif d["status"] == "finished":
            set_progress(task_id, {
                "status":  "processing",
                "percent": "100%",
                "speed":   "",
                "eta":     "",
            })

    # ---------------------------
    # yt-dlp options
    # ---------------------------
    outtmpl = os.path.join(task_dir, "%(title)s.%(ext)s")

    if file_format == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "progress_hooks": [progress_hook],
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(quality),
            }],
        }
    else:
        # e.g 'bestvideo[height<=1080]+bestaudio/best'
        ydl_opts = {
            "format": f"bestvideo[height<={quality}]+bestaudio/best",
            "outtmpl": outtmpl,
            "progress_hooks": [progress_hook],
            "merge_output_format": "mp4",
        }

    # ---------------------------
    # Run download
    # ---------------------------
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

        if is_cancelled(task_id):
            return

        # Find the output file (yt-dlp names it based on video title)
        ext      = "mp3" if file_format == "mp3" else "mp4"
        matches  = glob.glob(os.path.join(task_dir, f"*.{ext}"))
        filepath = matches[0] if matches else None

        set_progress(task_id, {
            "status":   "done",
            "percent":  "100%",
            "speed":    "",
            "eta":      "",
            "filepath": filepath,   # ← stored so the serve view can find it
        })



    except Exception as e:
        err = str(e)
        if "cancelled" in err.lower():
            pass
        else:
            set_progress(task_id, {
                "status":  "error",
                "percent": "0%",
                "speed":   "",
                "eta":     "",
                "error":   err,
            })


    finally:
        # If the task didn't finish successfully, clean up its directory
        import shutil
        task = get_progress(task_id)
        if task.get("status") not in ("done", "completed"):
            shutil.rmtree(task_dir, ignore_errors=True)