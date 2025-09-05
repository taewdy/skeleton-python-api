from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import httpx

from photos_api.models import Photo
from photos_api.photos import fetch_photos as fetch_photos_service, fetch_photo_by_id as fetch_photo_by_id_service

router = APIRouter(prefix="/photos", tags=["photos"])


@router.get("/", response_model=List[Photo])
async def get_photos(
    limit: Optional[int] = Query(None, ge=1, le=5000, description="Limit number of photos returned"),
) -> List[Photo]:
    """
    Fetch photos from JSONPlaceholder API.
    
    Args:
        limit: Optional limit on number of photos to return (1-5000)
        
    Returns:
        List of photos
        
    Raises:
        HTTPException: If external API request fails
    """
    try:
        photos = await fetch_photos_service(limit=limit)
        return photos
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{photo_id}", response_model=Photo)
async def get_photo_by_id(photo_id: int) -> Photo:
    """
    Fetch a single photo by ID from JSONPlaceholder API.
    
    Args:
        photo_id: ID of the photo to fetch
        
    Returns:
        Photo object
        
    Raises:
        HTTPException: If photo not found or external API request fails
    """
    try:
        photo = await fetch_photo_by_id_service(photo_id)
        return photo
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Photo with ID {photo_id} not found")
        raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
