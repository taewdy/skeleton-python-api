from typing import List, Optional

from fastapi import APIRouter, Depends

from app.models.photo import Photo
from app.services.photo_service import PhotoService
from app.core.http_client import JSONPlaceholderClient

router = APIRouter()


async def get_photo_service() -> PhotoService:
    """Dependency injection for PhotoService."""
    client = JSONPlaceholderClient()
    try:
        yield PhotoService(client)
    finally:
        await client.close()


@router.get("/photos", response_model=List[Photo])
async def get_photos(
    album_id: Optional[int] = None,
    photo_service: PhotoService = Depends(get_photo_service),
) -> List[Photo]:
    """
    Get photos from JSONPlaceholder API.
    
    Args:
        album_id: Optional album ID to filter photos by.
        photo_service: Injected photo service.
        
    Returns:
        List of photos.
    """
    return await photo_service.get_photos(album_id) 