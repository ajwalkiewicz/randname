class InvalidSexArgument(Exception):
    """InvalidSexArgument.
    
    Raise when selectet sex is not it available for chosen country. 
    """
    def __init__(self, sex: str, available_sex: list):
        self.sex = sex
        self.available_sex = available_sex
        self.message = f"{self.sex} not in {self.available_sex}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.sex} -> {self.message}"