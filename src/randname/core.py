"""Core module for randname

Functions in this module are aliased to methods of an instance of the Randname
class. This allows users to call functions directly from the module without
needing to instantiate the Randname class themselves. And makes implementation
easier, because functions share internal state and resources.

To change the database path, assign a new path to `randname.core.database`
attribute.

Examples:
    Example usage of module:

    >>> import randname
    >>> randname.randfull()
    'John Doe'

Attributes:
    database: Instance of the Database class used for name data.

Functions:
    randfirst: Generate a random first name.
    randlast: Generate a random last name.
    randfull: Generate a random full name.
    available_countries: List available countries in the database.
    show_data: Show information about the database.

Classes:
    Randname: Main class for generating random names.
"""

import json
import logging
import os
import random
from bisect import bisect_left
from pathlib import Path
from typing import Literal

import randname.database
import randname.error
from randname.config import logger

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

type ShortConvention = Literal["first", "last"]
type LongConvention = Literal["first_names", "last_names"]
type SexConvention = Literal["F", "M", "N"]


class Randname:
    PATH_TO_DATABASE = Path() / _THIS_FOLDER / "data"
    VALID_SEX_OPTIONS = ("M", "F", "N", None)

    def __init__(self, path_to_database: Path | None = None):
        if path_to_database is None:
            self._database = randname.database.Database(Randname.PATH_TO_DATABASE)
        else:
            self._database = randname.database.Database(path_to_database)

        logger.debug("Database: %s", self._database)

    @property
    def database(self) -> randname.database.Database:
        return self._database

    @database.setter
    def database(self, path: Path) -> None:
        self._database = randname.database.Database(path)
        logger.debug("Database path: %s", self._database.path)

    def randfull(
        self,
        year: int | None = None,
        sex: str | None = None,
        country: str | None = None,
        weights: bool = True,
    ) -> str:
        """Return full name

        Args:
            year: Year of birth, defaults to None
            sex: Sex's name, defaults to None
            country: Country of origin, defaults to None
            weights: Use population distribution if True, else treat all names
                with same probability, defaults to True

        Returns:
            Full name

        Raises:
            InvalidSexArgument: If sex is not in proper sex options
            InvalidCountryName: If country is not in valid countries

        Examples:
            >>> randfull()
            'John Doe'
        """
        country = self._gen_country(country)
        first_name_available_sex = self._available_sex(country, "first_names")
        last_name_available_sex = self._available_sex(country, "last_names")

        first_name_sex = last_name_sex = sex

        if sex not in Randname.VALID_SEX_OPTIONS:
            raise randname.error.InvalidSexArgumentError(
                sex, Randname.VALID_SEX_OPTIONS
            )

        if sex not in first_name_available_sex:
            first_name_sex = random.choice(first_name_available_sex)

        if sex not in last_name_available_sex:
            last_name_sex = random.choice(last_name_available_sex)

        first = self.randfirst(year, first_name_sex, country, weights)
        last = self.randlast(year, last_name_sex, country, weights)
        return f"{first} {last}"

    def randlast(
        self,
        year: int | None = None,
        sex: str | None = None,
        country: str | None = None,
        weights: bool = True,
    ) -> str:
        """Return random last name

        Args:
            year: Year of birth, defaults to None
            sex: Sex's name, defaults to None
            country: Country of origin, defaults to None
            weights: Use population distribution if True, else treat all names
                with same probability, defaults to True

        Returns:
            Last name

        Raises:
            InvalidSexArgument: If sex is not in proper sex options
            InvalidCountryName: If country is not in valid countries

        Examples:
            >>> randlast()
            'Doe'
        """
        last_name = self._gen_name("last", year, sex, country, weights)
        return last_name

    def randfirst(
        self,
        year: int | None = None,
        sex: str | None = None,
        country: str | None = None,
        weights: bool = True,
    ) -> str:
        """Return random first name

        Args:
            year: Year of birth, defaults to None
            sex: Sex's name, defaults to None
            country: Country of origin, defaults to None
            weights: Use population distribution if True, else treat all names
                with same probability, defaults to True

        Returns:
            First name

        Raises:
            InvalidSexArgument: If sex is not in proper sex options
            InvalidCountryName: If country is not in valid countries

        Examples:
            >>> randfirst()
            'John'
        """
        return self._gen_name("first", year, sex, country, weights)

    def _gen_name(
        self,
        short_name: ShortConvention,
        year: int | None = None,
        sex: str | None = None,
        country: str | None = None,
        cum_weights: bool = True,
    ) -> str:
        """Private function to get either first or last name

        Args:
            name_type: "first" or "last"
            year: Year of source database, defaults to None
            sex: Name gender, defaults to None
            country: Database country, defaults to None
            cum_weights: Include weights in database, defaults to True

        Returns:
            Name from database

        Raises:
            InvalidSexArgument: Raise when provided sex is not available for
                given database

        Examples:
            >>> _gen_name("first")
            "John"
            >>> _gen_name("last")
            "Doe"
        """
        long_name = Randname._map_short_to_full_convention(short_name)
        country = self._gen_country(country)
        year = self._gen_year(year, country, long_name)
        sex = self._gen_sex(sex, country, long_name)

        name_of_dataset = f"{year}_{sex}"
        path_to_dataset = self.database.path / country / long_name / name_of_dataset

        return Randname._gen_name_from_file(path_to_dataset, cum_weights)

    @staticmethod
    def _map_short_to_full_convention(
        short: ShortConvention,
    ) -> LongConvention:
        opt: dict[ShortConvention, LongConvention] = {
            "first": "first_names",
            "last": "last_names",
        }
        result = opt.get(short)

        if result is None:
            raise ValueError("Incorrect key")

        return result

    def _gen_country(self, country: str | None) -> str:
        countries = list(self.available_countries())
        if country is None:
            country = random.choice(countries)
        # TODO: if not countries
        if country not in countries:
            raise randname.error.InvalidCountryNameError(country, countries)
        return country

    def _gen_year(
        self,
        year: int | None,
        country: str,
        name_type: str,
    ) -> int:
        database_files = list((self._database.path / country / name_type).iterdir())
        database_years = set(year.name.split("_")[0] for year in database_files)
        data_range = sorted([int(year) for year in database_years])

        if not year:
            year = random.choice(data_range)

        logging.debug(f"Year: {year}")

        if not min(data_range) <= year <= max(data_range):
            logger.warning("%s -> %s not in range %s", year, year, data_range)

        # Correction of year index. If bisect_left returns int > len(data_range)
        # return bisect_left -1. It's in case of very small data sets.
        def correct_bisect_left(d, y):
            bisect = bisect_left(d, y)
            return bisect if bisect != len(d) else bisect - 1

        year_index = correct_bisect_left(data_range, year)
        logging.debug(f"Year index: {year_index}")

        return data_range[year_index]

    def _gen_sex(self, sex: str | None, country: str, name_type: str) -> str:
        available_sex = self._available_sex(country, name_type)

        if sex is None:
            sex = random.choice(available_sex)

        if str(sex).capitalize() not in available_sex:
            raise randname.error.InvalidSexArgumentError(sex, available_sex)

        return sex

    def _available_sex(self, country: str, name_type: str):
        info = self._database.path / country / "info.json"

        with info.open("r", encoding="utf-8") as fd:
            available_sex = json.load(fd)[name_type]

        logging.debug("Available sex: %s", available_sex)

        return available_sex

    @staticmethod
    def _gen_name_from_file(path_to_dataset: Path, cum_weights: bool = True) -> str:
        with path_to_dataset.open("r", encoding="utf-8") as json_file:
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

    def available_countries(self, path: Path | None = None) -> set[str]:
        """Return set of available countries

        Args:
            path: Path to database, defaults to DATABASE

        Returns:
            Set of available countries

        Examples:
            >>> available_countries()
            {'ES', 'PL', 'US'}
        """
        if path is None:
            path = self._database.path

        return {p.name for p in path.iterdir()}

    def show_data(
        self, path: Path | None
    ) -> dict[str, dict[LongConvention, list[SexConvention]]]:
        """Return dictionary with information about database.

        Args:
            path: Path to the root directory of database.

        Returns:
            Information about database

        Examples:
            >>> show_data()
            {
                'ES': {'first_names': ['M'], 'last_names': ['N']},
                'PL': {'first_names': ['M', 'F'], 'last_names': ['M', 'F']},
                'US': {'first_names': ['M', 'F'], 'last_names': ['N']}
            }
        """
        result: dict[str, dict[LongConvention, list[SexConvention]]] = {}

        if path is None:
            path = self.database.path

        for country in self.available_countries(path):
            path_to_info_json = path / country / "info.json"

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


# Create one instance of Randname
# Alias module-level functions to the instance methods
# This is similar approach as seen in libraries like 'random' or 'numpy'
# It allows users to call functions directly from the module without
# needing to instantiate the Randname class themselves.
# At the same time it makes implementation easier, because functions share
# internal state and resources.

_inst = Randname()

database = _inst.database

randfirst = _inst.randfirst
randlast = _inst.randlast
randfull = _inst.randfull

available_countries = _inst.available_countries
show_data = _inst.show_data
