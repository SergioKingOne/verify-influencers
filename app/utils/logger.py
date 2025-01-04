import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger(app):
    """Configure logging for the application"""

    # Clear existing handlers first
    app.logger.handlers.clear()

    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Set the basic logging level
    app.logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # Setup file handler (rotating log files)
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10240000, backupCount=10  # 10MB
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Add handlers to the app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    return app.logger
