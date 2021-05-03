import unittest
import random
from randnames import randnames
from bisect import bisect_left
from unittest.mock import patch

class TestRandomNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.country = "US"
        cls.first_names_sex = ["M", "F"]
        cls.last_names_sex = ["N"]
        cls.first_names_year_range = (1880, 2010)
        cls.last_names_year_range = (1990, 2010)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_last_name_no_arguments(self):
        result = randnames.last_name(country=self.country)
        self.assertIsInstance(result, str)

    def test_last_name_sex(self):
        for sex in self.last_names_sex:
            result = randnames.last_name(
                country=self.country, 
                sex=sex)
            self.assertIsInstance(result, str)

    def test_last_name_year(self):
        year = random.choice(self.last_names_year_range)
        result = randnames.last_name(country=self.country, year=year)
        self.assertIsInstance(result, str)
        

    def test_last_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(
            randnames.InvalidSexArgument): randnames.last_name(
                country=self.country,
                sex=sex)

    def test_last_name_year_not_in_range(self):
        year = max(self.last_names_year_range) + 1
        result = randnames.last_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) - 1
        result = randnames.last_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_last_name_weights(self):
        weights = False
        result = randnames.last_name(country=self.country, weights=weights)
        self.assertIsInstance(result, str)


    def test_first_name_no_arguments(self):
        result = randnames.first_name(country=self.country)
        self.assertIsInstance(result, str)

    def test_first_name_sex(self):
        for sex in self.first_names_sex:
            result = randnames.first_name(
                country=self.country, 
                sex=sex)
            self.assertIsInstance(result, str)

    def test_first_name_year(self):
        year = random.choice(self.first_names_year_range)
        result = randnames.first_name(country=self.country, year=year)
        self.assertIsInstance(result, str)
        

    def test_first_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(
            randnames.InvalidSexArgument): randnames.first_name(
                country=self.country,
                sex=sex)

    def test_first_name_year_not_in_range(self):
        year = max(self.first_names_year_range) + 1
        result = randnames.first_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.first_names_year_range) - 1
        result = randnames.first_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_first_name_weights(self):
        weights = False
        result = randnames.first_name(country=self.country, weights=weights)
        self.assertIsInstance(result, str)

    def test_full_name_no_arguments(self):
        result = randnames.full_name(country=self.country)
        self.assertIsInstance(result, str)

    def test_full_name_sex(self):
        for sex in self.first_names_sex:
            result = randnames.full_name(
                country=self.country, 
                first_sex=sex)
            self.assertIsInstance(result, str)

        for sex in self.last_names_sex:
            result = randnames.full_name(
                country=self.country, 
                last_sex=sex)
            self.assertIsInstance(result, str)

    def test_full_name_year(self):
        year = random.choice(self.first_names_year_range)
        result = randnames.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = random.choice(self.last_names_year_range)
        result = randnames.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)
        

    def test_full_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(
            randnames.InvalidSexArgument): randnames.full_name(
                country=self.country,
                first_sex=sex)
        
        with self.assertRaises(
            randnames.InvalidSexArgument): randnames.full_name(
                country=self.country,
                last_sex=sex)

    def test_full_name_year_not_in_range(self):
        year = max(self.first_names_year_range) + 1
        result = randnames.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.first_names_year_range) - 1
        result = randnames.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) + 1
        result = randnames.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) - 1
        result = randnames.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_full_name_weights(self):
        weights = False
        result = randnames.full_name(country=self.country, weights=weights)
        self.assertIsInstance(result, str)

if __name__ == "__main__":
    unittest.main()
