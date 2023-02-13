"""Tidelift-related testing"""

import unittest

from funderfinder.sources.tidelift import TideliftFinder

from ..context import funderfinder


class TestTidelift(unittest.TestCase):
    def test_get_funding_stats_is_funded(self):
        finder = TideliftFinder
        stats = finder.get_funding_stats(
            {
                "owner": finder.get_owner_name("pypa/setuptools"),
                "repo": finder.get_repo_name("pypa/setuptools"),
                "is_funded": False,
            }
        )
        self.assertTrue(stats["is_funded"])

    def test_get_funding_stats_is_not_funded(self):
        finder = TideliftFinder
        stats = finder.get_funding_stats(
            {
                "owner": finder.get_owner_name("georgetown-cset/funder-finder"),
                "repo": finder.get_repo_name("georgetown-cset/funder-finder"),
                "is_funded": False,
            }
        )
        self.assertTrue(not stats["is_funded"])
