# Database Guide

## Legal warning

Please kep in mind that randname is an open source project and we relay only 
on legally possessed data.

## How database looks

All data files are stored in `data` directory.

`data` directory contains directories for every currently supported country. 
Country directories are named accordingly to [Aplha-2 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements). 
It means that directory name is exactly 2 capital letters.

Inside country directory there are 2 separate directories and 1 info.json file. 
One for first names and one for las names.
 
* `first_names`
* `last_names`

`info.json` file contain information about stored date in country directory.
For example:
```JSON
{
    "country": "US",
    "first_names": ["M", "F"],
    "last_names": ["N"]
}
```
Above `info.json` file contain following information:
- country: US
- 2 first names files, one with male names and the other one with female names
- 1 last name file with neutral last names

Inside names directories, are actual data files.

Data files are in [JSON](https://en.wikipedia.org/wiki/JSON) format, 
but without `.json` extension.

Data files has to starts from `year`, `underscore`, and `gender capital letter` 
- `M`, `F` or `N`. Example: `1990_M` for male names in 1990.

### What letter to use?

Not all languages have same names grammar. For example english language have 
same form of last name regardless the gender. In the other hand some languages 
like polish have separate last names forms for male and female.

Use:
* `M` - for male
* `F` - for female
* `N` - when there is no distinction for male and female.

### Example:

```
randname/data/
├── ES
│   ├── first_names
│   │   └── 2020_M
│   ├── info.json
│   └── last_names
│       └── 2020_N
├── PL
│   ├── first_names
│   │   ├── 2021_F
│   │   └── 2021_M
│   ├── info.json
│   └── last_names
│       ├── 2020_F
│       └── 2020_M
└── US
    ├── first_names
    │   ├── 2018_F
    │   └── 2018_M
    ├── info.json
    └── last_names
        └── 2010_N
```

## Names file structure

```JSON
{
    "Names": ["John", "Michael", "etc.."],
    "Totals": [5, 9, ...],
}

```

## Source files

Most of the databases with names are in `.csv` or `.xlsx` formats.

When contributing pleas send also a source file from which you are creating 
JSON data.

## Tools

In `/tools` you can find simple python scrip that can help you to create JSON 
files from `.xlsx` or `.csv` files.

In order to make it work out of the box, a source file has to have the following 
structure:
* contains 2 columns
* first column has to be with names
* second column has to be with integer numbers that indicates the number name 
occurrences.

### Example source file

| Names             | Totals |
|-------------------|--------|
| NOWAK             | 143437 |
| KOWALSKI          | 92540  |
| WIŚNIEWSKI        | 72658  |
| WÓJCIK            | 65836  |
| KOWALCZYK         | 64736  |
|<- snip ->         |        | 
| ŽUK-OLSZEWSKI     | 2      |
| ŽUKOVSKI          | 2      |
| ŽUKOVSKIJ         | 2      |
| ŽVIRBLIS          | 2      |
| ŽYBORT            | 2      |

### Example usage

```
python3 convert_to_json.py -t csv -f PL/first_names/Imiona_nadane_wPolsce_w_latach_2000-2019.csv -o 2000_M
```

## Sources

US 

Last names

https://www.census.gov/topics/population/genealogy/data/1990_census.html https://www.census.gov/topics/population/genealogy/data/2000_surnames.html https://www.census.gov/topics/population/genealogy/data/2010_surnames.html

First names

PL

Last names

First names

ES

Last names

First names

https://www.ssa.gov/oact/babynames/limits.html

## Licenses
US: https://www.census.gov/data/software/x13as/disclaimer.html

PL:

ES:


