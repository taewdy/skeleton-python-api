import pytest
import httpx
from httpx import AsyncClient
from typing import List, Optional

from photos_api.app import create_app
from photos_api.models import Photo

import photos_api.photos.service as photos_service


@pytest.mark.asyncio
async def test_health_endpoint():
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["service"] == "photos-api"


@pytest.mark.asyncio
async def test_get_photos_with_limit(monkeypatch):
    async def fake_fetch_photos(limit: Optional[int] = None):
        data = [
            {"albumId": 1, "id": 1, "title": "t1", "url": "u1", "thumbnailUrl": "tu1"},
            {"albumId": 1, "id": 2, "title": "t2", "url": "u2", "thumbnailUrl": "tu2"},
            {"albumId": 1, "id": 3, "title": "t3", "url": "u3", "thumbnailUrl": "tu3"},
        ]
        if limit is not None:
            data = data[:limit]
        return [Photo(**d) for d in data]

    monkeypatch.setattr(photos_service, "fetch_photos", fake_fetch_photos)

    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/v1/photos/", params={"limit": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert set(data[0].keys()) == {"albumId", "id", "title", "url", "thumbnailUrl"}


@pytest.mark.asyncio
async def test_get_photo_by_id_success(monkeypatch):
    async def fake_fetch_photo_by_id(photo_id: int):
        assert photo_id == 42
        return Photo(
            albumId=1,
            id=42,
            title="Answer",
            url="https://example.com/42",
            thumbnailUrl="https://example.com/t42",
        )

    monkeypatch.setattr(photos_service, "fetch_photo_by_id", fake_fetch_photo_by_id)

    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/v1/photos/42")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 42


@pytest.mark.asyncio
async def test_get_photo_by_id_not_found(monkeypatch):
    async def fake_fetch_photo_by_id(photo_id: int):
        request = httpx.Request("GET", f"https://jsonplaceholder.typicode.com/photos/{photo_id}")
        response = httpx.Response(404, request=request)
        raise httpx.HTTPStatusError("Not found", request=request, response=response)

    monkeypatch.setattr(photos_service, "fetch_photo_by_id", fake_fetch_photo_by_id)

    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/v1/photos/6000")
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()
