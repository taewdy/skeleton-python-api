import asyncio
import random
import httpx
from typing import Any, Dict, Optional, Iterable


DEFAULT_TIMEOUT = 30.0


async def get_json(
    url: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = 0,
    backoff_factor: float = 0.2,
    retry_statuses: Optional[Iterable[int]] = None,
) -> Any:
    """Perform a GET request with optional retries and return parsed JSON.

    Retries on connect/read errors and selected 5xx status codes.
    """
    if retry_statuses is None:
        retry_statuses = (502, 503, 504)

    attempt = 0
    while True:
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, params=params)
                # Retry on configured 5xx statuses
                if response.status_code in retry_statuses:
                    response.raise_for_status()
                response.raise_for_status()
                return response.json()
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError, httpx.HTTPStatusError) as exc:
            if attempt >= max_retries:
                raise
            # exponential backoff with jitter
            sleep_for = backoff_factor * (2 ** attempt) + random.uniform(0, backoff_factor)
            attempt += 1
            await asyncio.sleep(sleep_for)
