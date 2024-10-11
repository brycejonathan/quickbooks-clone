import json
import logging
from app.main import app
from mangum import Mangum

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Lambda handler
handler = Mangum(app)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        response = handler(event, context)
        logger.info(f"Response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }
