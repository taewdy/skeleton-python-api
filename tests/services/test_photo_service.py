import pytest
from unittest.mock import AsyncMock, patch

from app.models.photo import Photo
from app.services.photo_service import PhotoService
from app.core.http_client import HTTPClient


@pytest.mark.asyncio
async def test_get_photos_success():
    """Test successful photo retrieval."""
    mock_client = AsyncMock()
    mock_client.get.return_value = [
        {
            "albumId": 1,
            "id": 1,
            "title": "test photo",
            "url": "https://example.com/photo.jpg",
            "thumbnailUrl": "https://example.com/thumb.jpg",
        }
    ]

    service = PhotoService(mock_client)
    photos = await service.get_photos()
    
    assert len(photos) == 1
    assert isinstance(photos[0], Photo)
    assert photos[0].title == "test photo"


@pytest.mark.asyncio
async def test_get_photos_with_album_id():
    """Test photo retrieval with album_id filter."""
    mock_client = AsyncMock()
    mock_client.get.return_value = [
        {
            "albumId": 1,
            "id": 1,
            "title": "test photo",
            "url": "https://example.com/photo.jpg",
            "thumbnailUrl": "https://example.com/thumb.jpg",
        }
    ]

    service = PhotoService(mock_client)
    photos = await service.get_photos(album_id=1)
    
    assert len(photos) == 1
    assert photos[0].album_id == 1
    mock_client.get.assert_called_with("/photos", params={"albumId": 1})


@pytest.mark.asyncio
async def test_get_photos_empty_response():
    """Test handling of empty response."""
    mock_client = AsyncMock()
    mock_client.get.return_value = []

    service = PhotoService(mock_client)
    photos = await service.get_photos()
    
    assert len(photos) == 0


@pytest.mark.asyncio
async def test_get_photos_error():
    """Test error handling in photo service."""
    mock_client = AsyncMock()
    mock_client.get.side_effect = Exception("API Error")

    service = PhotoService(mock_client)
    with pytest.raises(Exception):
        await service.get_photos() 