# randnames
Python module to draw random USA names.

# Summary

to be done

# Table of Contents

- [Project Title](#randnames)
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

# Installation

Randnames is availabe in python repository, and can be downloaded with pip.

```Bash
pip3 install randnames
```

# Usage

```Python
>>> import randnames

# Get first name
>>> randnames.first_name()
'John'

# Get last name
>>> randnames.last_name()
'Doe'

# Get full name
>>>randnames.full_name()
'John Doe'
```

# Documentation

Detailed documentation of module can by found here:
[randnames documentation](https://ajwalkiewicz.github.io/randnames/_build/html/index.html#)

# Database

So far project uses databases from www.census.gov and www.ssa.gov.

### Last names

Databases for USA last names: 

https://www.census.gov/topics/population/genealogy/data/1990_census.html
https://www.census.gov/topics/population/genealogy/data/2000_surnames.html
https://www.census.gov/topics/population/genealogy/data/2010_surnames.html

### first names

Database for USA first names:

https://www.ssa.gov/oact/babynames/limits.html

### license
https://www.census.gov/data/software/x13as/disclaimer.html

# Contribution
If you want to contribute to randnames projcet read [contribution](CONTRIBUTION.md) for more information.

We are especially looking for help with database creation. More information on how to help/create appropiate data files with names can be found in [database guide](DATABASE_GUIDE.md)

# Authors & Contributors

**Author**: Adam Walkiewicz

**Contributors**: Be first!

# To do

1. [ ] Summary
1. [ ] Tools
1. [ ] Contribution guideline
1. [ ] Unit tests
1. [ ] Instruction for database creation
1. [ ] Add equal chances for every name feature
1. [ ] Support for other countries names
1. [ ] Add 9 more countries 

# Change log

- PL last names added

# License

Randnames is licensed under the terms of the [MIT license](LICENSE)
