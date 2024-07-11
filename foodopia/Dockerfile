# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /foodopia

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    gettext \
    pkg-config \
    gcc \
    libffi-dev \
    libc-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Add and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install gunicorn with gevent separately to debug installation issues
RUN pip install --no-cache-dir gunicorn[gevent]

# Copy project
COPY . /foodopia/

# Expose port 8000 to the host
EXPOSE 8000

# Ensure the start script is executable
RUN chmod +x /foodopia/bin/docker_start.sh

# Start the Django application
ENTRYPOINT ["/foodopia/bin/docker_start.sh"]
