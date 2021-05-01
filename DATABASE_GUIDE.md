# Database Guide

## Legal warning
Please kep in minf that randnames is an opensource project and we relay only on legally possesed data.

## How database looks
All data files are stored in `data` directory.

`data` directory contains direcotries for every currently supported country. Country directories are named acordingly to [Aplha-2 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements). It means that direcotry name is exactly 2 capital letters.

Inside country directory there are 2 separate direcotries. One for first names and the other for las names.
* `first_names`
* `last_names`

Inside names diractories, are actuall data files.

Data files are in [JSON](https://en.wikipedia.org/wiki/JSON) format, but without `.json` extension.

Data files has to starts from `year`, `underscore`, and `gender capital letter` - `M`, `F` or `N`. Example: `1990_M` for male names in 1990.

### What letter to use?

Not all languages have same names gramar. For example english language have same form of last name regardles to gender. In the other hand some languages like polish have separate last names forms for male and female. Therefore last

Use:
* `M` - for male
* `F` - for female
* `N` - when there is no distinction for male and female.

```
N is not supported yet. It's support is planned in version 0.1.0
```

### Example:
```
.
├── PL
│   ├── first_names
│   └── last_names
│       └── 2021_N
└── US
    ├── first_names
    │   ├── 1880_F
    │   ├── 1880_M
<- snip ->
    │   ├── 2018_F
    │   └── 2018_M
    └── last_names
        ├── 1990_N
        └── 2010_N

```

## JSON file structure

```JSON
{
    "Names": ["John", "Michael", "etc.."],
    "Totals": [5, 9, 10],
}

```

## Source files
Most of the databases with names are in `.csv` or `.xlsx` formats.

When contributing pleas send also a source file from which you are creating JSON data.

## Tools

In `/tools` you can find simple python scrip that can help you to create JSON files from `.xlsx` or `.csv` files.

In odrer to make it work out of the box, a source file has to have the followng structure:
* contains 2 columns
* first column has to be with names
* second column has to be with integer nu,bers that indicates the number name occurences.

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


