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

    def test_flux_has_sponsor_this_project(self):
        # This test may fail in the future if Flux GitHub Sponsors get referenced in the Readme, or if
        # sponsors are removed from the "Sponsor this project" list
        self.assertTrue(self.finder.has_sponsor_this_project("FluxML/Flux.jl", 0, []))

    def test_babel_has_no_sponsor_this_project(self):
        # This test may fail in the future if new Babel GitHub Sponsors are added to the "Sponsor this project"
        # list, or existing GitHub Sponsors are removed from the readme but left in the "Sponsor this project" list
        self.assertFalse(self.finder.has_sponsor_this_project("babel/babel", 1, []))

    def test_funder_finder_has_no_sponsor_this_project(self):
        self.assertFalse(
            self.finder.has_sponsor_this_project("georgetown-cset/funder-finder", 0, [])
        )
