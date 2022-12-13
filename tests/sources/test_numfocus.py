import unittest

from funderfinder.sources.numfocus import get_funding_stats

from ..context import funderfinder


class TestNumfocus(unittest.TestCase):
    def test_irrelevant_get_funding_stats(self):
        stats = get_funding_stats(
            {"name": "Something Irrelevant", "slug": None, "github_name": None}
        )
        self.assertFalse(stats["is_affiliated"])

        stats = get_funding_stats(
            {"name": None, "slug": "something-irrelevant", "github_name": None}
        )
        self.assertFalse(stats["is_affiliated"])

        stats = get_funding_stats(
            {"name": None, "slug": None, "github_name": "something/irrelevant"}
        )
        self.assertFalse(stats["is_affiliated"])

    def test_get_funding_stats_github_repo(self):
        stats = get_funding_stats(
            {"name": None, "slug": None, "github_name": "pandas-dev/pandas"}
        )
        self.assertTrue(stats["is_affiliated"])

    def test_get_funding_stats_github_owner(self):
        stats = get_funding_stats({"name": None, "slug": None, "github_name": "conda"})
        self.assertTrue(stats["is_affiliated"])

        stats = get_funding_stats(
            {"name": None, "slug": None, "github_name": "conda/conda-build"}
        )
        self.assertTrue(stats["is_affiliated"])

    def test_get_funding_stats_slug(self):
        stats = get_funding_stats({"name": None, "slug": "dask", "github_name": None})
        self.assertTrue(stats["is_affiliated"])

    def test_get_funding_stats_project_name(self):
        stats = get_funding_stats(
            {"name": "Project Jupyter", "slug": None, "github_name": None}
        )
        self.assertTrue(stats["is_affiliated"])
