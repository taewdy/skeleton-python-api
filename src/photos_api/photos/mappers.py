"""Mapping helpers: raw external data -> domain models."""
from typing import Dict, Any

from photos_api.models import Photo


def photo_from_raw(data: Dict[str, Any]) -> Photo:
    """Convert raw dict (external API shape) into a Photo model.

    Relies on Pydantic field aliases to handle `albumId` and `thumbnailUrl`.
    """
    return Photo(**data)

