"""Initialization for the Flask application."""

from flask import Flask
from flasgger import Swagger
from config import Config
import logging

from .models import MaritimeData
from . import logging_config

app = Flask(__name__)
Swagger(app)
app.config.from_object(Config)

# Attempt to initialize MaritimeData
csv_path = app.config["CSV_PATH"]
try:
    maritime_data = MaritimeData(csv_path)
    # Make maritime_data accessible app-wide by storing it in app's config
    app.config["maritime_data"] = maritime_data
except Exception as e:
    logging.error(f"Failed to initialize MaritimeData with CSV path {csv_path}: {e}")
    # You might want to handle initialization failure here

# Import views to ensure view functions are registered with the Flask app instance
from . import views
