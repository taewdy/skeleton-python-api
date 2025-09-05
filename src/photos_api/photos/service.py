from typing import List, Optional

from photos_api.models import Photo
from photos_api.photos import gateway, mappers, validators


async def fetch_photos(limit: Optional[int] = None) -> List[Photo]:
    """Orchestrate listing photos: fetch raw, validate, map to models.

    The optional limit is applied at the service layer.
    """
    raw_list = await gateway.list_photos()
    if limit is not None:
        raw_list = raw_list[:limit]
    validated = [validators.validate_photo_data(item) for item in raw_list]
    return [mappers.photo_from_raw(item) for item in validated]


async def fetch_photo_by_id(photo_id: int) -> Photo:
    """Orchestrate fetching a single photo by id."""
    raw = await gateway.get_photo(photo_id)
    validated = validators.validate_photo_data(raw)
    return mappers.photo_from_raw(validated)
