"""Randname - A random name generator library.

This package provides functionality for generating random names from various
countries. It includes utilities for generating first names, last names, and
full names, with support for multiple countries and customizable options.

The package offers a simple API for generating random names that can be used in
testing, data generation, or any application requiring random name generation.

!!! warning
    This package uses pseudo-random generators from Python standard library.
    This package should not be used for security purposes.
    The base package contains limited dataset of names. It is easy to create
    a collision.

Attributes:
    __title__ (str): The title of the package.
    __version__ (str): The current version of the package.
    __author__ (str): The author of the package.
    __license__ (str): The license under which the package is distributed.

Examples:
    >>> import randname
    >>> randname.randfirst()
    'John'
    >>> randname.randlast()
    'Smith'
    >>> randname.randfull()
    'Jane Doe'
    >>> randname.available_countries()
    ['PL', 'US', 'ES', ...]


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

__title__ = "rname"
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
