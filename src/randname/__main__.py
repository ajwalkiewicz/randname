import argparse
from collections.abc import Sequence

from randname.core import Randname, available_countries, randfirst, randfull, randlast

sex_choices = [choice for choice in Randname.VALID_SEX_OPTIONS if choice]


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a random full name using randname library."
    )

    # Mutually exclusive arguments for first name and last name
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--first",
        action="store_true",
        help="Generate and display only the first name.",
    )
    group.add_argument(
        "--last",
        action="store_true",
        help="Generate and display only the last name.",
    )

    # Optional arguments
    parser.add_argument(
        "--country",
        choices=available_countries(),
        default="US",
        help="Specify the country for name generation (default: US).",
    )
    parser.add_argument(
        "--sex",
        choices=sex_choices,
        default=None,
        help="Specify the sex for name generation (default: None).",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Specify the year for name generation (default: None).",
    )

    return parser.parse_args(args)


def main():
    args = parse_args()

    if args.first:
        name = randfirst(country=args.country, sex=args.sex, year=args.year)
    elif args.last:
        name = randlast(country=args.country, sex=args.sex, year=args.year)
    else:
        name = randfull(country=args.country, sex=args.sex, year=args.year)

    print(name)


if __name__ == "__main__":
    main()
