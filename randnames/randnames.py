"""Main module for randnames

>>> import randomnames
>>> randomnames.full_name()
'John Doe'
"""

import random
import json
import os
from bisect import bisect_left

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
COUNTRIES_BASE = os.listdir(os.path.join(THIS_FOLDER, "data"))

LAST_NAMES_PATH = os.path.join(THIS_FOLDER, "data", "USA", "last_names")
FIRST_NAMES_PATH = os.path.join(THIS_FOLDER, "data", "USA", "first_names")

class InvalidSexArgument(Exception):
    """Invalid Sex Argument

    :param Exception: Exception
    :type Exception: Exception
    """
    def __init__(self, sex: str):
        self.sex = sex
        self.message = f"{self.sex} not in ['M', 'F']"
        super().__init__(self.message)

class YearNotInRange(Exception):
    """Year not in valid range

    :param Exception: [description]
    :type Exception: [type]
    """

    def __init__(self, year: int, _range: list):
        self.year = year
        self._range = _range
        self.message = f"{self.year} not in {self._range}"
        super().__init__(self.message)

def last_name(year: int = None, country: str = False, weights: bool = True) -> str:
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
    country = "USA" # Temporary fix untill dataset preparation

    if not country:
        country = random.choice(COUNTRIES_BASE)

    database_files = os.listdir(os.path.join(THIS_FOLDER, "data", country, "last_names"))
    data_range = (int(min(database_files)), int(max(database_files)))

    if not year:
        year = random.randint(*data_range)

    # if not year <= 2010:
    #     raise YearNotInRange(year, (None, 2010))

    # year_index = bisect_left(data_range, year)
    # Correction of year index. If bisect_left returns int > len(data_range) return bisect_left -1
    year_index = lambda d, y: bisect_left(d, y) if bisect_left(d, y) != len(d) else bisect_left(d, y) - 1

    year = data_range[year_index(data_range, year)]
    data_set_name = f'{year}'
    data_set_path = os.path.join(THIS_FOLDER, "data", country, "last_names", data_set_name)

    with open(data_set_path) as json_file:
        data_set = json.load(json_file)
        name_population = data_set["Names"]
        name_weights = data_set["Totals"]
        if weights:
            last_name = random.choices(name_population, cum_weights=name_weights)[0]
        else:
            last_name = random.choices(name_population)[0]
    return last_name

def first_name(year: int = None, sex: str = None) -> str:
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
    if not year:
        year = random.randint(1880, 2018)

    if not 1880 <= year <= 2018:
        raise YearNotInRange(year, (1880, 2018))

    if sex is None:
        sex = random.choice(('M', 'F'))

    if str(sex).capitalize() not in ('M', 'F'):
        raise InvalidSexArgument(sex)

    data_set_name = f'{year}_{sex.capitalize()}'
    data_set_path = os.path.join(FIRST_NAMES_PATH, data_set_name)

    with open(data_set_path) as json_file:
        data_set = json.load(json_file)
        name_population = data_set["Names"]
        name_weights = data_set["Totals"]
        first_name = random.choices(name_population, cum_weights=name_weights)[0]
    return first_name

def full_name(year: int = None, sex: str = None) -> str:
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
    return f"{first_name(year, sex)} {last_name(year)}"