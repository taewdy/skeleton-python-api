from typing import List, Optional
from ..models import Photo


class MockHTTPClient:
    """Mock HTTP client for testing when external API is not available."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
    
    async def fetch_photos(self, limit: Optional[int] = None) -> List[Photo]:
        """
        Mock fetch photos - returns sample photo data.
        
        Args:
            limit: Optional limit on number of photos to return
            
        Returns:
            List of mock Photo objects
        """
        # Sample photos data matching JSONPlaceholder API format
        mock_data = [
            {
                "albumId": 1,
                "id": 1,
                "title": "accusamus beatae ad facilis cum similique qui sunt",
                "url": "https://via.placeholder.com/600/92c952",
                "thumbnailUrl": "https://via.placeholder.com/150/92c952"
            },
            {
                "albumId": 1,
                "id": 2,
                "title": "reprehenderit est deserunt velit ipsam",
                "url": "https://via.placeholder.com/600/771796",
                "thumbnailUrl": "https://via.placeholder.com/150/771796"
            },
            {
                "albumId": 1,
                "id": 3,
                "title": "officia porro iure quia iusto qui ipsa ut modi",
                "url": "https://via.placeholder.com/600/24f355",
                "thumbnailUrl": "https://via.placeholder.com/150/24f355"
            },
            {
                "albumId": 1,
                "id": 4,
                "title": "culpa odio esse rerum omnis laboriosam voluptate repudiandae",
                "url": "https://via.placeholder.com/600/d32776",
                "thumbnailUrl": "https://via.placeholder.com/150/d32776"
            },
            {
                "albumId": 1,
                "id": 5,
                "title": "natus nisi omnis corporis facere mollitia rerum in",
                "url": "https://via.placeholder.com/600/f66b97",
                "thumbnailUrl": "https://via.placeholder.com/150/f66b97"
            }
        ]
        
        # Apply limit if specified
        if limit is not None:
            mock_data = mock_data[:limit]
        
        # Convert to Photo objects
        photos = [Photo(**photo_data) for photo_data in mock_data]
        return photos
    
    async def fetch_photo_by_id(self, photo_id: int) -> Photo:
        """
        Mock fetch a single photo by ID.
        
        Args:
            photo_id: ID of the photo to fetch
            
        Returns:
            Mock Photo object
            
        Raises:
            ValueError: If photo_id is not found (for testing 404 scenarios)
        """
        if photo_id < 1 or photo_id > 5000:
            raise ValueError(f"Photo with ID {photo_id} not found")
        
        # Generate mock data based on photo_id
        mock_data = {
            "albumId": ((photo_id - 1) // 50) + 1,
            "id": photo_id,
            "title": f"Mock photo {photo_id} - sample title for testing",
            "url": f"https://via.placeholder.com/600/mock{photo_id:04d}",
            "thumbnailUrl": f"https://via.placeholder.com/150/mock{photo_id:04d}"
        }
        
        return Photo(**mock_data)