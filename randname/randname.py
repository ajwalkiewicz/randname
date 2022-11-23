"""
**Main module for randname**

.. todo::
    TODO P0: Write unit tests for existing code
.. todo::
    TODO P1: Refactor code and review variable names
.. todo::
    TODO P2: Add database validation function
.. todo::
    TODO P3: Move from os.path to Path

Example usage of module:

>>> import randname
>>> randname.full_name()
'John Doe'
"""
import json
import logging
import os
import random
import warnings
from bisect import bisect_left
from pathlib import Path

import randname.database
import randname.error

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_COUNTRIES_BASE = os.listdir(os.path.join(_THIS_FOLDER, "data"))
_PROPER_SEX_OPTIONS = ("M", "F", "N", None)

PATH_TO_DATABASE = Path() / _THIS_FOLDER / "data"
DATABASE: str = randname.database.Database(PATH_TO_DATABASE)._path

WARNINGS = True

randname.set_logging_level("error")

logging.debug(f"This folder: {_THIS_FOLDER}")
logging.debug(f"Countries base: {_COUNTRIES_BASE}")
logging.debug(f"Database: {DATABASE}")
logging.debug(f"Warnings: " + ("off", "on")[WARNINGS])


class Randname:
    database = randname.database.Database(DATABASE)

    @classmethod
    def full_name(cls, *args, **kwargs):
        return full_name(database=cls.database.path, *args, **kwargs)

    @classmethod
    def first_name(cls, *args, **kwargs):
        return first_name(database=cls.database.path, *args, **kwargs)

    @classmethod
    def last_name(cls, *args, **kwargs):
        return last_name(database=cls.database.path, *args, **kwargs)


def full_name(
    year: int = None,
    sex: str = None,
    country: str = None,
    weights: bool = True,
    show_warnings: bool = WARNINGS,
    database: str = DATABASE,
) -> str:
    """Return full name

    :param year: year of birth, defaults to None
    :type year: int, optional
    :param sex: sex's name, defaults to None
    :type sex: str, optional
    :param country: country of origin, defaults to None
    :type country: str, optional
    :param weights: use population distribution if True, else treat all names with same probability, defaults to True
    :type weights: bool, optional
    :param show_warnings: show warnings, defaults to WARNINGS
    :type show_warnings: bool, optional
    :param database: path to database, defaults to DATABASE
    :type database: str, optional
    :raises InvalidSexArgument: if sex is not in proper sex options
    :raises InvalidCountryName: if country is not in valid countries
    :return: full name
    :rtype: str

    >>> full_name()
    'John Doe'
    """
    country = _gen_country(country, database)
    first_name_available_sex = _available_sex(database, country, "first_names")
    last_name_available_sex = _available_sex(database, country, "last_names")

    first_name_sex = last_name_sex = sex

    if sex not in _PROPER_SEX_OPTIONS:
        raise randname.error.InvalidSexArgument(sex, _PROPER_SEX_OPTIONS)

    if sex not in first_name_available_sex:
        first_name_sex = random.choice(first_name_available_sex)

    if sex not in last_name_available_sex:
        last_name_sex = random.choice(last_name_available_sex)

    first = first_name(year, first_name_sex, country, weights, show_warnings, database)
    last = last_name(year, last_name_sex, country, weights, show_warnings, database)
    return f"{first} {last}"


def last_name(
    year: int = None,
    sex: str = None,
    country: str = None,
    weights: bool = True,
    show_warnings: bool = WARNINGS,
    database: str = DATABASE,
) -> str:
    """Return random last name

    :param year: year of birth, defaults to None
    :type year: int, optional
    :param sex: sex's name, defaults to None
    :type sex: str, optional
    :param country: country of origin, defaults to None
    :type country: str, optional
    :param weights: use population distribution if True, else treat all names with same probability, defaults to True
    :type weights: bool, optional
    :param show_warnings: show warnings, defaults to WARNINGS
    :type show_warnings: bool, optional
    :param database: path to database, defaults to DATABASE
    :type database: str, optional
    :raises InvalidSexArgument: if sex is not in proper sex options
    :raises InvalidCountryName: if country is not in valid countries
    :return: last name
    :rtype: str

    >>> last_name()
    'Doe'
    """
    last_name = _gen_name("last", year, sex, country, weights, show_warnings, database)
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

    :param year: year of birth, defaults to None
    :type year: int, optional
    :param sex: sex's name, defaults to None
    :type sex: str, optional
    :param country: country of origin, defaults to None
    :type country: str, optional
    :param weights: use population distribution if True, else treat all names with same probability, defaults to True
    :type weights: bool, optional
    :param show_warnings: show warnings, defaults to WARNINGS
    :type show_warnings: bool, optional
    :param database: path to database, defaults to DATABASE
    :type database: str, optional
    :raises InvalidSexArgument: if sex is not in proper sex options
    :raises InvalidCountryName: if country is not in valid countries
    :return: first name
    :rtype: str

    >>> first_name()
    'John'
    """
    first_name = _gen_name(
        "first", year, sex, country, weights, show_warnings, database
    )
    return first_name


def _gen_name(
    name_type: str,
    year: int = None,
    sex: str = None,
    country: str = None,
    cum_weights: bool = True,
    show_warnings: bool = WARNINGS,
    database: str = DATABASE,
) -> str:
    """Private function to get either first or last name

    :param name_type: "first" or "last"
    :type name_type: str
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

    name_type = _map_name_to_form_name(name_type)
    country = _gen_country(country, database)
    year = _gen_year(year, database, country, name_type, show_warnings)
    sex = _gen_sex(sex, database, country, name_type)

    name_of_dataset = f"{year}_{sex}"
    path_to_dataset = os.path.join(database, country, name_type, name_of_dataset)

    logging.debug(f"Year: {year}")
    logging.debug(f"Data set name: {name_of_dataset}")
    logging.debug(f"Data set path: {path_to_dataset}")

    return _gen_name_from_file(path_to_dataset, cum_weights)


