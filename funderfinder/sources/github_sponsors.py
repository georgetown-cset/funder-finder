import argparse
import os
from typing import Any

import requests

API_KEY = "GITHUB_TOKEN"


def get_org_from_github_url():
    pass


def get_gh_org_funding_json(org: str) -> Any:
    """
    Retrives GitHub sponsors JSON for a GitHub organization. See:
    :param org: identifier for the GitHub organization
    :return: JSON
    """
    query = """
        {
          viewer {
            login
          }
          organization(login: "curl") {
            sponsors {
            totalCount
            }
        }
        }
    """
    variables = {"org": org}
    headers = {"Authorization": os.environ.get(API_KEY)}
    result = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers,
    )
    data = result.json()
    return data


def parse_gh_org_funding_json(gh_org_funding_json: Any) -> dict:
    """
    Retrives GitHub sponsors statistics for a GitHub organization. See:
    :param org: identifier for the GitHub organization
    :return: Dict of funding stats
    """
    # TODO: Write separate function that parses the data
    # Need to collect the relevant data
    # stats = data["data"]["collective"]
    # return {
    #     "num_contributors": stats["totalFinancialContributors"],
    #     "amount_received_usd": stats["stats"]["totalAmountReceived"]["value"],
    # }


if __name__ == "__main__":
    assert os.environ.get(API_KEY), "Please `export GITHUB_TOKEN=<your GitHub token>"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo",
        help="GitHub org and repo, e.g. psf/requests",
    )
    args = parser.parse_args()
    stats = get_gh_org_funding_json(args.repo)
    print(stats)
