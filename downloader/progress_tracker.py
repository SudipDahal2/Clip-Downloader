# downloader/progress_tracker.py

import uuid
from threading import Lock

# =====================================
# In-memory task storage
# =====================================
TASKS = {}
task_lock = Lock()


# =====================================
# Create New Download Task
# =====================================
def create_task(task_id, title="Unknown", thumbnail=""):
    """
    Creates a new download task with given task_id, title, and thumbnail.
    Called from views.py which supplies its own UUID.
    """
    with task_lock:
        TASKS[task_id] = {
            "status": "queued",
            "percent": "0%",
            "speed": "",
            "eta": "",
            "cancelled": False,
            "paused": False,
            "title": title,
            "thumbnail": thumbnail,
        }


# =====================================
# Update Progress
# =====================================
def set_progress(task_id, data):
    with task_lock:
        if task_id in TASKS:
            TASKS[task_id].update(data)


# =====================================
# Get Progress (single task)
# =====================================
def get_progress(task_id):
    with task_lock:
        return TASKS.get(task_id, {"status": "not_found"})


# =====================================
# Get ALL Tasks (for UI refresh endpoint)
# =====================================
def get_all_tasks():
    with task_lock:
        # Return a shallow copy so the lock isn't held during JSON serialization
        return {task_id: dict(data) for task_id, data in TASKS.items()}


# =====================================
# Cancel Task
# =====================================
def cancel_task(task_id):
    with task_lock:
        if task_id in TASKS:
            TASKS[task_id]["cancelled"] = True
            TASKS[task_id]["status"] = "cancelled"


# =====================================
# Pause / Resume Toggle
# =====================================
def toggle_pause(task_id):
    with task_lock:
        if task_id in TASKS:
            current = TASKS[task_id]["paused"]
            TASKS[task_id]["paused"] = not current
            TASKS[task_id]["status"] = "paused" if not current else "downloading"


# =====================================
# Check if Cancelled (used by downloader)
# =====================================
def is_cancelled(task_id):
    with task_lock:
        task = TASKS.get(task_id)
        if task:
            return task.get("cancelled", False)
        return False


# =====================================
# Check if Paused (used by downloader)
# =====================================
def is_paused(task_id):
    with task_lock:
        task = TASKS.get(task_id)
        if task:
            return task.get("paused", False)
        return False