def _map_name_to_form_name(name_type: str) -> str:
    opt = {
        "first": "first_names",
        "last": "last_names",
    }
    return opt.get(name_type)


def _gen_country(country: str, path_to_database: str) -> str:
    countries = list(available_countries(path_to_database))
    if not country:
        country = random.choice(countries)
    # TODO: if not countries
    if country not in countries:
        raise randname.error.InvalidCountryName(country, countries)
    return country


def _gen_year(
    year: int, database: str, country: str, name_type: str, show_warnings
) -> int:
    database_files = os.listdir(os.path.join(database, country, name_type))
    database_years = set(year.split("_")[0] for year in database_files)
    data_range = sorted([int(year) for year in database_years])

    if not year:
        year = random.choice(data_range)

    logging.debug(f"Year: {year}")

    if show_warnings:
        if not min(data_range) <= year <= max(data_range):
            message = f"{year} -> {year} not in range {data_range}"
            warnings.warn(message)

    # Correction of year index. If bisect_left returns int > len(data_range)
    # return bisect_left -1. It's in case of very small data sets.
    def correct_bisect_left(d, y):
        bisect = bisect_left(d, y)
        return bisect if bisect != len(d) else bisect - 1

    year_index = correct_bisect_left(data_range, year)
    logging.debug(f"Year index: {year_index}")

    return data_range[year_index]


def _gen_sex(sex: str, database: str, country: str, name_type: str) -> str:
    available_sex = _available_sex(database, country, name_type)

    if sex is None:
        sex = random.choice(available_sex)

    if str(sex).capitalize() not in available_sex:
        raise randname.error.InvalidSexArgument(sex, available_sex)

    return sex


def _available_sex(path_to_dataset: str, country: str, name_type: str):
    logging.debug(path_to_dataset)
    logging.debug(country)
    logging.debug(name_type)
    info = os.path.join(path_to_dataset, country, "info.json")

    with open(info, "r", encoding="utf-8") as info:
        available_sex = json.load(info)[name_type]

    logging.debug(f"Available sex: {available_sex}")
    return available_sex


def _gen_name_from_file(path_to_dataset: str, cum_weights: bool = True) -> str:
    with open(path_to_dataset, "r", encoding="utf-8") as json_file:
        logging.debug(f"Opening: {json_file.name}")
        data_set = json.load(json_file)
        name_population = data_set["Names"]
        name_cum_weights = data_set["Totals"]

    if cum_weights:
        name = random.choices(name_population, cum_weights=name_cum_weights)[0]
    else:
        name = random.choices(name_population)[0]

    logging.debug(f"Name: {name}")

    return name


# Support functions


def available_countries(path_to_database: str = DATABASE) -> set:
    """Return set of available countries

    :return: set of available countries
    :rtype: set

    >>> available_countries()
    {'ES', 'PL', 'US'}
    """
    return set(os.listdir(path_to_database))


def show_data(path_to_database: str = DATABASE) -> dict:
    """Return dictionary with information about database.

    :return: information about database
    :rtype: dict

    >>> show_data()
    {
        'ES': {'first_names': ['M'], 'last_names': ['N']},
        'PL': {'first_names': ['M', 'F'], 'last_names': ['M', 'F']},
        'US': {'first_names': ['M', 'F'], 'last_names': ['N']}
    }
    """
    result = {}

    for country in available_countries(path_to_database):
        path_to_info_json = os.path.join(path_to_database, country, "info.json")

        with open(path_to_info_json, "r", encoding="utf-8") as info_file:
            info_dict = json.load(info_file)
            result.setdefault(
                info_dict["country"],
                {
                    "first_names": info_dict["first_names"],
                    "last_names": info_dict["last_names"],
                },
            )

    return result


def validate_database(path_to_database: Path) -> bool:
    """Validate database

    :param path_to_database: path to database
    :type path_to_database: Path
    :return: True if database is valid, else False
    :rtype: bool
    """

    randname.database.Database(path_to_database)


if __name__ == "__main__":
    _gen_name("first")
    _gen_name("last")
    first_name()
    last_name()
    full_name()
