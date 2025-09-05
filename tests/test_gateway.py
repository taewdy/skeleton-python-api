import pytest
import respx
import httpx

from photos_api.photos import gateway


@pytest.mark.asyncio
@respx.mock
async def test_list_photos_success(monkeypatch):
    # Point base URL to test server
    from photos_api.settings import get_settings

    get_settings.cache_clear()  # type: ignore[attr-defined]
    s = get_settings()
    # Keep real base URL; respx intercepts absolute URL below

    route = respx.get("https://jsonplaceholder.typicode.com/photos").mock(
        return_value=httpx.Response(200, json=[{"albumId": 1, "id": 1, "title": "t", "url": "u", "thumbnailUrl": "tu"}])
    )

    data = await gateway.list_photos()
    assert route.called
    assert isinstance(data, list)
    assert data[0]["id"] == 1


@pytest.mark.asyncio
@respx.mock
async def test_get_photo_404_raises():
    route = respx.get("https://jsonplaceholder.typicode.com/photos/9999").mock(
        return_value=httpx.Response(404)
    )
    with pytest.raises(httpx.HTTPStatusError):
        await gateway.get_photo(9999)
    assert route.called

