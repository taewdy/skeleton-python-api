from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..api import photos_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Photos API",
        description="A FastAPI service for fetching photos from JSONPlaceholder API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(photos_router)
    
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
            "message": "Photos API",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/health"
        }
    
    return app