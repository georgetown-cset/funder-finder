import unittest

from ..context import funderfinder
from funderfinder.utils.github_sources import get_funding_sources


class TestGithubSources(unittest.TestCase):
    def test_get_funding_sources_babel(self):
        expected_sources = [
            "https://opencollective.com/babel",
            "https://gitcoin.co/grants/2906/babel-compiler-for-next-generation-javascript",
            "https://github.com/sponsors/babel"
        ]
        self.assertEqual(expected_sources, get_funding_sources("babel/babel"))

    def test_get_funding_sources_cityscrapers(self):
        expected_sources = ["https://www.citybureau.org/support"]
        self.assertEqual(expected_sources, get_funding_sources("City-Bureau/city-scrapers"))

    def test_get_funding_sources_tensorflow(self):
        expected_sources = []
        self.assertEqual(expected_sources, get_funding_sources("tensorflow/tensorflow"))