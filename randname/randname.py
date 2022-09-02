"""Main module for randnames

Simple usage:
>>> import randomname
>>> randoname.full_name()
'John Doe'
"""
import json
import logging
import os
import random
import warnings
from bisect import bisect, bisect_left

import randname

from .errors import *

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_COUNTRIES_BASE = os.listdir(os.path.join(_THIS_FOLDER, "data"))

DATABASE = os.path.join(_THIS_FOLDER, "data")
WARNINGS = True

randname.set_logging_level("error")

logging.debug(f"This folder: {_THIS_FOLDER}")
logging.debug(f"Countries base: {_COUNTRIES_BASE}")
logging.debug(f"Database: {DATABASE}")
logging.debug(f"Warnings: " + ("off", "on")[WARNINGS])


def _get_name(
    name: str,
    year: int = None,
    sex: str = None,
    country: str = None,
    weights: bool = True,
    show_warnings: bool = WARNINGS,
    database: str = DATABASE,
) -> str:
    """Private function to get either first or last name

    :param name: "first_name" or "last_name"
    :type name: str
    :param year: year of source database, defaults to None
    :type year: int, optional
    :param sex: name gender, defaults to None
    :type sex: str, optional
    :param country: database country, defaults to None
    :type country: str, optional
    :param weights: include weights in database, defaults to True
    :type weights: bool, optional
    :raises InvalidSexArgument: raise when provided sex is not available for given database
    :return: name from database
    :rtype: str

    >>> _get_name("first")
    "John"
    >>> _get_name("last")
    "Doe"
    """

    logging.debug(f"Database: {database}")
    logging.debug(f"Warnings: " + ("OFF", "ON")[show_warnings])

    opt = {
        "first": "first_names",
        "last": "last_names",
    }
    name = opt.get(name)

    if not country:
        country = random.choice(_COUNTRIES_BASE)

    database_files = os.listdir(os.path.join(database, country, name))
    database_years = set(year.split("_")[0] for year in database_files)
    data_range = sorted([int(year) for year in database_years])

    if not year:
        year = random.choice(data_range)
    logging.debug(f"Year: {year}")

    if show_warnings:
        if not min(data_range) <= year <= max(data_range):
            message = f"{year} -> {year} not in range {data_range}"
            warnings.warn(message)

    info = os.path.join(database, country, "info.json")
    with open(info, "r") as info:
        available_sex = json.load(info)[name]
        logging.debug(f"Available sex: {available_sex}")

    if sex is None:
        sex = random.choice(available_sex)

    if str(sex).capitalize() not in available_sex:
        raise InvalidSexArgument(sex, available_sex)

    # Correction of year index. If bisect_left returns int > len(data_range)
    # return bisect_left -1. It's in case of very small data sets.
    def correct_bisect_left(d, y):
        bisect = bisect_left(d, y)
        return bisect if bisect != len(d) else bisect - 1

    year_index = correct_bisect_left(data_range, year)
    logging.debug(f"Year index: {year_index}")

    year = data_range[year_index]
    data_set_name = f"{year}_{sex}"
    data_set_path = os.path.join(database, country, name, data_set_name)

    logging.debug(f"Year: {year}")
    logging.debug(f"Data set name: {data_set_name}")
    logging.debug(f"Data set path: {data_set_path}")

    with open(data_set_path) as json_file:
        logging.debug(f"Opening: {json_file.name}")
        data_set = json.load(json_file)
        name_population = data_set["Names"]
        name_weights = data_set["Totals"]
        if weights:
            name = random.choices(name_population, cum_weights=name_weights)[0]
        else:
            name = random.choices(name_population)[0]

    logging.debug(f"Name: {name}")
    return name


# Main functions


def last_name(
    year: int = None,
    sex: str = None,
    country: str = None,
    weights: bool = True,
    show_warnings: bool = WARNINGS,
    database: str = DATABASE,
) -> str:
    """Return random last name

    :param year: year of source database, defaults to None
    :type year: int, optional
    :param country: select database country, defaults to False
    :type country: str, optional
    :raises YearNotInRange: throw error if year is not in valid range
    :return: last name as string
    :rtype: str

    >>> last_name()
    'Doe'
    """
    last_name = _get_name("last", year, sex, country, weights, show_warnings, database)
    return last_name


def first_name(
    year: int = None,
    sex: str = None,
    country: str = None,
    weights: bool = True,
    show_warnings: bool = WARNINGS,
    database: str = DATABASE,
) -> str:
    """Return random first name

    :param year: year of source database, defaults to None
    :type year: int, optional
    :param sex: first name gender, defaults to None
    :type sex: str, optional
    :raises YearNotInRange: If year is not in valid range
    :raises InvalidSexArgument: If invalid sex argument
    :return: first name as string
    :rtype: str

    >>> first_name()
    'John'
    """
    first_name = _get_name(
        "first", year, sex, country, weights, show_warnings, database
    )
    return first_name


# Flavor functions


def full_name(
    year: int = None,
    first_sex: str = None,
    last_sex: str = None,
    country: str = None,
    weights: bool = True,
    show_warnings: bool = WARNINGS,
    database: str = DATABASE,
) -> str:
    """Return full name

    :param year: year of the birth, defaults to None
    :type year: int, optional
    :param first_sex: sex for the first name, defaults to None
    :type first_sex: str, optional
    :param last_sex: sex for the last name, defaults to None
    :type last_sex: str, optional
    :param country: country of origin, defaults to None
    :type country: str, optional
    :param weights: use population distribution if True, else treat all names with same probability, defaults to True
    :type weights: bool, optional
    :param show_warnings: show warnings, defaults to WARNINGS
    :type show_warnings: bool, optional
    :param database: path to database, defaults to DATABASE
    :type database: str, optional
    :return: full name
    :rtype: str

     >>> full_name()
    'John Doe'
    """
    # TODO: refactor full name to have just one sex parameter
    first = first_name(year, first_sex, country, weights, show_warnings, database)
    last = last_name(year, last_sex, country, weights, show_warnings, database)
    return f"{first} {last}"


# Support functions


def available_countries() -> set:
    """Return set of available countries

    :return: set of available countries
    :rtype: set

    >>> available_countries()
    {'ES', 'PL', 'US'}
    """
    return set(os.listdir(os.path.join(_THIS_FOLDER, "data")))


def data_lookup() -> dict:
    """Return dictionary with imformation about database.

    :return: information about database
    :rtype: dict

    >>> data_lookup()
    {
        'ES': {'first_names': ['M'], 'last_names': ['N']},
        'PL': {'first_names': ['M', 'F'], 'last_names': ['M', 'F']},
        'US': {'first_names': ['M', 'F'], 'last_names': ['N']}
    }
    """
    result = {}

    for country in available_countries():
        path_to_info_json = os.path.join(_THIS_FOLDER, "data", country, "info.json")

        with open(path_to_info_json) as info_file:
            info_dict = json.load(info_file)
            result.setdefault(
                info_dict["country"],
                {
                    "first_names": info_dict["first_names"],
                    "last_names": info_dict["last_names"],
                },
            )

    return result


if __name__ == "__main__":
    _get_name("first")
    _get_name("last")
    first_name()
    last_name()
    full_name()

"""
.. todolist::

    [ ] P1: Refactor code and review variable names
    [ ] P1: Move from os.path to Path
    [ ] P2: Add database validation function
    [ ] P2: Change warnings to logging module
"""
