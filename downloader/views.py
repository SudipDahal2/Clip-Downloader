import uuid
import os
import shutil
import threading
from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, Http404

from .forms import DownloadForm
from .youtube_downloader import download_media, extract_info
from .progress_tracker import (
    create_task,
    get_all_tasks,
    get_progress,
    cancel_task,
    toggle_pause,
)


# ── Home ────────────────────────────────────────────────────
def home(request):
    form = DownloadForm()
    return render(request, "home.html", {"form": form})


# ── Start download ───────────────────────────────────────────
def start_download(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    form = DownloadForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"error": "Invalid form"}, status=400)

    raw_urls    = form.cleaned_data["url"]
    file_format = form.cleaned_data["file_format"]
    mode        = form.cleaned_data["mode"]
    quality     = form.cleaned_data.get("quality", "")
    if not quality:
        quality = "192" if file_format == "mp3" else "1080"

    urls = [u.strip() for u in raw_urls.splitlines() if u.strip()] \
           if mode == "bulk" else [raw_urls.strip()]

    created_tasks = []

    for url in urls:
        task_id = str(uuid.uuid4())

        try:
            title, thumbnail = extract_info(url)
        except Exception:
            title, thumbnail = "Unknown Title", ""

        create_task(task_id, title, thumbnail)

        thread = threading.Thread(
            target=download_media,
            args=(task_id, [url], file_format, quality),
            daemon=True,
        )
        thread.start()
        created_tasks.append(task_id)

    return JsonResponse({"tasks": created_tasks})


# ── All tasks (polling) ──────────────────────────────────────
def all_tasks(request):
    tasks = get_all_tasks()
    # Don't expose the server filepath to the browser
    safe = {}
    for tid, data in tasks.items():
        safe[tid] = {k: v for k, v in data.items() if k != "filepath"}
    return JsonResponse(safe)


# ── Serve file to user's browser, then delete from server ───
def serve_file(request, task_id):
    task = get_progress(task_id)

    if task.get("status") not in ("done", "completed"):
        raise Http404("File not ready")

    filepath = task.get("filepath")
    if not filepath or not os.path.exists(filepath):
        raise Http404("File not found on server")

    filename = os.path.basename(filepath)

    # FileResponse streams the file directly to the user's browser.
    # The browser sees it as a download (Content-Disposition: attachment).
    task_dir = os.path.dirname(filepath)

    response = FileResponse(
        open(filepath, "rb"),
        as_attachment=True,
        filename=filename,
    )

    # Delete the task folder in the background. On Windows, an open file
    # cannot be deleted. Since FileResponse streams the file to the browser,
    # we must repeatedly try deleting it until the stream finishes and releases it.
    def cleanup():
        import time
        for _ in range(720):  # Try for up to 2 hours
            time.sleep(10)
            try:
                shutil.rmtree(task_dir)
            except Exception:
                pass
            if not os.path.exists(task_dir):
                break

    threading.Thread(target=cleanup, daemon=True).start()

    return response


# ── Cancel ───────────────────────────────────────────────────
def cancel(request, task_id):
    cancel_task(task_id)
    return JsonResponse({"status": "cancelled"})


# ── Pause / Resume ───────────────────────────────────────────
def pause(request, task_id):
    toggle_pause(task_id)
    return JsonResponse({"status": "toggled"})


