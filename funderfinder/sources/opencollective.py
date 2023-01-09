import argparse
import os
from typing import Union

import requests

from ._finder import Finder

"""
Retrieves project funding statistics from Opencollective. To run this script, you must first set
an OPENCOLLECTIVE_API_KEY environment variable. See: https://graphql-docs-v2.opencollective.com/access
"""


class OpenCollectiveFinder(Finder):
    name = "Open Collective"
    API_KEY_NAME = "OPENCOLLECTIVE_API_KEY"

    def __init__(self):
        assert os.environ.get(
            self.API_KEY_NAME
        ), "Please `export OPENCOLLECTIVE_API_KEY=<your opencollective api key>"
        self.api_key = os.environ.get(self.API_KEY_NAME)

    def get_funding_stats(self, project_slug: str) -> dict:
        """
        Retrives funding statistics for a project. See: https://graphql-docs-v2.opencollective.com/queries/collective
        :param project_slug: identifier for the project (like 'babel' in 'https://opencollective.com/babel')
        :return: Dict of funding stats
        """
        query = """
          query ($slug: String) {
            collective (slug: $slug) {
              totalFinancialContributors
              stats {
                totalAmountReceived {
                  currency
                  value
                }
              }
            }
          }
        """
        variables = {"slug": project_slug}

        result = requests.post(
            f"https://api.opencollective.com/graphql/v2/{self.api_key}",
            json={"query": query, "variables": variables},
        )
        data = result.json()
        stats = data["data"]["collective"]
        if stats:
            return {
                "num_contributors": stats["totalFinancialContributors"],
                "total_funding_usd": stats["stats"]["totalAmountReceived"]["value"],
            }

    def run(
        self, gh_project_slug: Union[str, None] = None, _: Union[str, None] = None
    ) -> Union[dict, None]:
        return self.get_funding_stats(self.get_repo_name(gh_project_slug))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project_slug",
        help="identifier for the project (like 'babel' in 'https://opencollective.com/babel')",
    )
    args = parser.parse_args()
    finder = OpenCollectiveFinder()
    stats = finder.get_funding_stats(args.project_slug)
    print(stats)
