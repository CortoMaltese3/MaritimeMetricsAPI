"""Initialization for the Flask application."""

from flask import Flask

# Import your configuration object
from config import Config
# Import your logging configuration
from . import logging_config

# Create the Flask application instance
app = Flask(__name__)
# Apply configurations from the Config object
app.config.from_object(Config)

# Import views to ensure view functions are registered with the Flask app
from . import views
