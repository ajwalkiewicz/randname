import random
import json
import os
from bisect import bisect_left
import random_names_errors as err

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

LAST_NAMES_PATH = os.path.join(THIS_FOLDER, "data", "USA", "last_names")
FIRST_NAMES_PATH = os.path.join(THIS_FOLDER, "data", "USA", "first_names")


def last_name(year=1900):
    if not year <= 2010:
        raise err.YearNotInRange(year, (None, 2010))

    data_range = (1990, 2010)
    year_index = bisect_left(data_range, year)
    
    year = data_range[year_index]
    data_set_name = f'{year}'
    data_set_path = os.path.join(LAST_NAMES_PATH, data_set_name)

    with open(data_set_path) as json_file:
        data_set = json.load(json_file)
        name_population = data_set["Names"]
        name_weights = data_set["Totals"]
        last_name = random.choices(name_population, cum_weights=name_weights)[0]
    return last_name

def first_name(year=1900, sex=None):
    if not 1880 <= year <= 2018:
        raise err.YearNotInRange(year, (1880, 2018))

    if sex is None:
        sex = random.choice(('M', 'F'))

    if sex not in ('M', 'F'):
        raise err.InvalidSexArgument(sex)

    data_set_name = f'{year}_{sex}'
    data_set_path = os.path.join(FIRST_NAMES_PATH, data_set_name)

    with open(data_set_path) as json_file:
        data_set = json.load(json_file)
        name_population = data_set["Names"]
        name_weights = data_set["Totals"]
        first_name = random.choices(name_population, cum_weights=name_weights)[0]
    return first_name


if __name__ == "__main__":
    # print(last_name())
    print(first_name())
    # print(first_name(sex="D"))
    print(first_name(year=1923))