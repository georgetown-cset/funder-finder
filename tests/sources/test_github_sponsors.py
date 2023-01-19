"""GitHub sponsors-related testing"""

import json
import os
import unittest
from urllib.error import HTTPError

import funderfinder.sources.github_sponsors as gs


class TestGithubSponsors(unittest.TestCase):
    finder = gs.GitHubSponsorsFinder(run_checks=False)

    def test_get_gh_org_funding_json(self):
        try:
            self.finder.get_gh_org_funding_json("georgetown-cset")
        except HTTPError:
            raise

    def test_get_gh_top_contributors_json(self):
        # note: this could change one day! if so, will be
        # a happy thing :)
        usernames_in_top_contribs = ["jmelot", "jspeed-meyers"]
        got = self.finder.get_gh_top_contributors_json("georgetown-cset/funder-finder")
        for username in usernames_in_top_contribs:
            self.assertEqual(username in got, True)

    def test_get_gh_user_gh_sponsors(self):
        self.finder.get_gh_user_gh_sponsors("ljharb")

    def test_parse_gh_user_gh_sponsors_json(self):
        test_file_path = os.path.join(
            os.path.dirname(__file__), "test-gh-user-gh-sponsors.json"
        )
        with open(test_file_path, encoding="utf-8") as test_json_file:
            test_json = json.load(test_json_file)

        got = self.finder.parse_gh_user_gh_sponsors_json(test_json)
        self.assertEqual(got, 15)
