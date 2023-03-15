import unittest

from funderfinder.sources.gsoc import GSOCFinder

from ..context import funderfinder


class TestGSOC(unittest.TestCase):
    def test_no_data_get_funding_stats(self):
        stats = GSOCFinder().get_funding_stats({"slug": "some/projectthatdoesntexist"})
        self.assertIsNone(stats)

    def test_has_data_get_funding_stats(self):
        stats = GSOCFinder().get_funding_stats({"slug": "enigma-dev/enigma-dev"})
        self.assertTrue("contributions" in stats)
        # in an effort to make the test not break when the year updates, only checking years it participated
        # as of 2023
        for year in range(2020, 2024):
            self.assertIn(
                {"date_contribution_made": f"{year}-05-01"}, stats["contributions"]
            )
