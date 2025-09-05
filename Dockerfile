FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools (if needed for deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
COPY src /app/src

RUN pip install --no-cache-dir uv && \
    uv sync --no-dev

EXPOSE 8000

ENV PHOTOS_API_SERVER__HOST=0.0.0.0 \
    PHOTOS_API_SERVER__PORT=8000 \
    PHOTOS_API_SERVER__RELOAD=false \
    PHOTOS_API_SERVER__LOG_LEVEL=info

CMD ["uv", "run", "python", "-m", "photos_api.main"]

