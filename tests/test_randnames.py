import unittest
from pathlib import Path
from unittest.mock import patch

import randname
import randname.error
from randname.core import (
    Randname,
    _inst,
    available_countries,
    randfirst,
    randfull,
    randlast,
    show_data,
)


def mock_random_choice(*args, **kwargs):
    return "T1"


class TestRandomNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = Path.cwd() / "tests" / "test_data"
        _inst.database = cls.database

    @classmethod
    def tearDownClass(cls):
        _inst.database = Randname.PATH_TO_DATABASE

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_non_existing_database(self):
        _inst.database = Path("/nonexistingdir")
        with self.assertRaises(FileNotFoundError):
            randfirst()

        with self.assertRaises(FileNotFoundError):
            randlast()
        _inst.database = Randname.PATH_TO_DATABASE

    def test_last_name_standard_usage(self):
        name = randlast(sex="F", country="T1")
        test = "Last_T1_F_2"
        self.assertEqual(name, test)

        name = randlast(sex="M", country="T1")
        test = "Last_T1_M_2"
        self.assertEqual(name, test)

    def test_first_name_standard_usage(self):
        name = randfirst(sex="F", country="T1")
        test = "First_T1_F_2"
        self.assertEqual(name, test)

        name = randfirst(sex="M", country="T1")
        test = "First_T1_M_2"
        self.assertEqual(name, test)

    def test_full_name_standard_usage(self):
        name = randfull(sex="F", country="T1")
        test = "First_T1_F_2 Last_T1_F_2"
        self.assertEqual(name, test)

        name = randfull(sex="M", country="T1")
        test = "First_T1_M_2 Last_T1_M_2"
        self.assertEqual(name, test)

        name = randfull(sex="F", country="T3")
        test = "First_T1_M_2 Last_T1_F_2"
        self.assertEqual(name, test)

    def test_get_name(self):
        # TODO: test case for each parameter:
        # name: str,
        # year: int = None,
        # sex: str = None,
        # country: str = None,
        # weights: bool = True,
        # show_warnings: bool = WARNINGS,
        # database: str = DATABASE,
        pass

    def test_map_name_to_form_name(self):
        self.assertEqual(_inst._map_short_to_full_convention("first"), "first_names")
        self.assertEqual(_inst._map_short_to_full_convention("last"), "last_names")

    def test_gen_country_valid_country_in_database(self):
        test_country = "T1"
        country = _inst._gen_country(test_country)
        self.assertEqual(test_country, country)

    def test_gen_country_invalid_country_in_database(self):
        test_country = "T4"
        with self.assertRaises(randname.error.InvalidCountryNameError):
            _inst._gen_country(test_country)

    def test_gen_country_random(self):
        test_country = "T1"
        with patch("random.choice", mock_random_choice):
            country = _inst._gen_country(None)
            self.assertEqual(test_country, country)

    def test_gen_year(self):
        # TODO: gen year
        ...

    def test_gen_sex(self):
        # TODO: gen sex
        ...

    def test_available_sex(self):
        # TODO: available_sex
        ...

    def test_gen_name_from_file(self):
        file = Path("./tests/test_data/T2/first_names/gen_name_from_file_test")
        name = _inst._gen_name_from_file(file)
        test = "First_T2_F_2"
        self.assertEqual(name, test)

    def test_gen_name_from_file_with_cum_weights_set_to_false(self):
        test = {"First_T2_F_1", "First_T2_F_2"}
        file = Path("./tests/test_data/T2/first_names/gen_name_from_file_test")
        names = {_inst._gen_name_from_file(file, False) for _ in range(100)}
        # It's not 100% sure, but chance of rolling 100 times just one name is equal to: 1/(2^100) which is approximately 0, exactly it's: 7.8886e10-31.
        self.assertEqual(names, test)

    def test_available_countries(self):
        countries = available_countries(self.database)
        test = {"T1", "T2", "T3"}
        self.assertEqual(countries, test)

    def test_show_data(self):
        data = show_data(self.database)
        test = {
            "T3": {"first_names": ["M"], "last_names": ["M", "F"]},
            "T2": {"first_names": ["M", "F"], "last_names": ["M", "F"]},
            "T1": {"first_names": ["M", "F"], "last_names": ["M", "F"]},
        }
        self.assertDictEqual(data, test)

    def test_validate_database(self):
        # TODO: validate_database
        ...
