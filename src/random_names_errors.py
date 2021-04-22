class RandomNameError(Exception):
    pass

class InvalidSexArgument(Exception):
    """Invalid Sex Argument

    :param Exception: Exception
    :type Exception: Exception
    """
    def __init__(self, sex: str):
        self.sex = sex
        self.message = f"{self.sex} not in ['M', 'F']"
        super().__init__(self.message)

class YearNotInRange(Exception):
    """Year not in valid range

    :param Exception: [description]
    :type Exception: [type]
    """

    def __init__(self, year: int, _range: list):
        self.year = year
        self._range = _range
        self.message = f"{self.year} not in {self._range}"
        super().__init__(self.message)