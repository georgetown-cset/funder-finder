import json
import unittest
from urllib.error import HTTPError

import funderfinder.sources.github_sponsors as gs


class TestGithubSponsors(unittest.TestCase):
    def test_get_org_from_github_url(self):
        self.assertEqual(
            "tensorflow",
            gs.get_org_from_github_url("https://github.com/tensorflow/tensorflow"),
        )
        self.assertEqual(
            "georgetown-cset",
            gs.get_org_from_github_url(
                "https://github.com/georgetown-cset/funder-finder"
            ),
        )

    def get_org_and_owner_from_github_url(self):
        self.assertEqual(
            "tensorflow/tensorflow",
            gs.get_org_from_github_url("https://github.com/tensorflow/tensorflow"),
        )
        self.assertEqual(
            "georgetown-cset/funder-finder",
            gs.get_org_from_github_url(
                "https://github.com/georgetown-cset/funder-finder"
            ),
        )

    def test_get_gh_org_funding_json(self):
        try:
            gs.get_gh_org_funding_json("georgetown-cset")
        except HTTPError:
            raise

    def test_parse_gh_org_funding_json(self):
        example_json = """
        {"data":
            {"viewer":
                {"login": "jspeed-meyers"},
            "organization": {"sponsors": {"totalCount": 79}}
            }
        }
        """
        expected_dict = {
            "current_sponsors_total_count": 79,
        }
        self.assertEqual(
            expected_dict, gs.parse_gh_org_funding_json(json.loads(example_json))
        )

    def test_get_gh_top_contributors_json(self):
        # note: this could change one day! if so, will be
        # a happy thing :)
        usernames_in_top_contribs = ["jmelot", "jspeed-meyers"]
        got = gs.get_gh_top_contributors_json("georgetown-cset/funder-finder")
        for username in usernames_in_top_contribs:
            self.assertEqual(username in got, True)

    def test_get_gh_user_gh_sponsors(self):
        gs.get_gh_user_gh_sponsors("ljharb")
