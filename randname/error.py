"""**Error module**"""


class InvalidSexArgument(Exception):
    """InvalidSexArgument.

    Raise when selected sex is not it available for chosen country.
    """

    def __init__(self, sex: str, available_sex: list):
        self.sex = sex
        self.available_sex = available_sex
        self.message = f"{self.sex} not in {self.available_sex}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.sex} -> {self.message}"


class InvalidCountryName(Exception):
    """Raise when country is not in available countries list"""

    def __init__(self, country: str, available_countries: list):
        self.country = country
        self.available_countries = available_countries
        self.message = f"{self.country} not in {self.available_countries}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.country} -> {self.message}"


class DirectoryDoesNotExist(Exception):
    """Raise when specified directory with database does not exist.

    .. todo::
        TODO: To implement
    """

    ...


class MissingInfoFile(Exception):
    """Raise when info.json file is missing in the country directory.

    .. todo::
        TODO: To implement
    """

    ...


class FileNameDoesNotMatchPattern(Exception):
    """Raise when file doesn't match the pattern.

    .. todo::
        TODO: To implement
    """

    ...


class GenderMismatch(Exception):
    """Raise when supported genders defined in info.json does not match
    to what is in corresponding folders

    .. todo::
        TODO: To implement
    """

    ...
