from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from photos_api.api import photos_router
from photos_api.settings import get_settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="A FastAPI service for fetching photos from JSONPlaceholder API",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.server.debug,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins(),
        allow_credentials=True,
        allow_methods=settings.cors.methods(),
        allow_headers=settings.cors.headers(),
    )
    
    # Include routers under API version prefix
    app.include_router(photos_router, prefix="/v1")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict:
        """Health check endpoint."""
        return {"status": "healthy", "service": "photos-api"}
    
    # Root endpoint
    @app.get("/")
    async def root() -> dict:
        """Root endpoint with API information."""
        return {
            "message": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/health",
        }

    # Exception handlers (centralized)
    import httpx
    from fastapi.responses import JSONResponse

    @app.exception_handler(httpx.HTTPError)
    async def httpx_error_handler(_, exc: httpx.HTTPError):
        return JSONResponse(status_code=502, content={"detail": f"External API error: {str(exc)}"})

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    # Request ID middleware and simple request logging
    import uuid
    import logging
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response

    logger = logging.getLogger("photos_api")

    class RequestIDMiddleware(BaseHTTPMiddleware):
        def __init__(self, app, header_name: str = "X-Request-ID"):
            super().__init__(app)
            self.header_name = header_name

        async def dispatch(self, request: Request, call_next) -> Response:
            request_id = request.headers.get(self.header_name, str(uuid.uuid4()))
            logger.info(
                "request",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                },
            )
            response = await call_next(request)
            response.headers[self.header_name] = request_id
            return response

    app.add_middleware(RequestIDMiddleware)

    # Configure logging format (JSON optional)
    try:
        import json
        import sys

        root_logger = logging.getLogger()
        # Avoid duplicating handlers on reload
        if not root_logger.handlers:
            handler = logging.StreamHandler(sys.stdout)

            if settings.logging.as_json:
                class JsonFormatter(logging.Formatter):
                    def format(self, record: logging.LogRecord) -> str:
                        payload = {
                            "level": record.levelname.lower(),
                            "logger": record.name,
                            "message": record.getMessage(),
                            "time": self.formatTime(record, self.datefmt),
                        }
                        for key in ("request_id", "method", "path"):
                            if hasattr(record, key):
                                payload[key] = getattr(record, key)
                        return json.dumps(payload)

                handler.setFormatter(JsonFormatter())
            else:
                handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

            root_logger.addHandler(handler)
            root_logger.setLevel(getattr(logging, settings.server.log_level.upper(), logging.INFO))
    except Exception:
        # If logging configuration fails, continue with defaults
        pass

    # Metrics instrumentation
    try:
        from prometheus_fastapi_instrumentator import Instrumentator

        Instrumentator().instrument(app).expose(app, endpoint="/metrics")
    except Exception:
        # Metrics optional; ignore if dependency missing in certain environments
        pass

    return app
