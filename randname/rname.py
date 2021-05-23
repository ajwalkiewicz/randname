import random
import json
import os
import warnings
from bisect import bisect_left
from .errors import *

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_COUNTRIES_BASE = os.listdir(os.path.join(_THIS_FOLDER, "data"))
_DEFAULT_DATABASE = os.path.join(_THIS_FOLDER, "data")

class RandName():
    def __init__(
        self,
        database=_DEFAULT_DATABASE,
        # year: int = None,
        # sex: str = None,
        # country: str = None,
        # weights: bool = True
        ):
        self.db = database
        # self.year = year
        # self.sex: sex
        # self.country: country
        # self.weights: weights

    def get_name(
        self,
        name,
        year: int = None,
        sex: str = None,
        country: str = None,
        weights: bool = True
        ) -> str:

        opt = {
            "first": "first_names",
            "last": "last_names",
        }
        name = opt.get(name)

        if not country:
            country = random.choice(_COUNTRIES_BASE)

        database_files = os.listdir(os.path.join(self.db, country, name))
        database_years = set(year.split("_")[0] for year in database_files)
        data_range = (int(min(database_years)), int(max(database_years)))

        if not year:
            year = random.randint(*data_range)

        if not min(data_range) <= year <= max(data_range):
            message = f"{year} -> {year} not in range {data_range}"
            warnings.warn(message)

        info = os.path.join(self.db, country, "info.json")
        with open(info, "r") as info:
            available_sex = json.load(info)[name]

        if sex is None:
            sex = random.choice(available_sex)

        if str(sex).capitalize() not in available_sex:
            raise InvalidSexArgument(sex, available_sex)

        # Correction of year index. If bisect_left returns int > len(data_range) return bisect_left -1
        year_index = lambda d, y: bisect_left(d, y) if bisect_left(d, y) != len(d) else bisect_left(d, y) - 1

        year = data_range[year_index(data_range, year)]
        data_set_name = f'{year}_{sex}'
        data_set_path = os.path.join(self.db, country, name, data_set_name)

        with open(data_set_path) as json_file:
            data_set = json.load(json_file)
            name_population = data_set["Names"]
            name_weights = data_set["Totals"]
            if weights:
                last_name = random.choices(name_population, cum_weights=name_weights)[0]
            else:
                last_name = random.choices(name_population)[0]
        return last_name

    # Main functions

    def get_last_name(self, year: int = None, sex: str = None, country: str = None, weights: bool = True) -> str:
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
        last_name = self.get_name("last", year, sex, country, weights)
        return last_name

    def get_first_name(self, year: int = None, sex: str = None, country: str = None, weights: bool = True) -> str:
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
        first_name = self.get_name("first", year, sex, country, weights)
        return first_name

    # Flavor functions

    def get_full_name(
        self,
        year: int = None,
        first_sex: str = None,
        last_sex: str = None,
        country: str = None,
        weights: bool = True) -> str:
        """Return random first and las name

        :param year: year of source database, defaults to None
        :type year: int, optional
        :param sex: first name gender, defaults to None
        :type sex: str, optional
        :return: full name as string
        :rtype: str

        >>> full_name()
        'John Doe'
        """
        first_name = self.get_first_name(year, first_sex, country, weights)
        last_name = self.get_last_name(year, last_sex, country, weights)
        return f"{first_name} {last_name}"

    # Support finctions

    @property
    def available_countries(self) -> list:
        """Return list of available countries

        :return: lis of available countries
        :rtype: list
        """
        return set(os.listdir(os.path.join(_THIS_FOLDER, "data")))

    @property
    def data_lookup(self) -> dict:
        """Return dictionary with imformation about database.
        {
            country_name: {
                first_names: available_sex_as_list,
                last_names: available_sex_as_list
                },
            ...
        }

        :return: information about database
        :rtype: dict
        """
        result = {}

        for country in self.available_countries:
            path_to_info_json = os.path.join(_THIS_FOLDER, "data", country, "info.json")

            with open(path_to_info_json) as info_file:
                info_dict = json.load(info_file)
                result.setdefault(
                    info_dict["country"],
                    {
                        "first_names": info_dict["first_names"],
                        "last_names": info_dict["last_names"],
                    })

        return result


if __name__ == "__main__":
    pass
    # _get_name("first_names", sex="M", country="US")
    # last_name(country="ES", sex="F")
    n = RandName()
    n.get_name("last")
