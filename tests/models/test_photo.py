import pytest

from app.models.photo import Photo


def test_photo_model_creation():
    """Test creating a photo model with valid data."""
    photo = Photo(
        album_id=1,
        id=1,
        title="Test Photo",
        url="https://example.com/photo.jpg",
        thumbnail_url="https://example.com/thumb.jpg",
    )
    
    assert photo.album_id == 1
    assert photo.id == 1
    assert photo.title == "Test Photo"
    assert photo.url == "https://example.com/photo.jpg"
    assert photo.thumbnail_url == "https://example.com/thumb.jpg"


def test_photo_model_validation():
    """Test photo model validation."""
    # Test with missing required fields
    with pytest.raises(ValueError):
        Photo(
            album_id=1,
            id=1,
            title="Test Photo",
            url="https://example.com/photo.jpg",
            # Missing thumbnail_url
        )

    # Test with invalid URL format
    with pytest.raises(ValueError):
        Photo(
            album_id=1,
            id=1,
            title="Test Photo",
            url="not-a-url",
            thumbnail_url="https://example.com/thumb.jpg",
        )


def test_photo_model_json():
    """Test photo model JSON serialization."""
    photo = Photo(
        album_id=1,
        id=1,
        title="Test Photo",
        url="https://example.com/photo.jpg",
        thumbnail_url="https://example.com/thumb.jpg",
    )
    
    json_data = photo.model_dump()
    assert json_data == {
        "album_id": 1,
        "id": 1,
        "title": "Test Photo",
        "url": "https://example.com/photo.jpg",
        "thumbnail_url": "https://example.com/thumb.jpg",
    } 