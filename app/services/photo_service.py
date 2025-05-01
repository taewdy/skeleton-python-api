from typing import List, Optional

from app.core.http_client import HTTPClient
from app.models.photo import Photo


class PhotoService:
    """Service for handling photo-related operations."""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
    
    async def get_photos(self, album_id: Optional[int] = None) -> List[Photo]:
        """
        Get photos from JSONPlaceholder API.
        
        Args:
            album_id: Optional album ID to filter photos by.
            
        Returns:
            List of Photo objects.
        """
        params = {"albumId": album_id} if album_id else None
        response = await self.http_client.get("/photos", params=params)
        return [Photo(**photo) for photo in response] 