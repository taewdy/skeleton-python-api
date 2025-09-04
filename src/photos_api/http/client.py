import httpx
from typing import List, Optional
from ..models import Photo


class HTTPClient:
    """HTTP client for making requests to external APIs."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
    
    async def fetch_photos(self, limit: Optional[int] = None) -> List[Photo]:
        """
        Fetch photos from JSONPlaceholder API.
        
        Args:
            limit: Optional limit on number of photos to return
            
        Returns:
            List of Photo objects
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = "https://jsonplaceholder.typicode.com/photos"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Apply limit if specified
            if limit is not None:
                data = data[:limit]
            
            # Convert to Photo objects
            photos = [Photo(**photo_data) for photo_data in data]
            return photos
    
    async def fetch_photo_by_id(self, photo_id: int) -> Photo:
        """
        Fetch a single photo by ID from JSONPlaceholder API.
        
        Args:
            photo_id: ID of the photo to fetch
            
        Returns:
            Photo object
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = f"https://jsonplaceholder.typicode.com/photos/{photo_id}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            return Photo(**data)