"""**Database module**"""
import json
import logging
from pathlib import Path
from typing import Union, List

import jsonschema

import randname.error

from . import set_logging_level

set_logging_level("error")


class Database:
    schema_info_json = {
        "type": "object",
        "title": "info.json schema",
        "description": "Schema for info.json file",
        "properties": {
            "country": {"type": "string"},
            "first_names": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "last_names": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        },
        "required": ["country", "first_names", "last_names"],
        "additionalProperties": False,
    }
    schema_name_json = {
        "type": "object",
        "title": "first_names and last_names schema",
        "description": "Schema for last and first names files",
        "properties": {
            "Names": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "Totals": {"type": "array", "items": {"type": "number"}, "minItems": 1},
        },
        "required": ["Names", "Totals"],
        "additionalProperties": False,
    }

    draft_validator_info = jsonschema.Draft7Validator(schema_info_json)
    draft_validator_name = jsonschema.Draft7Validator(schema_name_json)

    def __init__(self, path_to_database: Union[Path, str]):
        """Database container

        :param path_to_database: path to directory with database
        :type path_to_database: Union[Path, str]
        """
        # self.validate_database(path_to_database)
        self._path = Path(path_to_database)

    @property
    def path(self) -> Path:
        """Path to database

        :return: path to database
        :rtype: Path
        """
        return self._path

    @path.setter
    def path(self, new_path: Union[Path, str]) -> None:
        self.validate(new_path)
        self._path = Path(new_path)

    def validate(self, path_to_database: Union[Path, str] = None) -> None:
        """Check if database has valid structure and it's files are
        correctly formatted.

        ..warning::
            Validating database might take some time, depends how large is the database.

        :param path_to_database: path to database
        :type path_to_database: Union[Path, str]
        :raises randname.error.DirectoryDoesNotExist: raise when directory with database does not exist.
        :raises randname.error.MissingInfoFile: raise when info.json is missing.
        :raises randname.error.GenderMismatch: raise when gender information in info.json does not match to what is in directories.
        :raises randname.error.FileNameDoesNotMatchPattern: raise when file with names doesn't mach naming convention.
        :raises jsonschema.ValidationError: raise when json file doesn't match pattern.
        """
        invalid_name_pattern = []
        invalid_json_files = []

        if path_to_database:
            path = Path() / path_to_database
        else:
            path = self._path

        if not path.is_dir():
            raise randname.error.DirectoryDoesNotExist(path)

        # traverse directory
        for country_directory in path.iterdir():
            path_to_info_file = Path() / country_directory / "info.json"
            first_names_dir = Path() / country_directory / "first_names"
            last_names_dir = Path() / country_directory / "last_names"

            # check for required files
            if not path_to_info_file.exists():
                raise randname.error.MissingInfoFile(path_to_info_file)
            if not first_names_dir.exists():
                raise randname.error.DirectoryDoesNotExist(first_names_dir)
            if not last_names_dir.exists():
                raise randname.error.DirectoryDoesNotExist(last_names_dir)

            # check info.json
            with open(path_to_info_file, "r", encoding="utf-8") as info_file:
                json_file = json.load(info_file)
                first_names_sex = set(json_file["first_names"])
                last_names_sex = set(json_file["last_names"])

            try:
                self._validate_json_schema(self.schema_info_json, path_to_info_file)
            except jsonschema.ValidationError:
                logging.error(f"Invalid info file: {info_file}")
                invalid_json_files.append(info_file)

            # check if content fo info.json match the content of first_names and last_names directories
            sex_in_first_names_dir = set(
                [path.name.split("_")[1] for path in first_names_dir.iterdir()]
            )
            sex_in_last_names_dir = set(
                [path.name.split("_")[1] for path in last_names_dir.iterdir()]
            )

            diff = first_names_sex.difference(sex_in_first_names_dir)
            if diff:
                raise randname.error.GenderMismatch(
                    f"Info file: {path_to_info_file}, defines: {first_names_sex}, but there is {sex_in_first_names_dir} in firs_names directory"
                )
            diff = last_names_sex.difference(sex_in_last_names_dir)
            if diff:
                raise randname.error.GenderMismatch(
                    f"Info file: {path_to_info_file}, defines: {last_names_sex}, but there is {sex_in_last_names_dir} in firs_names directory"
                )

            # TODO: refactor into smaller functions
            # check first_names
            glob_pattern = f"[1-9]*_[{''.join(first_names_sex)}]"
            for f in first_names_dir.iterdir():
                match = f.match(glob_pattern)
                if not match:
                    logging.error(f"Invalid name pattern: {f}")
                    invalid_name_pattern.append(f)
                try:
                    self._validate_json_schema(self.schema_name_json, f)
                except jsonschema.ValidationError:
                    logging.error(f"Invalid content pattern: {f}")
                    invalid_json_files.append(f)

            # check last_names
            glob_pattern = f"[1-9]*_[{''.join(last_names_sex)}]"
            for f in last_names_dir.iterdir():
                if not f.match(glob_pattern):
                    logging.error(f"Invalid name pattern: {f}")
                    invalid_name_pattern.append(f)
                try:
                    self._validate_json_schema(self.schema_name_json, f)
                except jsonschema.ValidationError:
                    logging.error(f"Invalid content pattern: {f}")
                    invalid_json_files.append(f)
        
        if invalid_json_files:
            raise jsonschema.ValidationError(invalid_json_files)

        if invalid_name_pattern:
            raise randname.error.FileNameDoesNotMatchPattern(invalid_name_pattern)


    def _validate_json_schema(
        self, schema, path_to_json: Union[Path, str] = None
    ) -> None:
        if path_to_json:
            path = path_to_json
        else:
            path = self._path

        with open(path, "r", encoding="utf-8") as f:
            json_content = json.load(f)

        if schema is self.schema_name_json:
            self.draft_validator_name.validate(json_content)

        if schema is self.schema_info_json:
            self.draft_validator_info.validate(json_content)

        jsonschema.validate(json_content, schema)
