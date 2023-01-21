"""Tidelift-related testing"""

import unittest

import funderfinder.sources.tidelift as tl


class TestTidelift(unittest.TestCase):
    def test_check_tidelift_funding_true(self):
        self.assertEqual(
            True,
            tl.check_tidelift_funding("pypa/setuptools"),
        )

    def test_check_tidelift_funding_false(self):
        self.assertEqual(
            False,
            tl.check_tidelift_funding("georgetown-cset/funder-finder"),
        )
