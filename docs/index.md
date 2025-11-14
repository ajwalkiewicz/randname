[![PyPI version](https://badge.fury.io/py/rname.svg)](https://badge.fury.io/py/rname)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](license.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://shields.io/)
[![Author: Walu](https://img.shields.io/badge/Aurhor-Walu-gray.svg)](https://shields.io/)

# randname

Python module to generate random name.

## Summary

Randname is a python module for generating random name - first and last. 
It uses official data from appropriate governmental/scientific research centers.

Names are drawn with the consideration of their frequency. Therefor most common 
name wil be drawn much more often (this feature can be disabled).

Currently supported countries:
US, PL, ES.

Default database is small, and constrained to 10000 records for each first and 
last names for every country. Default data size: 60 000 records

With the full database downloaded from project 
[github page](https://github.com/ajwalkiewicz/randname/), 
the amount of names is increased to around 700 000 records.

## Installation

Randname is available in python repository, and can be downloaded with pip.

```Bash
pip3 install rname
```

## Usage

```Python
>>> import randname

# Get first name
>>> randname.randfirst()
'John'

# Get last name
>>> randname.randlast()
'Doe'

# Get full name
>>>randname.randfull()
'John Doe'

# Setting directory to external database
>>> randname.database = "/path/to/external/database/"
```

## Database

Default database included in pypi package is very small. To not make the 
package unnecessary too large, every country have one set of data for last 
and first names (with distinction for the male, female, neutral name), 
for the most recent year. Each file contains up to 10000 records.

Currently supported countries:

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

Full database is bigger and doesn't have the limit of records. If you wan to 
use it, download it from project [github page](https://github.com/ajwalkiewicz/randname/).

To use other databases specify directory by setting `database_path` variable

```Python
>>> import randname
>>> randname.database = "path_to_your_database"
```

---

More details about database can be found [here](database.md)

## Contribution

If you want to contribute to randname project read 
[contribution](contribution.md) for more information.

I am looking especially for help with database creation. More information on 
how to help/create appropriate data files with names can be found in 
[database guide](database.md)

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

Randname is licensed under the terms of the [MIT license](license.md)
