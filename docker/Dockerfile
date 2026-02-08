FROM python:3.13-slim

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# System deps (add git, curl, etc. as needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (cache-friendly)
COPY backend/requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Default command can be overridden by docker-compose
CMD ["bash"]
