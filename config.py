"""Configuration module for Flask application settings."""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class for Flask application settings.

    Loads settings from environment variables to allow dynamic configuration.
    Includes paths and operational flags like debug mode.

    Attributes:
        CSV_PATH (str): Path to the CSV file with vessel data.
        DEBUG (bool): Enables debug mode based on the "DEBUG" environment variable.
    """

    CSV_PATH = "data/vessel_data.csv"
    ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv("DEBUG", "True")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
