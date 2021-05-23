#!/usr/bin/python3
"""[summary]
Convert xlsx to json file compiant with randname module
"""
import pandas as pd
import numpy as np
import os
import json
import argparse

DESCRIPTION = """
xlsx to jason tool

Example: ./xlsx_to_json -f example_data.xlsx -o example_output
"""

EPILOG = """
Report bugs to aj.walkiewicz@gmail.com
Copyright (C) 2021 Adam Walkiewicz
"""

NAMES = "Names"
TOTALS = "Totals"
COUNT = 10000

def valid_dataframe(df) -> bool:
    """Validate dataframe

    :param df: dataframe
    :type df: pandas.core.frame.DataFrame
    :return: return True if valid. Else False
    :rtype: bool
    """

    if len(df.columns) != 2:
        return False

    return True


def modify_dataframe_names(df):
    df.columns = [NAMES, TOTALS]
    df[NAMES] = df[NAMES].apply(lambda name: str(name).title())

def convert_weights_to_cumulative(df):
    df["Totals"] = np.cumsum(df["Totals"])

def save_to_json(df, output_file: str):
    temp_dict = {
        NAMES: tuple(df[NAMES].head(COUNT)),
        TOTALS: tuple(df[TOTALS].head(COUNT))
        }

    with open(output_file, "w") as json_file:
        json.dump(temp_dict, json_file, ensure_ascii=False)

def parse_arguments():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(DESCRIPTION),
        epilog=(EPILOG)
    )
    parser.add_argument(
        "-t",
        "--type",
        required=True,
        type=str
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="path to xlsx file"
    )
    parser.add_argument(
        "-w",
        "--cum_weights",
        required=False,
        default=True,
        action="store_false",
        help="disable cumulative weights"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        default=False,
        type=str
    )
    return parser.parse_args()

def main():

    args = parse_arguments()

    # validate data exist

    file_type = {
        "csv": pd.read_csv,
        "xlsx": pd.read_excel
    }

    if args.type not in file_type.keys():
        return False
    else:
        df = file_type[args.type](args.file, usecols=[0, 1])

    # df = pd.read_excel(args.file)

    if not valid_dataframe(df):
        return False

    modify_dataframe_names(df)

    convert_weights_to_cumulative(df)

    if args.output:
        output_file = args.output
    else:
        output_file = args.file + "_out"

    save_to_json(df, output_file=output_file)

if __name__ == "__main__":
    main()

