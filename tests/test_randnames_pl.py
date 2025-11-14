import random
import unittest

import randname.error
from randname import core


class TestRandomNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.country = "PL"
        cls.first_names_sex = ["M", "F"]
        cls.last_names_sex = ["M", "F"]
        cls.first_names_year_range = (2018, 2021)
        cls.last_names_year_range = (2020, 2020)

    @classmethod
    def tearDownClass(cls):
        core._inst.database = core.Randname.PATH_TO_DATABASE

    def setUp(self):
        pass

    def tearDown(self):
        core._inst.database = core.Randname.PATH_TO_DATABASE

    def test_last_name_no_arguments(self):
        result = core.randlast(country=self.country)
        self.assertIsInstance(result, str)

    def test_last_name_sex(self):
        for sex in self.last_names_sex:
            result = core.randlast(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

    def test_last_name_year(self):
        year = random.choice(self.last_names_year_range)
        result = core.randlast(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_last_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(randname.error.InvalidSexArgumentError):
            core.randlast(country=self.country, sex=sex)

    def test_last_name_year_not_in_range(self):
        year = max(self.last_names_year_range) + 1
        result = core.randlast(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) - 1
        result = core.randlast(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_last_name_weights(self):
        weights = False
        result = core.randlast(country=self.country, weights=weights)
        self.assertIsInstance(result, str)

    def test_first_name_no_arguments(self):
        result = core.randfirst(country=self.country)
        self.assertIsInstance(result, str)

    def test_first_name_sex(self):
        for sex in self.first_names_sex:
            result = core.randfirst(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

    def test_first_name_year(self):
        year = random.choice(self.first_names_year_range)
        result = core.randfirst(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_first_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(randname.error.InvalidSexArgumentError):
            core.randfirst(country=self.country, sex=sex)

    def test_first_name_year_not_in_range(self):
        year = max(self.first_names_year_range) + 1
        result = core.randfirst(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.first_names_year_range) - 1
        result = core.randfirst(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_first_name_weights(self):
        weights = False
        result = core.randfirst(country=self.country, weights=weights)
        self.assertIsInstance(result, str)

    def test_full_name_no_arguments(self):
        result = core.randfull(country=self.country)
        self.assertIsInstance(result, str)

    def test_full_name_sex(self):
        for sex in self.first_names_sex:
            result = core.randfull(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

        for sex in self.last_names_sex:
            result = core.randfull(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

    def test_full_name_year(self):
        year = random.choice(self.first_names_year_range)
        result = core.randfull(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = random.choice(self.last_names_year_range)
        result = core.randfull(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_full_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(randname.error.InvalidSexArgumentError):
            core.randfull(country=self.country, sex=sex)

        with self.assertRaises(randname.error.InvalidSexArgumentError):
            core.randfull(country=self.country, sex=sex)

    def test_full_name_year_not_in_range(self):
        year = max(self.first_names_year_range) + 1
        result = core.randfull(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.first_names_year_range) - 1
        result = core.randfull(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) + 1
        result = core.randfull(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) - 1
        result = core.randfull(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_full_name_weights(self):
        weights = False
        result = core.randfull(country=self.country, weights=weights)
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
