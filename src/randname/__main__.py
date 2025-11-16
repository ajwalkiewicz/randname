import argparse
from collections.abc import Sequence

import randname
from randname.core import Randname, available_countries, randfirst, randfull, randlast

# Remove `None` from valid choices, because there it is not easy to pass it
# in CLI, and it is not necessary, as the default is None
sex_choices = [choice for choice in Randname.VALID_SEX_OPTIONS if choice]


def parse_args(
    args: Sequence[str] | None = None,
) -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(
        prog="randname",
        description="Generate a random name using randname library.",
        add_help=False,
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

    # Utility arguments
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {randname.__version__}",
        help="Show the version of the randname library and exit.",
    )
    parser.add_argument(
        "--help", "-h", action="help", help="Show this help message and exit."
    )

    return parser.parse_args(args), parser


def main():
    args, parser = parse_args()

    if args.help:
        parser.print_help()

    if args.first:
        name = randfirst(country=args.country, sex=args.sex, year=args.year)
    elif args.last:
        name = randlast(country=args.country, sex=args.sex, year=args.year)
    else:
        name = randfull(country=args.country, sex=args.sex, year=args.year)

    print(name)


if __name__ == "__main__":
    main()
