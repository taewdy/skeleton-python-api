from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import httpx
import os

from ..models import Photo
from ..http import HTTPClient
from ..http.mock_client import MockHTTPClient

router = APIRouter(prefix="/photos", tags=["photos"])


def get_http_client():
    """Get HTTP client based on environment configuration."""
    use_mock = os.getenv("USE_MOCK_API", "false").lower() == "true"
    if use_mock:
        return MockHTTPClient()
    return HTTPClient()


@router.get("/", response_model=List[Photo])
async def get_photos(
    limit: Optional[int] = Query(None, ge=1, le=5000, description="Limit number of photos returned")
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
        http_client = get_http_client()
        photos = await http_client.fetch_photos(limit=limit)
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
        http_client = get_http_client()
        photo = await http_client.fetch_photo_by_id(photo_id)
        return photo
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Photo with ID {photo_id} not found")
        raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")
    except ValueError as e:
        # Handle mock client ValueError for 404 scenarios
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")