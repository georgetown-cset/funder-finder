import unittest

from funderfinder.sources.numfocus import NumFocusFinder

from ..context import funderfinder


class TestNumfocus(unittest.TestCase):
    def test_irrelevant_get_funding_stats(self):
        stats = NumFocusFinder.get_funding_stats(
            {"name": "Something Irrelevant", "slug": None, "github_name": None}
        )
        self.assertIsNone(stats)

        stats = NumFocusFinder.get_funding_stats(
            {"name": None, "slug": "something-irrelevant", "github_name": None}
        )
        self.assertIsNone(stats)

        stats = NumFocusFinder.get_funding_stats(
            {"name": None, "slug": None, "github_name": "something/irrelevant"}
        )
        self.assertIsNone(stats)

    def test_get_funding_stats_github_repo(self):
        stats = NumFocusFinder.get_funding_stats(
            {"name": None, "slug": None, "github_name": "pandas-dev/pandas"}
        )
        self.assertTrue(stats["is_funded"])

    def test_get_funding_stats_github_owner(self):
        stats = NumFocusFinder.get_funding_stats(
            {"name": None, "slug": None, "github_name": "conda"}
        )
        self.assertTrue(stats["is_funded"])

        stats = NumFocusFinder.get_funding_stats(
            {"name": None, "slug": None, "github_name": "conda/conda-build"}
        )
        self.assertTrue(stats["is_funded"])

    def test_get_funding_stats_slug(self):
        stats = NumFocusFinder.get_funding_stats(
            {"name": None, "slug": "dask", "github_name": None}
        )
        self.assertTrue(stats["is_funded"])

    def test_get_funding_stats_project_name(self):
        stats = NumFocusFinder.get_funding_stats(
            {"name": "Project Jupyter", "slug": None, "github_name": None}
        )
        self.assertTrue(stats["is_funded"])
