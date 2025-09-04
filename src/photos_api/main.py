"""
Main entry point for the Photos API application.
"""
import uvicorn
from .app import create_app

# Create the FastAPI application
app = create_app()


def main() -> None:
    """Main entry point for running the application."""
    uvicorn.run(
        "photos_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()