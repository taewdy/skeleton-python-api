"""Validation helpers for Photos domain.

These are lightweight placeholders. The Photo Pydantic model already
validates types and required fields; add domain-specific checks here when needed.
"""
from photos_api.photos.protocols import RawPhoto


def validate_photo_data(data: RawPhoto) -> RawPhoto:
    """Return the input data after optional domain checks.

    Example checks to add later:
    - Ensure required keys exist before mapping
    - Check ID ranges, URL formats beyond basic type checks
    """
    return data
