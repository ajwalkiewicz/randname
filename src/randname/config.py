"""Configuration for logging in the randname library.

This module act as singleton. Once imported it will not be re-imported again.
Thus, `logger` is always the same object.

Attributes:
    DEFAULT_LOGGING_LEVEL: Default logging level for the application.
    LOGGING_LEVEL_MAP: Mapping of string logging levels to logging module constants.
    logger: Configured logger instance.

Functions:
    set_logger: Set logger for the application.
"""

import logging

DEFAULT_LOGGING_LEVEL = logging.DEBUG
LOGGING_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def set_logger(level_name: str) -> logging.Logger:
    """Set logger for the application.

    Args:
        level_name: Logging level to set. Can be a string key from LOGGING_LEVEL_MAP
            or a logging level constant.

    Returns:
        logger
    """
    level = LOGGING_LEVEL_MAP.get(level_name, logging.ERROR)
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger = logging.getLogger("randname")
    logger.addHandler(handler)

    return logger


logger = set_logger("error")
