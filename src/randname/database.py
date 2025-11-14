"""Database module

Classes:
    Database: Database container and validator.
"""

import json
from pathlib import Path
from typing import Union

import jsonschema

import randname.error
from randname.config import logger


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
        """Database container.

        Database does not validates the database on initialization., due to
        performance considerations.

        To validate the database, use `Database.validate(path)` method.
        Or set the `path` property, which will validate the new path.

        Args:
            path_to_database: Path to directory with database
        """
        # self.validate_database(path_to_database)
        self._path = Path(path_to_database)

    @property
    def path(self) -> Path:
        """Path to database

        Returns:
            Path to database
        """
        return self._path

    @path.setter
    def path(self, new_path: Path) -> None:
        Database.validate(new_path)
        self._path = Path(new_path)

    @staticmethod
    def validate(path: Path) -> bool:
        """Check if database has valid structure and it's files are
        correctly formatted.

        Warning:
            Validating database might take some time, depends how large is the database.

        Args:
            path: Path to database

        Raises:
            randname.error.DirectoryDoesNotExist: Raise when directory with database does not exist.
            randname.error.MissingInfoFile: Raise when info.json is missing.
            randname.error.GenderMismatch: Raise when gender information in info.json does not match to what is in directories.
            randname.error.FileNameDoesNotMatchPattern: Raise when file with names doesn't match naming convention.
            jsonschema.ValidationError: Raise when json file doesn't match pattern.
        """
        invalid_name_pattern: list[Path] = []
        invalid_json_files: list[Path] = []

        if not path.is_dir():
            raise randname.error.DirectoryDoesNotExistError(path)

        # traverse directory
        for country_directory in path.iterdir():
            path_to_info_file = Path() / country_directory / "info.json"
            first_names_dir = Path() / country_directory / "first_names"
            last_names_dir = Path() / country_directory / "last_names"

            # check for required files
            if not path_to_info_file.exists():
                raise randname.error.MissingInfoFileError(path_to_info_file)
            if not first_names_dir.exists():
                raise randname.error.DirectoryDoesNotExistError(first_names_dir)
            if not last_names_dir.exists():
                raise randname.error.DirectoryDoesNotExistError(last_names_dir)

            # check info.json
            with path_to_info_file.open("r", encoding="utf-8") as info_file:
                json_file = json.load(info_file)
                first_names_sex = set(json_file["first_names"])
                last_names_sex = set(json_file["last_names"])

            try:
                Database._validate_json_schema(
                    Database.schema_info_json, path_to_info_file
                )
            except jsonschema.ValidationError:
                logger.error(f"Invalid info file: {path_to_info_file}")
                invalid_json_files.append(path_to_info_file)

            # check if content fo info.json match the content of first_names and last_names directories
            sex_in_first_names_dir = set(
                [path.name.split("_")[1] for path in first_names_dir.iterdir()]
            )
            sex_in_last_names_dir = set(
                [path.name.split("_")[1] for path in last_names_dir.iterdir()]
            )

            diff = first_names_sex.difference(sex_in_first_names_dir)
            if diff:
                raise randname.error.GenderMismatchError(
                    f"Info file: {path_to_info_file}, defines: {first_names_sex}, but there is {sex_in_first_names_dir} in firs_names directory"
                )
            diff = last_names_sex.difference(sex_in_last_names_dir)
            if diff:
                raise randname.error.GenderMismatchError(
                    f"Info file: {path_to_info_file}, defines: {last_names_sex}, but there is {sex_in_last_names_dir} in firs_names directory"
                )

            # TODO: refactor into smaller functions
            # check first_names
            glob_pattern = f"[1-9]*_[{''.join(first_names_sex)}]"
            for f in first_names_dir.iterdir():
                match = f.match(glob_pattern)
                if not match:
                    logger.error(f"Invalid name pattern: {f}")
                    invalid_name_pattern.append(f)
                try:
                    Database._validate_json_schema(Database.schema_name_json, f)
                except jsonschema.ValidationError:
                    logger.error(f"Invalid content pattern: {f}")
                    invalid_json_files.append(f)

            # check last_names
            glob_pattern = f"[1-9]*_[{''.join(last_names_sex)}]"
            for f in last_names_dir.iterdir():
                if not f.match(glob_pattern):
                    logger.error(f"Invalid name pattern: {f}")
                    invalid_name_pattern.append(f)
                try:
                    Database._validate_json_schema(Database.schema_name_json, f)
                except jsonschema.ValidationError:
                    logger.error(f"Invalid content pattern: {f}")
                    invalid_json_files.append(f)

        if invalid_json_files:
            raise jsonschema.ValidationError(str(invalid_json_files))

        if invalid_name_pattern:
            raise randname.error.FileNameDoesNotMatchPatternError(invalid_name_pattern)

        return True

    @staticmethod
    def _validate_json_schema(schema, path: Path) -> None:
        """Validate JSON schema for database files

        Args:
            schema: JSON schema to validate against
            path_to_json: Path to JSON file to validate

        Raises:
            jsonschema.ValidationError: If JSON doesn't match schema
        """
        with path.open("r", encoding="utf-8") as f:
            json_content = json.load(f)

        if schema is Database.schema_name_json:
            Database.draft_validator_name.validate(json_content)

        if schema is Database.schema_info_json:
            Database.draft_validator_info.validate(json_content)

        jsonschema.validate(json_content, schema)
