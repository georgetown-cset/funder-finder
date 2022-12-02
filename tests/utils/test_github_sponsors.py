import unittest

import funderfinder.sources.github_sponsors as gs

from ..context import funderfinder


class TestGithubSponsors(unittest.TestCase):
    def test_get_org_from_github_url(self):
        expected_org = "tensorflow"
        self.assertEqual(expected_org, gs.get_org_from_github_url("https://github.com/tensorflow/tensorflow"))

    def test_parse_gh_org_funding_json(self):
        pass
        # TODO: Put in structure of JSON
        #   example_json  =     {
        #   "data": {
        #     "viewer": {
        #       "login": "jspeed-meyers"
        #     },
        #     "organization": {
        #       "sponsors": {
        #         "totalCount": 50
        #       }
        #     }
        #   }
        # }
        #         expected_sources = ["https://www.citybureau.org/support"]
        # expected_dict = {}
        # self.assertEqual(
        #     expected_dict, parse_gh_org_funding_json(example_json)
        # )
