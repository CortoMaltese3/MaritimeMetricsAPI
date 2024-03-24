"""Initialization for the Flask application."""

from flask import Flask
from flasgger import Swagger
from config import Config
import logging

from .database import db
from . import logging_config
from .models import MaritimeData

app = Flask(__name__)
Swagger(app)
app.config.from_object(Config)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Swagger(app)

    # Initialize the database with the app
    db.init_app(app)

    # Import models and views to ensure they're registered with the app
    from .models import VesselData
    from . import views

    return app


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
