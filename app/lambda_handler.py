from mangum import Mangum
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from app.main import app

logger = Logger()


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """Lambda handler for the FastAPI application."""
    try:
        # Create Mangum handler
        asgi_handler = Mangum(app)
        
        # Process the request
        response = asgi_handler(event, context)
        
        return response
    except Exception as e:
        logger.exception("Error processing request")
        return {
            "statusCode": 500,
            "body": {"error": "Internal server error"},
            "headers": {
                "Content-Type": "application/json",
            },
        } 