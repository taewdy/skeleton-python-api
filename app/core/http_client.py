from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import httpx


class HTTPClient(ABC):
    """Abstract base class for HTTP clients."""
    
    @abstractmethod
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the specified URL."""
        pass


class JSONPlaceholderClient(HTTPClient):
    """HTTP client for JSONPlaceholder API."""
    
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the specified URL."""
        response = await self.client.get(f"{self.base_url}{url}", params=params)
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose() 