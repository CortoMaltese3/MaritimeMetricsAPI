"""Logging configuration for the application.

This module defines a logging configuration class used to set up application-wide logging. 
It configures both console and file logging, including setting the log level, format, 
and the file log's destination.
"""

import logging
import logging.handlers


class LogConfig:
    """Configures application logging.

    This class encapsulates the configuration for logging across the application. It sets up
    logging to output both to the console and to a specified log file, with predefined
    formats and levels for each.

    Attributes:
        LOG_FORMAT (str): The format for log messages.
        DATE_FORMAT (str): The date format for log messages.
        LOG_FILE (str): The path to the log file.
        LOG_LEVEL_CONSOLE (int): The logging level for console output.
        LOG_LEVEL_FILE (int): The logging level for file output.
    """

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOG_FILE = "logs/app.log"
    LOG_LEVEL_CONSOLE = logging.INFO
    LOG_LEVEL_FILE = logging.WARNING

    @staticmethod
    def setup_logging():
        """Sets up the application-wide logging configuration.

        Configures the root logger to output messages to the console and a file, `app.log`,
        by default. The console output level is set to INFO, and the file output level
        is set to WARNING. Both outputs use a common format that includes the timestamp,
        log level, and message.

        Exception Handling:
            Handles any IOError exceptions (e.g., file access permissions) that might occur
            when setting up the file handler.
        """
        # Configure root logger
        logging.basicConfig(
            level=LogConfig.LOG_LEVEL_CONSOLE,
            format=LogConfig.LOG_FORMAT,
            datefmt=LogConfig.DATE_FORMAT,
        )

        try:
            # Create and configure file handler
            file_handler = logging.FileHandler(LogConfig.LOG_FILE)
            file_handler.setLevel(LogConfig.LOG_LEVEL_FILE)
            file_handler.setFormatter(logging.Formatter(LogConfig.LOG_FORMAT))
            logging.getLogger("").addHandler(file_handler)
        except IOError as e:
            logging.error("Failed to configure file handler for logging: %s", e)


LogConfig.setup_logging()
