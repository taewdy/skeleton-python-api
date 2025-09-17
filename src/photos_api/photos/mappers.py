"""Mapping helpers: raw external data -> domain models."""

from photos_api.models import Photo
from photos_api.photos.protocols import RawPhoto


def photo_from_raw(data: RawPhoto) -> Photo:
    """Convert raw dict (external API shape) into a Photo model.

    Relies on Pydantic field aliases to handle `albumId` and `thumbnailUrl`.
    """
    return Photo(**data)
