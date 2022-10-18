import random
import unittest

import randname
import randname.error


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
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_last_name_no_arguments(self):
        result = randname.last_name(country=self.country)
        self.assertIsInstance(result, str)

    def test_last_name_sex(self):
        for sex in self.last_names_sex:
            result = randname.last_name(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

    def test_last_name_year(self):
        year = random.choice(self.last_names_year_range)
        result = randname.last_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_last_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(randname.error.InvalidSexArgument):
            randname.last_name(country=self.country, sex=sex)

    def test_last_name_year_not_in_range(self):
        year = max(self.last_names_year_range) + 1
        result = randname.last_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) - 1
        result = randname.last_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_last_name_weights(self):
        weights = False
        result = randname.last_name(country=self.country, weights=weights)
        self.assertIsInstance(result, str)

    def test_first_name_no_arguments(self):
        result = randname.first_name(country=self.country)
        self.assertIsInstance(result, str)

    def test_first_name_sex(self):
        for sex in self.first_names_sex:
            result = randname.first_name(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

    def test_first_name_year(self):
        year = random.choice(self.first_names_year_range)
        result = randname.first_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_first_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(randname.error.InvalidSexArgument):
            randname.first_name(country=self.country, sex=sex)

    def test_first_name_year_not_in_range(self):
        year = max(self.first_names_year_range) + 1
        result = randname.first_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.first_names_year_range) - 1
        result = randname.first_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_first_name_weights(self):
        weights = False
        result = randname.first_name(country=self.country, weights=weights)
        self.assertIsInstance(result, str)

    def test_full_name_no_arguments(self):
        result = randname.full_name(country=self.country)
        self.assertIsInstance(result, str)

    def test_full_name_sex(self):
        for sex in self.first_names_sex:
            result = randname.full_name(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

        for sex in self.last_names_sex:
            result = randname.full_name(country=self.country, sex=sex)
            self.assertIsInstance(result, str)

    def test_full_name_year(self):
        year = random.choice(self.first_names_year_range)
        result = randname.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = random.choice(self.last_names_year_range)
        result = randname.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_full_name_invalid_sex(self):
        sex = "D"
        with self.assertRaises(randname.error.InvalidSexArgument):
            randname.full_name(country=self.country, sex=sex)

    def test_full_name_year_not_in_range(self):
        year = max(self.first_names_year_range) + 1
        result = randname.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.first_names_year_range) - 1
        result = randname.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) + 1
        result = randname.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

        year = max(self.last_names_year_range) - 1
        result = randname.full_name(country=self.country, year=year)
        self.assertIsInstance(result, str)

    def test_full_name_weights(self):
        weights = False
        result = randname.full_name(country=self.country, weights=weights)
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
