import argparse
import os

import requests

"""
Retrieves project funding statistics from Opencollective. To run this script, you must first set
an OPENCOLLECTIVE_API_KEY environment variable. See: https://graphql-docs-v2.opencollective.com/access
"""

API_KEY = "OPENCOLLECTIVE_API_KEY"


def get_funding_stats(project_slug: str) -> dict:
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
    api_key = os.environ.get(API_KEY)
    result = requests.post(
        f"https://api.opencollective.com/graphql/v2/{api_key}",
        json={"query": query, "variables": variables},
    )
    data = result.json()
    stats = data["data"]["collective"]
    return {
        "num_contributors": stats["totalFinancialContributors"],
        "amount_received_usd": stats["stats"]["totalAmountReceived"]["value"],
    }


if __name__ == "__main__":
    assert os.environ.get(
        API_KEY
    ), "Please `export OPENCOLLECTIVE_API_KEY=<your opencollective api key>"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project_slug",
        help="identifier for the project (like 'babel' in 'https://opencollective.com/babel')",
    )
    args = parser.parse_args()
    stats = get_funding_stats(args.project_slug)
    print(stats)
