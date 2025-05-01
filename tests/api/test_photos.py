from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.photo import Photo

client = TestClient(app)


@patch("app.api.photos.JSONPlaceholderClient")
async def test_get_photos_success(mock_client_class):
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
    mock_client_class.return_value = mock_client

    response = client.get("/api/v1/photos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "test photo"


@patch("app.api.photos.JSONPlaceholderClient")
async def test_get_photos_with_album_id(mock_client_class):
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
    mock_client_class.return_value = mock_client

    response = client.get("/api/v1/photos?album_id=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["album_id"] == 1


@patch("app.api.photos.JSONPlaceholderClient")
async def test_get_photos_error(mock_client_class):
    """Test error handling in photos endpoint."""
    mock_client = AsyncMock()
    mock_client.get.side_effect = Exception("API Error")
    mock_client_class.return_value = mock_client

    response = client.get("/api/v1/photos")
    assert response.status_code == 500
    assert "error" in response.json()


@patch("app.api.photos.JSONPlaceholderClient")
async def test_get_photos_empty_response(mock_client_class):
    """Test handling of empty response."""
    mock_client = AsyncMock()
    mock_client.get.return_value = []
    mock_client_class.return_value = mock_client

    response = client.get("/api/v1/photos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0 