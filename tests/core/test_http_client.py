import pytest
from unittest.mock import AsyncMock, patch

from app.core.http_client import HTTPClient, JSONPlaceholderClient


@pytest.mark.asyncio
async def test_jsonplaceholder_client_get_success():
    """Test successful GET request."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"test": "data"}
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        client = JSONPlaceholderClient()
        result = await client.get("/test")
        
        assert result == {"test": "data"}


@pytest.mark.asyncio
async def test_jsonplaceholder_client_get_with_params():
    """Test GET request with parameters."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"test": "data"}
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        client = JSONPlaceholderClient()
        result = await client.get("/test", params={"key": "value"})
        
        assert result == {"test": "data"}


@pytest.mark.asyncio
async def test_jsonplaceholder_client_get_error():
    """Test error handling in GET request."""
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        client = JSONPlaceholderClient()
        with pytest.raises(Exception):
            await client.get("/test")


@pytest.mark.asyncio
async def test_jsonplaceholder_client_close():
    """Test client cleanup."""
    mock_client = AsyncMock()
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        client = JSONPlaceholderClient()
        await client.close()
        
        mock_client.aclose.assert_called_once() 