import unittest
from unittest.mock import patch

import randname
import randname.error
from randname.randname import (
    _gen_name,
    _map_name_to_form_name,
    _gen_country,
    _gen_year,
    _gen_sex,
    _gen_name_from_file,
)


def mock_random_choice(*args, **kwargs):
    return "T1"


class TestRandomNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.database = Path() / "." / "test_data"
        cls.database = "./tests/test_data"
        cls.kwargs = {"database": cls.database}

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_non_existing_database(self):
        database = "/nonexistingdir"
        with self.assertRaises(FileNotFoundError):
            randname.first_name(database=database)
            randname.last_name(database=database)

    def test_last_name_standard_usage(self):
        name = randname.last_name(sex="F", country="T1", **self.kwargs)
        test = "Last_T1_F_2"
        self.assertEqual(name, test)

        name = randname.last_name(sex="M", country="T1", **self.kwargs)
        test = "Last_T1_M_2"
        self.assertEqual(name, test)

    def test_first_name_standard_usage(self):
        name = randname.first_name(sex="F", country="T1", **self.kwargs)
        test = "First_T1_F_2"
        self.assertEqual(name, test)

        name = randname.first_name(sex="M", country="T1", **self.kwargs)
        test = "First_T1_M_2"
        self.assertEqual(name, test)

    def test_full_name_standard_usage(self):
        name = randname.full_name(sex="F", country="T1", **self.kwargs)
        test = "First_T1_F_2 Last_T1_F_2"
        self.assertEqual(name, test)

        name = randname.full_name(sex="M", country="T1", **self.kwargs)
        test = "First_T1_M_2 Last_T1_M_2"
        self.assertEqual(name, test)

        name = randname.full_name(sex="F", country="T3", **self.kwargs)
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
        self.assertEqual(_map_name_to_form_name("first"), "first_names")
        self.assertEqual(_map_name_to_form_name("last"), "last_names")

    def test_gen_country_valid_country_in_database(self):
        test_country = "T1"
        country = _gen_country(test_country, self.database)
        self.assertEqual(test_country, country)

    def test_gen_country_invalid_country_in_database(self):
        test_country = "T4"
        with self.assertRaises(randname.error.InvalidCountryName):
            _gen_country(test_country, self.database)

    def test_gen_country_random(self):
        test_country = "T1"
        with patch("random.choice", mock_random_choice):
            country = _gen_country(None, self.database)
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
        path_to_dataset = "./tests/test_data/T2/first_names/gen_name_from_file_test"
        name = _gen_name_from_file(path_to_dataset)
        test = "First_T2_F_2"
        self.assertEqual(name, test)

    def test_gen_name_from_file_with_cum_weights_set_to_false(self):
        path_to_dataset = "./tests/test_data/T2/first_names/gen_name_from_file_test"
        test = {"First_T2_F_1", "First_T2_F_2"}
        names = {_gen_name_from_file(path_to_dataset, False) for _ in range(100)}
        # It's not 100% sure, but chance of rolling 100 times just one name is equal to: 1/(2^100) which is approximately 0, exactly it's: 7.8886e10-31.
        self.assertEqual(names, test)

    def test_available_countries(self):
        countries = randname.available_countries(self.database)
        test = {"T1", "T2", "T3"}
        self.assertEqual(countries, test)

    def test_show_data(self):
        data = randname.show_data(self.database)
        test = {
            "T3": {"first_names": ["M"], "last_names": ["M", "F"]},
            "T2": {"first_names": ["M", "F"], "last_names": ["M", "F"]},
            "T1": {"first_names": ["M", "F"], "last_names": ["M", "F"]},
        }
        self.assertDictEqual(data, test)

    def test_validate_database(self):
        # TODO: validate_database
        ...
