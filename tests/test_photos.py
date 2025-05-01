from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.photo import Photo

client = TestClient(app)


@patch("app.api.photos.JSONPlaceholderClient")
async def test_get_photos(mock_client_class):
    # Setup mock
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

    # Test without album_id
    response = client.get("/api/v1/photos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "test photo"

    # Test with album_id
    response = client.get("/api/v1/photos?album_id=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["album_id"] == 1 