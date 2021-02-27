#!/usr/bin/env python3

import unittest
from splitamount import SplitAmount as SA


class TestSplitAmount(unittest.TestCase):

    def test_get_fraction(self):
        self.assertEqual(SA(.1).get_fraction(), 10)
        self.assertEqual(SA(.0).get_fraction(), 0)
        self.assertEqual(SA(.9).get_fraction(), 90)
        self.assertEqual(SA(.09).get_fraction(), 9)
        self.assertEqual(SA(.99).get_fraction(), 99)

    def test_get_integral(self):
        self.assertEqual(SA(.1).get_integral(), 0)
        self.assertEqual(SA(10.1).get_integral(), 10)

    def test_get_full_amount(self):
        self.assertEqual(SA(.09).get_full_amount(), 9)
        self.assertEqual(SA(.9).get_full_amount(), 90)
        self.assertEqual(SA(1.9).get_full_amount(), 190)
        self.assertEqual(SA(1.99).get_full_amount(), 199)


if __name__ == '__main__':
    unittest.main()
