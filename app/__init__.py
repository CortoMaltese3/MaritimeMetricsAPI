"""Initialization for the Flask application."""

from flask import Flask

from . import logging_config

app = Flask(__name__)
