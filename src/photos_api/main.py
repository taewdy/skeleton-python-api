"""
Main entry point for the Photos API application.
"""
from dotenv import load_dotenv
import uvicorn
from photos_api.app import create_app
from photos_api.settings import get_settings

# Load environment variables from a .env file if present
load_dotenv()

# Create the FastAPI application
app = create_app()


def main() -> None:
    """Main entry point for running the application."""
    s = get_settings()
    uvicorn.run(
        "photos_api.main:app",
        host=s.server.host,
        port=s.server.port,
        reload=s.server.reload,
        log_level=s.server.log_level,
    )


if __name__ == "__main__":
    main()
