import os
import shutil
import threading
import time
import uuid

from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render

from .forms import DownloadForm
from .progress_tracker import (
    cancel_task,
    create_task,
    get_all_tasks,
    get_progress,
    toggle_pause,
)
from .youtube_downloader import download_media, extract_info


def home(request):
    form = DownloadForm()
    return render(request, "home.html", {"form": form})


def start_download(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    form = DownloadForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"error": form.errors}, status=400)

    raw_urls = form.cleaned_data["url"].strip()
    file_format = form.cleaned_data["file_format"].lower().strip()
    mode = form.cleaned_data["mode"].strip()
    quality = (form.cleaned_data.get("quality") or "").strip()

    if not quality:
        quality = "192" if file_format == "mp3" else "1080"

    urls = (
        [u.strip() for u in raw_urls.splitlines() if u.strip()]
        if mode == "bulk"
        else [raw_urls]
    )

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


def all_tasks(request):
    tasks = get_all_tasks()
    safe = {}

    for tid, data in tasks.items():
        safe[tid] = {k: v for k, v in data.items() if k != "filepath"}

    return JsonResponse(safe)


def serve_file(request, task_id):
    task = get_progress(task_id)

    if not task or task.get("status") not in ("done", "completed"):
        raise Http404("File not ready")

    filepath = task.get("filepath")
    if not filepath or not os.path.exists(filepath):
        raise Http404("File not found on server")

    filename = os.path.basename(filepath)
    task_dir = os.path.dirname(filepath)

    response = FileResponse(
        open(filepath, "rb"),
        as_attachment=True,
        filename=filename,
    )

    def cleanup():
        for _ in range(720):  # up to 2 hours
            time.sleep(10)
            try:
                if os.path.exists(task_dir):
                    shutil.rmtree(task_dir)
            except Exception:
                pass

            if not os.path.exists(task_dir):
                break

    threading.Thread(target=cleanup, daemon=True).start()
    return response


def cancel(request, task_id):
    cancel_task(task_id)
    return JsonResponse({"status": "cancelled"})


def pause(request, task_id):
    toggle_pause(task_id)
    return JsonResponse({"status": "toggled"})