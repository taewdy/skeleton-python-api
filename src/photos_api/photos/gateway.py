"""External API adapter for the Photos domain.

Responsible solely for I/O with the remote service and returning raw data
structures (dicts/lists). No business rules or model mapping here.
"""
from typing import Any, Dict, List

from photos_api.http.client import get_json
from photos_api.settings import get_settings
from typing import cast


async def list_photos() -> List[Dict[str, Any]]:
    s = get_settings()
    base = str(s.external.base_url).rstrip("/")
    url = f"{base}/photos"
    data = await get_json(
        url,
        timeout=s.external.http_timeout,
        max_retries=s.external.max_retries,
        backoff_factor=s.external.backoff_factor,
    )
    # Expect a list of dicts
    return data  # type: ignore[return-value]


async def get_photo(photo_id: int) -> Dict[str, Any]:
    s = get_settings()
    base = str(s.external.base_url).rstrip("/")
    url = f"{base}/photos/{photo_id}"
    data = await get_json(
        url,
        timeout=s.external.http_timeout,
        max_retries=s.external.max_retries,
        backoff_factor=s.external.backoff_factor,
    )
    # Expect a dict
    return data  # type: ignore[return-value]
