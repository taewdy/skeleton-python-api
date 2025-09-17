from __future__ import annotations

from typing import List, Optional

from photos_api.models import Photo
from photos_api.photos import gateway as photos_gateway
from photos_api.photos import mappers, validators
from photos_api.photos.protocols import PhotosGateway


async def fetch_photos(limit: Optional[int] = None, *, photo_gateway: PhotosGateway | None = None) -> List[Photo]:
    """Orchestrate listing photos: fetch raw, validate, map to models.

    The optional limit is applied at the service layer.
    """
    if photo_gateway is None:
        raw_list = await photos_gateway.list_photos()
    else:
        raw_list = await photo_gateway.list_photos()
    if limit is not None:
        raw_list = raw_list[:limit]
    validated = [validators.validate_photo_data(item) for item in raw_list]
    return [mappers.photo_from_raw(item) for item in validated]


async def fetch_photo_by_id(photo_id: int, *, photo_gateway: PhotosGateway | None = None) -> Photo:
    """Orchestrate fetching a single photo by id."""
    if photo_gateway is None:
        raw = await photos_gateway.get_photo(photo_id)
    else:
        raw = await photo_gateway.get_photo(photo_id)
    validated = validators.validate_photo_data(raw)
    return mappers.photo_from_raw(validated)
