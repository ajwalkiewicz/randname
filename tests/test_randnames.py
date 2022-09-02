import random
import unittest
from pathlib import Path
from bisect import bisect_left
from unittest.mock import patch

from randname import randname


class TestRandomNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.database = Path() / "." / "test_data"
        cls.database = "/home/walu/Git/randname/tests/test_data"
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
        name = randname.full_name(
            first_sex="F", last_sex="F", country="T1", **self.kwargs
        )
        test = "First_T1_F_2 Last_T1_F_2"
        self.assertEqual(name, test)

        name = randname.full_name(
            first_sex="M", last_sex="M", country="T1", **self.kwargs
        )
        test = "First_T1_M_2 Last_T1_M_2"
        self.assertEqual(name, test)

    def test_available_countries(self):
        # correct_countries = set({"T1", "T2", "T3"})
        # self.assertSetEqual(randname.available_countries(), correct_countries)
        # TODO: refactor available countries function
        pass

    def test_data_lookup(self):
        # TODO: refactor data lookup function
        pass


if __name__ == "__main__":
    print(randname.__version__)
    unittest.main()
