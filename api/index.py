from flask import Flask, request
from api.hello_world.index import hello_world_bp  # Add this import
import os
import logging

# Configure logging based on environment
if os.environ.get('VERCEL_ENV'):
    # On Vercel, just log to console which will be captured by Vercel's logging system
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )
else:
    # In development, keep file logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('flask_app.log', mode='w')
        ]
    )

# Get the root logger and set its level
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Create a logger specific to your app
logger = logging.getLogger(__name__)

# Set third-party loggers to INFO level
logging.getLogger('pinecone').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logging.getLogger('neo4j').setLevel(logging.INFO)


app = Flask(__name__)


# Add this before request handler to log all requests
@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

# Add this after request handler to log all responses
@app.after_request
def log_response_info(response):
    logger.debug('Response: %s', response.get_data())
    return response

app.register_blueprint(hello_world_bp)  # Add this line