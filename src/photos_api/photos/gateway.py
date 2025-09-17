"""External API adapter for the Photos domain."""
from __future__ import annotations

from typing import List, cast

from photos_api.http.client import get_json
from photos_api.photos.protocols import RawPhoto
from photos_api.settings import get_settings


async def list_photos() -> List[RawPhoto]:
    """Fetch raw photo payloads from the configured external service."""

    settings = get_settings()
    base = str(settings.external.base_url).rstrip("/")
    url = f"{base}/photos"
    data = await get_json(
        url,
        timeout=settings.external.http_timeout,
        max_retries=settings.external.max_retries,
        backoff_factor=settings.external.backoff_factor,
    )
    return cast(List[RawPhoto], data)


async def get_photo(photo_id: int) -> RawPhoto:
    """Fetch a single raw photo payload from the configured external service."""

    settings = get_settings()
    base = str(settings.external.base_url).rstrip("/")
    url = f"{base}/photos/{photo_id}"
    data = await get_json(
        url,
        timeout=settings.external.http_timeout,
        max_retries=settings.external.max_retries,
        backoff_factor=settings.external.backoff_factor,
    )
    return cast(RawPhoto, data)


__all__ = ["list_photos", "get_photo"]
