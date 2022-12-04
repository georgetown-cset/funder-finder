import json
import unittest

from urllib.error import HTTPError

import funderfinder.sources.github_sponsors as gs


class TestGithubSponsors(unittest.TestCase):
    def test_get_org_from_github_url(self):
        expected_org = "tensorflow"
        self.assertEqual(
            expected_org,
            gs.get_org_from_github_url("https://github.com/tensorflow/tensorflow"),
        )
        expected_org = "tensorflow"
        self.assertEqual(
            "georgetown-cset",
            gs.get_org_from_github_url(
                "https://github.com/georgetown-cset/funder-finder"
            ),
        )

    def test_get_gh_org_funding_json(self):
        result = gs.get_gh_org_funding_json("georgetown-cset")
        try:
            json.json_loads(result)
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
