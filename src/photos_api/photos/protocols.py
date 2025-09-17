"""Contracts for Photos domain dependencies."""
from __future__ import annotations

from typing import Protocol, Sequence, TypedDict


class RawPhoto(TypedDict):
    """Shape of the raw photo payload returned by the external API."""

    albumId: int
    id: int
    title: str
    url: str
    thumbnailUrl: str


class PhotosGateway(Protocol):
    """Protocol describing the behaviour required from a photos gateway."""

    async def list_photos(self) -> Sequence[RawPhoto]:
        """Return a collection of raw photo payloads."""

    async def get_photo(self, photo_id: int) -> RawPhoto:
        """Return a single raw photo payload looked up by identifier."""
