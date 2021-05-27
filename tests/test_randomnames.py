import unittest
import random
from randname import randname
from bisect import bisect_left
from unittest.mock import patch

class TestRandomNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.available_countries = {"PL", "US", "ES"}
        cls.available_data = {'US': {'first_names': ['M', 'F'], 'last_names': ['N']}, 'PL': {'first_names': ['M', 'F'], 'last_names': ['M', 'F']}, 'ES': {'first_names': ['M'], 'last_names': ['N']}}

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_name_no_arguments(self):
        result = randname.get_name("first")
        self.assertIsInstance(result, str)
    
    def test_get_name_year(self):
        year = 1990
        result = randname.get_name("first", year=year)
        self.assertIsInstance(result, str)

    # def test_get_name_sex(self):
    #     sex = "F"
    #     result = randname.get_name("first_names", sex=sex)
    #     self.assertIsInstance(result, str)

    def test_get_name_country(self):
        country = "US"
        result = randname.get_name("first", country=country)
        self.assertIsInstance(result, str)

    def test_get_name_weights(self):
        weights = False
        result = randname.get_name("first", weights=weights)
        self.assertIsInstance(result, str)

    def test_get_name_invalid_sex(self):
        # available_sex = ["M", "F"]
        sex = "D"
        with self.assertRaises(randname.InvalidSexArgument): randname.get_name("first", sex=sex)

    def test_first_name_no_arguments(self):
        result = randname.first_name()
        self.assertIsInstance(result, str)

    def test_last_name_no_arguments(self):
        result = randname.last_name()
        self.assertIsInstance(result, str)

    def test_full_name(self):
        result = randname.full_name()
        self.assertIsInstance(result, str)

    def test_available_countries(self):
        result = randname.available_countries()
        self.assertEqual(result, self.available_countries)

    def test_data_lookup(self):
        result = randname.data_lookup()
        self.assertDictEqual(result, self.available_data)



if __name__ == "__main__":
    print(randname.__version__)
    unittest.main()
