import unittest
import random
import randomnames
from bisect import bisect_left
from unittest.mock import patch

class TestRandomNames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    # @patch('randomnames.random.randint')
    # def test_first_name(self, mocked_randint):
    #     result = 
    #     self.assertEqual(result, 'Adam')

    def test_first_name(self):
        result = randomnames.first_name()
        self.assertIsInstance(result, str)

    def test_last_name(self):
        result = randomnames.last_name()
        self.assertIsInstance(result, str)

    # def test_perf_first_name(self):
    #     iterations = 100
    #     for _ in range(iterations):
    #         result = randomnames.first_name()
    #         self.assertIsInstance(result, str)

if __name__ == "__main__":
    unittest.main()