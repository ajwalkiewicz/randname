# randname
Python module to generate random name.

# Summary

Randname is a python module for generating random name - first and last. It uses official data from appropiate governmant/scientific reserch centers. 

Names are drawn with the consideration of their frequency. Therefor moste common name wil be drawn much more often (this feature can be disabled).

Currently supported cuntries:
US, PL, ES.

Default database is small, and constrained to 10000 records for each first and last names for every country.
Default data size: 60 000 records

With the full database downloaded from project [github page](https://github.com/ajwalkiewicz/randname/), the amount of names is increased to around 700 000 records.

# Installation

```Bash
pip3 install rname
```

# Simple Usage

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
```

# Documentation

Detailed documentation of module can by found here:
[randname documentation](https://ajwalkiewicz.github.io/randname/_build/html/index.html#)

# Database

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

Full database is bigger and doesn't have the limit of records. If you wan to use it, dowload it from project [github page](https://github.com/ajwalkiewicz/randname/).

More detail about database can be found [here](DATABASE.md)

# Contribution
If you want to contribute to randname projcet read [contribution](CONTRIBUTION.md) for more information.

I am looking especially for help with database creation. More information on how to help/create appropiate data files with names can be found in [database guide](DATABASE.md)

# Authors & Contributors

**Author**: Adam Walkiewicz

**Contributors**: Be first!

# License

Randname is licensed under the terms of the [MIT license](LICENSE)