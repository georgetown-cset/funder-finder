import argparse
import os
from typing import Any

import requests

API_KEY = "GITHUB_TOKEN"


def get_org_from_github_url(gh_url: str) -> str:
    """
    Returns GitHub org from a GitHub URL,
    e.g. https://github.com/georgetown-cset/funder-finder -> georgetown-cset
    :param gh_url: identifier for the GitHub organization
    :return: str
    """
    return gh_url.split("/")[-2]


def get_gh_org_funding_json(org: str) -> Any:
    """
    Retrives GitHub sponsors JSON for a GitHub organization. See:
    :param org: identifier for the GitHub organization
    :return: JSON
    """
    query = """
        query ($org: String!) {
          viewer {
            login
          }
          organization(login: $org) {
            sponsors {
              totalCount
            }
          }
        }
    """
    variables = {"org": org}
    # adding bearer before the token is a suprising but necessary requirement
    # see SO: https://stackoverflow.com/questions/70693292/github-graphql-api-this-endpoint-requires-you-to-be-authenticated
    headers = {"Authorization": "bearer " + os.environ.get(API_KEY)}
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
    funding_dict = {
        "current_sponsors_total_count": gh_org_funding_json["data"]["organization"][
            "sponsors"
        ]["totalCount"]
    }
    return funding_dict


if __name__ == "__main__":
    assert os.environ.get(API_KEY), "Please `export GITHUB_TOKEN=<your GitHub token>"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo",
        help="GitHub org and repo, e.g. psf/requests",
    )
    args = parser.parse_args()

    org = get_org_from_github_url(args.repo)
    stats = get_gh_org_funding_json(org)
    print(stats)
