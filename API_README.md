# Photos API

A FastAPI service that fetches photos from the JSONPlaceholder API, built following Python best practices and functional organization patterns.

## 🏗️ Architecture

This project follows the **functional organization pattern** recommended for Python web applications, where code is organized by what it does rather than abstract architectural layers.

### Project Structure

```
src/photos_api/
├── api/              # FastAPI endpoints and routing
│   ├── __init__.py
│   └── photos.py     # Photos endpoints
├── app/              # FastAPI application factory
│   ├── __init__.py
│   └── factory.py    # App creation and configuration
├── http/             # HTTP clients and utilities
│   ├── __init__.py
│   ├── client.py     # Real HTTP client for external API
│   └── mock_client.py # Mock client for testing
├── models/           # Pydantic data models
│   ├── __init__.py
│   └── photo.py      # Photo model definition
├── __init__.py
└── main.py          # Application entry point
```

## 🚀 Features

- **GET /photos/** - Fetch all photos with optional limit parameter
- **GET /photos/{photo_id}** - Fetch a single photo by ID
- **GET /health** - Health check endpoint
- **GET /** - Root endpoint with API information
- **Interactive API Documentation** - Available at `/docs`
- **Mock Mode** - For testing when external API is unavailable
- **Proper Error Handling** - HTTP status codes and error messages
- **Type Safety** - Full type hints and Pydantic validation

## 📋 API Endpoints

### GET /photos/

Fetch photos from JSONPlaceholder API.

**Parameters:**
- `limit` (optional): Limit number of photos returned (1-5000)

**Example:**
```bash
curl -X GET "http://localhost:8001/photos/?limit=3"
```

**Response:**
```json
[
  {
    "albumId": 1,
    "id": 1,
    "title": "accusamus beatae ad facilis cum similique qui sunt",
    "url": "https://via.placeholder.com/600/92c952",
    "thumbnailUrl": "https://via.placeholder.com/150/92c952"
  }
]
```

### GET /photos/{photo_id}

Fetch a single photo by ID.

**Example:**
```bash
curl -X GET "http://localhost:8001/photos/42"
```

**Response:**
```json
{
  "albumId": 1,
  "id": 42,
  "title": "Mock photo 42 - sample title for testing",
  "url": "https://via.placeholder.com/600/mock0042",
  "thumbnailUrl": "https://via.placeholder.com/150/mock0042"
}
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) for dependency management

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd /path/to/skeleton-python-api
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Run the application:**
   ```bash
   # For production (connects to real JSONPlaceholder API)
   uv run uvicorn src.photos_api.main:app --host 0.0.0.0 --port 8001
   
   # For testing with mock data (recommended)
   USE_MOCK_API=true uv run uvicorn src.photos_api.main:app --host 0.0.0.0 --port 8001
   ```

4. **Access the API:**
   - API Base URL: http://localhost:8001
   - Interactive Documentation: http://localhost:8001/docs
   - Health Check: http://localhost:8001/health

## 🧪 Testing

### Manual Testing

Test the endpoints using curl:

```bash
# Test health endpoint
curl -X GET "http://localhost:8001/health"

# Test photos endpoint with limit
curl -X GET "http://localhost:8001/photos/?limit=3"

# Test single photo
curl -X GET "http://localhost:8001/photos/1"

# Test 404 error handling
curl -X GET "http://localhost:8001/photos/9999"
```

### Using the Test Script

```bash
uv run python test_api.py
```

## 🔧 Configuration

### Environment Variables

- `USE_MOCK_API`: Set to `"true"` to use mock data instead of external API (useful for testing)

### Mock Mode

When `USE_MOCK_API=true`, the API uses locally generated mock data that matches the JSONPlaceholder API format. This is useful for:
- Testing without network connectivity
- Development environments
- CI/CD pipelines
- Demonstrations

## 📚 Data Model

### Photo

```python
class Photo(BaseModel):
    album_id: int = Field(..., alias="albumId")
    id: int
    title: str
    url: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
```

**Example:**
```json
{
  "albumId": 1,
  "id": 1,
  "title": "accusamus beatae ad facilis cum similique qui sunt",
  "url": "https://via.placeholder.com/600/92c952",
  "thumbnailUrl": "https://via.placeholder.com/150/92c952"
}
```

## 🏃‍♂️ Development

### Adding New Endpoints

1. Add new route functions to `src/photos_api/api/photos.py`
2. Update the router imports in `src/photos_api/api/__init__.py`
3. Include the router in `src/photos_api/app/factory.py`

### Adding New Models

1. Create new model classes in `src/photos_api/models/`
2. Export them in `src/photos_api/models/__init__.py`

### Code Quality

The project is configured with:
- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking

Run code quality checks:
```bash
uv run black src/
uv run isort src/
uv run mypy src/
```

## 🌐 External API Integration

This service integrates with the JSONPlaceholder API (https://jsonplaceholder.typicode.com/photos) which provides fake JSON data for testing and prototyping.

**Note:** If you encounter network connectivity issues, use the mock mode by setting `USE_MOCK_API=true`.

## 🎯 Production Considerations

For production deployment:

1. **Security**: Configure CORS origins properly in `src/photos_api/app/factory.py`
2. **Environment**: Use proper environment variables for configuration
3. **Logging**: Implement structured logging
4. **Monitoring**: Add health checks and metrics
5. **Performance**: Consider caching for frequently requested data
6. **Rate Limiting**: Implement rate limiting for external API calls

## 🧾 Dependencies

See `pyproject.toml` for the complete list of dependencies:

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **httpx**: Async HTTP client for external API calls
- **Pydantic**: Data validation using Python type annotations
- **python-dotenv**: Environment variable management

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## ✅ Success Criteria

- ✅ FastAPI service following functional organization pattern
- ✅ GET /photos endpoint with external API integration
- ✅ Proper Pydantic models matching the specified Photo struct
- ✅ Error handling and HTTP status codes
- ✅ Mock mode for testing without external dependencies
- ✅ Interactive API documentation
- ✅ Health check and root endpoints
- ✅ Type safety and validation
- ✅ Modern Python packaging with uv and pyproject.toml