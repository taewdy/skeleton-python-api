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
├── http/             # HTTP transport (generic)
│   ├── __init__.py
│   └── client.py     # Low-level HTTP helpers (e.g., get_json)
├── photos/           # Photos domain (business)
│   ├── __init__.py
│   ├── service.py    # Orchestration: compose gateway + mappers + validators
│   ├── gateway.py    # External API adapter (I/O only, returns raw data)
│   ├── mappers.py    # Raw -> Photo model mapping
│   └── validators.py # Domain validation hooks
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
- **Metrics** - Prometheus metrics at `/metrics`
- **Proper Error Handling** - HTTP status codes and error messages
- **Type Safety** - Full type hints and Pydantic validation

## 📋 API Endpoints

### GET /v1/photos/

Fetch photos from JSONPlaceholder API.

**Parameters:**
- `limit` (optional): Limit number of photos returned (1-5000)

**Example:**
```bash
curl -X GET "http://localhost:8000/v1/photos/?limit=3"
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

### GET /v1/photos/{photo_id}

Fetch a single photo by ID.

**Example:**
```bash
curl -X GET "http://localhost:8000/v1/photos/42"
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
   uv run uvicorn photos_api.main:app --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API Base URL: http://localhost:8000
   - Interactive Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🧪 Testing

### Manual Testing

Test the endpoints using curl:

```bash
# Test health endpoint
curl -X GET "http://localhost:8000/health"

# Test photos endpoint with limit
curl -X GET "http://localhost:8000/v1/photos/?limit=3"

# Test single photo
curl -X GET "http://localhost:8000/v1/photos/1"

# Test 404 error handling
curl -X GET "http://localhost:8000/v1/photos/9999"
```

### Metrics

If enabled, Prometheus metrics are exposed at `/metrics`.

Quick check with curl:
```
curl -s http://localhost:8000/metrics | head -n 20
```

Prometheus scrape config example:
```
scrape_configs:
  - job_name: 'photos-api'
    metrics_path: /metrics
    static_configs:
      - targets: ['localhost:8000']
```

Docker Compose target example:
```
scrape_configs:
  - job_name: 'photos-api'
    metrics_path: /metrics
    static_configs:
      - targets: ['photos-api:8000']
```

## 🔧 Configuration

### Settings and Environment Variables

Settings are managed via `pydantic-settings` with the `PHOTOS_API_` prefix, nested keys using `__`, and `.env` support.

Supported variables (defaults in parentheses):
- `PHOTOS_API_APP_NAME` ("Photos API")
- `PHOTOS_API_APP_VERSION` (package version or "0.1.0")
- `PHOTOS_API_SERVER__DEBUG` (false)
- `PHOTOS_API_SERVER__HOST` ("0.0.0.0")
- `PHOTOS_API_SERVER__PORT` (8000)
- `PHOTOS_API_SERVER__RELOAD` (true)
- `PHOTOS_API_SERVER__LOG_LEVEL` ("info")
- `PHOTOS_API_CORS__ALLOW_ORIGINS` ("*") — comma-separated list or "*"
- `PHOTOS_API_CORS__ALLOW_METHODS` ("GET") — comma-separated
- `PHOTOS_API_CORS__ALLOW_HEADERS` ("*") — comma-separated or "*"
- `PHOTOS_API_EXTERNAL__BASE_URL` ("https://jsonplaceholder.typicode.com")
- `PHOTOS_API_EXTERNAL__HTTP_TIMEOUT` (30.0)
- `PHOTOS_API_EXTERNAL__MAX_RETRIES` (2)
- `PHOTOS_API_EXTERNAL__BACKOFF_FACTOR` (0.2)
- `PHOTOS_API_LOGGING__AS_JSON` (false)

Example `.env`:
```
PHOTOS_API_SERVER__DEBUG=true
PHOTOS_API_SERVER__RELOAD=true
PHOTOS_API_SERVER__LOG_LEVEL=debug
PHOTOS_API_CORS__ALLOW_ORIGINS=http://localhost:3000,http://localhost:5173
PHOTOS_API_EXTERNAL__BASE_URL=https://jsonplaceholder.typicode.com
PHOTOS_API_EXTERNAL__HTTP_TIMEOUT=20
PHOTOS_API_EXTERNAL__MAX_RETRIES=2
PHOTOS_API_EXTERNAL__BACKOFF_FACTOR=0.2
PHOTOS_API_LOGGING__AS_JSON=true
```

### Testing Strategy

Use monkeypatching to replace domain functions in `photos.service` with fakes during tests. See `tests/test_api.py` for examples.

## 📜 Logging

- Toggle JSON logs with `PHOTOS_API_LOGGING__AS_JSON=true`.
- Control level via `PHOTOS_API_SERVER__LOG_LEVEL` (e.g. `info`, `debug`).
- Each response includes an `X-Request-ID` header; it is also logged.

Example JSON log line:
```
{"level":"info","logger":"photos_api","message":"request","time":"2025-09-06 12:00:00","request_id":"7f0a9c3e-7e2a-4b8e-9a6b-2f2d1c1b0c5f","method":"GET","path":"/v1/photos"}
```

To enable JSON logging in development:
```
export PHOTOS_API_LOGGING__AS_JSON=true
export PHOTOS_API_SERVER__LOG_LEVEL=debug
```

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

**Note:** For testing without network, override the HTTP client dependency to a fake implementation.

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
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## ✅ Success Criteria

- ✅ FastAPI service following functional organization pattern
- ✅ GET /photos endpoint with external API integration
- ✅ Proper Pydantic models matching the specified Photo struct
- ✅ Error handling and HTTP status codes
- ✅ Interactive API documentation
- ✅ Health check and root endpoints
- ✅ Type safety and validation
- ✅ Modern Python packaging with uv and pyproject.toml
