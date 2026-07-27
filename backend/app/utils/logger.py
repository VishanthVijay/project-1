import logging
import sys
from app.config import settings

# Define log output format
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"


def setup_logger(name: str = "habit_tracker") -> logging.Logger:
    """
    Configures and returns a standard logger instance.
    Logs are written to stdout with appropriate severity levels.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    return logger


logger = setup_logger()
