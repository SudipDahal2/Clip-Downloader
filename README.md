# YTGrab

YTGrab is a clean, modern web application that allows you to download audio (MP3) or video (MP4) from YouTube. It features a beautiful, responsive UI with real-time download progress tracking, and supports downloading multiple videos simultaneously.

![YT Grab Screenshot](docs/screenshot.png) *(Note: Placeholder for actual screenshot)*

## Features

- **High-Quality Downloads**: Uses `yt-dlp` to fetch the highest quality audio (MP3, 192k) or combined video+audio (MP4) formats.
- **Single & Bulk Modes**: Download a single link or add multiple links dynamically in an intuitive interface.
- **Real-Time Progress**: See the download progress, speed, and ETA for each file live.
- **Privacy Focused**: Files are temporarily downloaded into isolated server folders and automatically cleaned up 5 seconds after they are served to your browser. No files are kept permanently on the server.
- **Pause & Cancel**: Control your active downloads directly from the UI.
- **Beautiful UI**: Modern, typography-driven, and grain-textured design with smooth CSS micro-animations.

---

## Prerequisites

Before running the app, ensure you have the following installed on your system:

1. **Python 3.8+**: The backend is built with Django.
2. **FFmpeg**: Required by `yt-dlp` for extracting audio and merging video/audio formats.
   - **Windows**: Download [FFmpeg builds](https://gyan.dev/ffmpeg/builds/) or use `winget install ffmpeg`. Ensure the `ffmpeg` executable is in your system's PATH.
   - **macOS**: `brew install ffmpeg`
   - **Linux (Ubuntu/Debian)**: `sudo apt install ffmpeg`

---

## How to Run Locally

Follow these steps to spin up the local development server:

### 1. Clone or Download the Project

Navigate to your workspace directory and open a terminal:

```bash
cd /path/to/downloader
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to run the project inside an isolated Python virtual environment.

**Windows (PowerShell/CMD):**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

All required packages (Django, yt-dlp, etc.) are listed in `requirements.txt`. With your virtual environment activated, run:

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

Set up the initial SQLite database required by Django:

```bash
python manage.py migrate
```

### 5. Start the Development Server

Start the Django local server:

```bash
python manage.py runserver
```

### 6. Open the Application

Open your web browser and go to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## How It Works

### 1. Form Submission (Frontend)
When you submit the form (single or bulk), an asynchronous `POST` request is sent to the `/start/` endpoint. The server responds immediately with a list of generated `task_id`s. The frontend uses these IDs to spawn progress cards.

### 2. Download Execution (Backend)
For every `task_id`, the backend spins up a background thread running `download_media` from `youtube_downloader.py`.
- A temporary folder is created in `media/downloads/<task_id>/`.
- `yt-dlp` processes the URL. Its `progress_hook` is leveraged to capture real-time updates (percent, ETA, speed).
- These updates are saved into a thread-safe `progress_tracker.py` dictionary.

### 3. Real-Time Polling
While tasks are active, the frontend browser polls the `/tasks/` endpoint every 1 second. It checks the live status dictionary and updates the progress bars and text on the UI smoothly.

### 4. Serving and Cleanup
When a download finishes, a **"↓ Save file"** button appears. Clicking it requests the `/serve/<task_id>/` URL.
- Django's `FileResponse` streams the file from the server directory natively down to the user's local disk as an attachment.
- Immediately after opening the file for streaming, a daemon thread is started on the server which sleeps for 5 seconds (to allow the stream to finish) and then completely deletes the `media/downloads/<task_id>/` folder, ensuring no storage leaks.
