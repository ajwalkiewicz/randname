[![PyPI version](https://badge.fury.io/py/rname.svg)](https://badge.fury.io/py/rname)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://shields.io/)
[![Author: Walu](https://img.shields.io/badge/Aurhor-Walu-gray.svg)](https://shields.io/)

# randname

Python module to generate random name.

## Summary

Randname is a python module for generating random name - first and last. It uses official data from appropiate governmant/scientific reserch centers.

Names are drawn with the consideration of their frequency. Therefor moste common name wil be drawn much more often (this feature can be disabled).

Currently supported cuntries:
US, PL, ES.

Default database is small, and constrained to 10000 records for each first and last names for every country.
Default data size: 60 000 records

With the full database downloaded from project [github page](https://github.com/ajwalkiewicz/randname/), the amount of names is increased to around 700 000 records.

## Table of Contents

- [Project Title](#randname)
- [Summary](#summary)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Database](#database)
- [Contribution](#contribution)
- [Authors & Contributors](#authors-&-contributors)
- [To Do](#to-do)
- [License](#license)

## Installation

Randnames is availabe in python repository, and can be downloaded with pip.

```Bash
pip3 install rname
```

## Usage

```Python
>>> import randname

# Get name
>>> randname.get_name("first")
'John'
>>> randname.get_name("last")
'Doe'

# Get first name
>>> randname.first_name()
'John'

# Get last name
>>> randname.last_name()
'Doe'

# Get full name
>>>randname.full_name()
'John Doe'

# Setting dirrection to external database
>>> randname.database_path = "/path/to/external/database/"
```

## Documentation

Detailed documentation of module can by found here:
[randname documentation](https://ajwalkiewicz.github.io/randname/_build/html/index.html#)

## Database

Default database included in pypi package is very small. To not make the package unnecessary too large, every country have one set of data for last and first names (with distinction for the male, female, neutral name), for the most recent year. Each file contains up to 10000 records.

Currently supprted countries:

US:

- 2010, last names (neutral)
- 2018, first names (male, female)

PL:

- 2020, last names (male, female)
- 2021, first names (male, female)

ES:

- 2020, last names (male)
- 2020, first names (male)

### Biger database

Full database is bigger and doesn't have the limit of records. If you wan to use it, dowload it from project [github page](https://github.com/ajwalkiewicz/randname/).

To use other databases specify directory by setting `database_path` variable

```Python
>>> import randnames
>>> randnames.database_path = "path_to_your_database"
```

---

More details about database can be found [here](DATABASE.md)

## Contribution

If you want to contribute to randname projcet read [contribution](CONTRIBUTION.md) for more information.

I am looking especially for help with database creation. More information on how to help/create appropiate data files with names can be found in [database guide](DATABASE.md)

## Authors & Contributors

**Author**: Adam Walkiewicz

**Contributors**: Be first!

## To do

1. [x] Summary
1. [ ] Tools
1. [ ] Contribution guideline
1. [ ] Unit tests
1. [ ] Instruction for database creation
1. [x] Add equal chances for every name
1. [ ] Support for other countries names
1. [ ] Add 9 more countries

## License

Randnames is licensed under the terms of the [MIT license](LICENSE)
