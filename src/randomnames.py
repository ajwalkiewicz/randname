#!/usr/bin/python3
import random
import json
import os
from bisect import bisect_left
from name_errors import InvalidSexArgument

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

LAST_NAMES_PATH = os.path.join(THIS_FOLDER, "lastNames.json")
FIRST_NAMES_PATH = os.path.join(THIS_FOLDER, "firstNames.json")


def last_name(year=1900):
    population = [1900, 1910, 1920, 1990, 2010]
    year_index = bisect_left(population, year)
    variable_year = population[year_index]
    variable_name = f'{variable_year}'

    with open(LAST_NAMES_PATH) as json_file:
        json_variable_name = json.load(json_file)[variable_name]
        name_population = json_variable_name["Names"]
        name_weights = json_variable_name["Totals"]
        last_name = random.choices(name_population, cum_weights=name_weights)[0]
    return last_name

def first_name(year=1900, sex=None):
    if year < 1880:
        year = 1880

    if sex is None:
        sex = random.choice(['M', 'F'])

    if sex not in ['M', 'F']:
        raise InvalidSexArgument(sex)

    variable_name = f'{year}_{sex}'

    with open(FIRST_NAMES_PATH) as json_file:
        json_variable_name = json.load(json_file)[variable_name]
        name_population = json_variable_name["Names"]
        name_weights = json_variable_name["Totals"]
        first_name = random.choices(name_population, cum_weights=name_weights)[0]
    return first_name


if __name__ == "__main__":
    # print(last_name())
    print(first_name())
    # print(first_name(sex="D"))
    print(first_name(year=1923))