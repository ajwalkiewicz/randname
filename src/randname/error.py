"""Error module

Classes:
    RandnameError: Base exception for randname library.
    InvalidSexArgumentError: Exception for invalid sex argument.
    InvalidCountryNameError: Exception for invalid country name.
    DirectoryDoesNotExistError: Exception for non-existing database directory.
    MissingInfoFileError: Exception for missing info.json file.
    FileNameDoesNotMatchPatternError: Exception for invalid file name pattern.
    GenderMismatchError: Exception for gender mismatch in database directories.
"""

from typing import Any


class RandnameError(Exception): ...


class InvalidSexArgumentError(RandnameError):
    """Exception raised when selected sex is not available for chosen country.

    Attributes:
        sex: The invalid sex value that was provided
        available_sex: List of available sex values for the country
        message: Explanation of the error
    """

    def __init__(self, sex: str | None, available_sex: tuple[Any, ...]):
        self.sex = sex
        self.available_sex = available_sex
        self.message = f"{self.sex} not in {self.available_sex}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.sex} -> {self.message}"


class InvalidCountryNameError(RandnameError):
    """Exception raised when country is not in available countries list.

    Attributes:
        country: The invalid country name that was provided
        available_countries: List of available countries
        message: Explanation of the error
    """

    def __init__(self, country: str, available_countries: list[str]):
        self.country = country
        self.available_countries = available_countries
        self.message = f"{self.country} not in {self.available_countries}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.country} -> {self.message}"


class DirectoryDoesNotExistError(RandnameError):
    """Exception raised when specified directory with database does not exist."""


class MissingInfoFileError(RandnameError):
    """Exception raised when info.json file is missing in the country directory."""


class FileNameDoesNotMatchPatternError(RandnameError):
    """Exception raised when file doesn't match the pattern."""


class GenderMismatchError(RandnameError):
    """Exception raised when supported genders defined in info.json does not match
    to what is in corresponding folders."""
