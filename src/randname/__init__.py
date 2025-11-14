"""Randname - A random name generator library.

Modules:
    config: Configuration for logging.
    core: Core functionality for generating random names.
    database: Database handling for name data.
    error: Custom exceptions for the randname library.
"""

from importlib.metadata import version

from randname.core import (
    available_countries,
    randfirst,
    randfull,
    randlast,
    show_data,
)

__title__ = "randname"
__version__ = version(__title__)
__author__ = "Adam Walkiewicz"
__license__ = "MIT"

__all__ = [
    "available_countries",
    "randfirst",
    "randfull",
    "randlast",
    "show_data",
]
