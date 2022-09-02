# __init__.py
import logging

__title__ = "randname"
__version__ = "0.3.3"
__author__ = "Adam Walkiewicz"
__license__ = "MIT"

DEFAULT_LOGGING_LEVEL = logging.DEBUG

LOGGING_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

logging_level = DEFAULT_LOGGING_LEVEL


def set_logging_level(logging_level=logging_level):
    logging_level = LOGGING_LEVEL_MAP.get(logging_level)
    return logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
        level=logging_level,
    )


from randname.randname import *
