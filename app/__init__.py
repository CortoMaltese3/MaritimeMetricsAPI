"""Initialization for the Flask application."""

from flask import Flask
from flasgger import Swagger

# Import configurations and logging
from config import Config
from . import logging_config

# Create the Flask application instance
app = Flask(__name__)
# Initialize Swagger
swagger = Swagger(app)
# Apply configurations from the Config object
app.config.from_object(Config)

# Import views to ensure view functions are registered with the Flask app
from . import views
