# Python API Backend

A modern Python API backend using FastAPI and AWS Lambda, following SOLID principles and best practices.

## Project Structure

```
.
├── app/                    # Application code
│   ├── api/               # API routes
│   ├── core/              # Core functionality
│   │   └── http_client.py # HTTP client interface and implementation
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   └── lambda_handler.py  # Lambda handler
├── tests/                 # Test files
│   ├── api/              # API endpoint tests
│   ├── core/             # Core functionality tests
│   ├── models/           # Model tests
│   └── services/         # Service layer tests
├── .github/               # GitHub Actions workflows
├── .gitignore            # Git ignore file
├── template.yaml         # SAM template
├── build_layer.sh        # Layer build script
├── pyproject.toml        # Project configuration
└── requirements.txt      # Project dependencies
```

## Python Testing Conventions

### Test Organization

Python follows a distinct testing convention that differs from some other languages (like Go). Here's why and how we organize tests:

1. **Separate Test Directory**
   - Tests are placed in a dedicated `tests/` directory at the project root
   - This follows the standard Python project structure
   - Makes it easier to exclude tests from production deployments

2. **Test File Naming**
   - Test files are prefixed with `test_`
   - Test functions are prefixed with `test_`
   - Example: `test_http_client.py`, `test_get_photos()`

3. **Test Directory Structure**
   - Mirrors the source code structure
   - Example:
     ```
     app/
     ├── api/
     │   └── photos.py
     └── core/
         └── http_client.py
     
     tests/
     ├── api/
     │   └── test_photos.py
     └── core/
         └── test_http_client.py
     ```

### Testing Tools and Practices

1. **pytest**
   - The de facto standard testing framework
   - Provides powerful fixtures and parameterization
   - Example:
     ```python
     @pytest.mark.asyncio
     async def test_get_photos():
         # Test implementation
     ```

2. **Test Categories**
   - Unit Tests: Test individual components in isolation
   - Integration Tests: Test component interactions
   - End-to-End Tests: Test the entire application flow

3. **Test Fixtures**
   - Reusable test components
   - Defined using `@pytest.fixture`
   - Example:
     ```python
     @pytest.fixture
     async def http_client():
         client = JSONPlaceholderClient()
         yield client
         await client.close()
     ```

4. **Mocking**
   - Use `unittest.mock` or `pytest-mock`
   - Isolate components for testing
   - Example:
     ```python
     @patch("app.api.photos.JSONPlaceholderClient")
     async def test_get_photos(mock_client):
         # Test with mocked client
     ```

5. **Test Coverage**
   - Use `pytest-cov` for coverage reporting
   - Aim for high coverage of critical paths
   - Example command:
     ```bash
     pytest --cov=app tests/
     ```

### Best Practices

1. **Test Independence**
   - Each test should be independent
   - Tests should not rely on the state from other tests
   - Use fixtures to set up test data

2. **Descriptive Test Names**
   - Test names should describe what's being tested
   - Include the expected outcome
   - Example: `test_get_photos_returns_empty_list_when_no_photos_exist`

3. **Test Documentation**
   - Use docstrings to explain test purpose
   - Document edge cases and assumptions
   - Example:
     ```python
     def test_photo_model_validation():
         """Test photo model validation with invalid data.
         
         This test verifies that the Photo model correctly
         validates required fields and URL formats.
         """
     ```

4. **Error Testing**
   - Test both success and error cases
   - Verify error messages and status codes
   - Example:
     ```python
     def test_invalid_url_raises_error():
         with pytest.raises(ValueError):
             Photo(url="invalid-url")
     ```

## Architecture

### Dependency Injection & SOLID Principles

The project follows SOLID principles, particularly:

1. **Single Responsibility Principle (SRP)**:
   - Each class has a single responsibility
   - `HTTPClient` handles HTTP communication
   - `PhotoService` handles business logic
   - API routes handle request/response

2. **Interface Segregation Principle (ISP)**:
   - `HTTPClient` abstract base class defines a minimal interface
   - Concrete implementations can extend functionality as needed

3. **Dependency Inversion Principle (DIP)**:
   - High-level modules depend on abstractions
   - `PhotoService` depends on `HTTPClient` interface
   - Easy to swap implementations (e.g., for testing)

### HTTP Client Pattern

The HTTP client implementation follows best practices:

1. **Abstract Interface**:
```python
class HTTPClient(ABC):
    @abstractmethod
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass
```

2. **Concrete Implementation**:
```python
class JSONPlaceholderClient(HTTPClient):
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
```

3. **Resource Management**:
```python
async def get_photo_service() -> PhotoService:
    client = JSONPlaceholderClient()
    try:
        yield PhotoService(client)
    finally:
        await client.close()
```

### Error Handling

The project implements robust error handling:

1. **HTTP Client Errors**:
```python
class HTTPClientError(Exception):
    pass

try:
    response = await self.client.get(url)
    response.raise_for_status()
except httpx.HTTPError as e:
    raise HTTPClientError(f"HTTP error occurred: {str(e)}")
```

2. **Retry Logic**:
```python
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = await self.client.get(url, params=params)
    response.raise_for_status()
    return response.json()
```

### Testing

The project uses a comprehensive testing approach:

1. **Mocking Dependencies**:
```python
@patch("app.api.photos.JSONPlaceholderClient")
async def test_get_photos(mock_client_class):
    mock_client = AsyncMock()
    mock_client.get.return_value = [...]
```

2. **Resource Cleanup**:
- FastAPI's dependency injection ensures proper cleanup
- Context managers handle resource management

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

1. Health Check:
```bash
GET /api/v1/health
```

2. Get Photos:
```bash
GET /api/v1/photos
GET /api/v1/photos?album_id=1
```

## Testing

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Linting

Run all linters:
```bash
black .
isort .
flake8
mypy .
```

## Docker

Build and run with Docker:
```bash
docker-compose up --build
```

## CI/CD

The project includes GitHub Actions for CI/CD:
- Runs on push to main and pull requests
- Tests with multiple Python versions
- Runs linting and type checking
- Generates and uploads test coverage

## Deployment

### Prerequisites

1. Install AWS SAM CLI:
```bash
pip install aws-sam-cli
```

2. Configure AWS credentials:
```bash
aws configure
```

### Local Development

1. Start the API locally:
```bash
sam local start-api
```

2. Test the API:
```bash
curl http://localhost:3000/api/v1/health
```

### Deployment to AWS

1. Build the dependencies layer:
```bash
chmod +x build_layer.sh
./build_layer.sh
```

2. Deploy using SAM:
```bash
sam build
sam deploy --guided
```

### CI/CD Pipeline

The project includes GitHub Actions for CI/CD:
- Runs on push to main and pull requests
- Tests with multiple Python versions
- Runs linting and type checking
- Generates and uploads test coverage
- Deploys to AWS Lambda on successful builds

## Lambda-Specific Features

### Cold Start Optimization

The application is optimized for Lambda cold starts:
- Minimal dependencies
- Efficient resource initialization
- Proper connection pooling

### Logging

Using AWS Lambda Powertools for structured logging:
```python
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):
    logger.info("Processing request")
```

### Error Handling

Robust error handling for Lambda environment:
```python
try:
    # Process request
except Exception as e:
    logger.exception("Error processing request")
    return {
        "statusCode": 500,
        "body": {"error": "Internal server error"}
    }
```

### Monitoring

The application includes:
- CloudWatch Logs integration
- X-Ray tracing
- Custom metrics 