# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies (including ffmpeg for yt-dlp)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the project code
COPY . /app/

# Create media directory if it doesn't exist
RUN mkdir -p /app/media

# Expose port 8000
EXPOSE 8000

# Run gunicorn
CMD ["bash", "-lc", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 --workers 3 ytdownloader.wsgi:application"]

