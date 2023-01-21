"""GitHub finder testing"""

import json
import os
import unittest
from urllib.error import HTTPError

import funderfinder.sources._finder as finder


class TestFinder(unittest.TestCase):
    def test_get_org_from_github_url(self):
        self.assertEqual(
            "tensorflow",
            finder.Finder.get_owner_name("https://github.com/tensorflow/tensorflow"),
        )
        self.assertEqual(
            "georgetown-cset",
            finder.Finder.get_owner_name(
                "https://github.com/georgetown-cset/funder-finder"
            ),
        )

    def get_org_and_owner_from_github_url(self):
        self.assertEqual(
            "tensorflow/tensorflow",
            finder.Finder.get_owner_and_repo_name_from_github_url(
                "https://github.com/tensorflow/tensorflow"
            ),
        )
        self.assertEqual(
            "georgetown-cset/funder-finder",
            finder.Finder.get_owner_and_repo_name_from_github_url(
                "https://github.com/georgetown-cset/funder-finder"
            ),
        )
