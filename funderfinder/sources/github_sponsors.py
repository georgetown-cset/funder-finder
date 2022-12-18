import argparse
import json
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


def get_org_and_owner_from_github_url(gh_url: str) -> str:
    """
    Returns GitHub org and owner from a GitHub URL,
    e.g. https://github.com/georgetown-cset/funder-finder -> georgetown-cset/funder-finder
    :param gh_url: identifier for the GitHub organization
    :return: str
    """
    return "/".join(gh_url.split("/")[-2:])


def get_gh_org_funding_json(org: str) -> Any:
    """
    Retrieves GitHub sponsors JSON for a GitHub organization. See:
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
    Retrieves GitHub sponsors statistics for a GitHub organization.
    :param org: identifier for the GitHub organization
    :return: Dict of funding stats
    """
    funding_dict = {
        "current_sponsors_total_count": gh_org_funding_json["data"]["organization"][
            "sponsors"
        ]["totalCount"]
    }
    return funding_dict


def get_gh_top_contributors_json(gh_url: str, num_top_contribs: int = 3) -> list:
    """
    Retrieves JSON of top contributors to a GitHub repo and whether these
    contributors have GitHub sponsors. Needs to use GitHub REST API because
    GraphQL API doesn't return contributors (as of Dec. 2022).
    :param gh_url: GitHub repository URL
    :param num_top_contribs: number of contributors to check
    :return: list
    """
    org_and_owner = get_org_and_owner_from_github_url(gh_url)
    response = requests.get(
        "https://api.github.com/repos/"
        + org_and_owner
        + "/contributors?page=1"
        + "&per_page="
        + str(num_top_contribs),
        auth=(os.environ.get("GITHUB_USERNAME"), os.environ.get("GITHUB_TOKEN")),
    )

    if response.ok:
        contributors = json.loads(response.text or response.content)

    top_contribs = []
    for contributor in contributors:
        top_contribs.append(contributor["login"])

    return top_contribs


def get_gh_user_gh_sponsors(user: str) -> Any:
    """
    Retrieves GitHub sponsors JSON for a GitHub user.
    :param user: identifier a GitHub user
    :return: JSON
    """
    query = """
        query ($user: String!) {
            user(login: $user) {
                sponsors(first: 100) {
                edges {
                    node {
                    ... on Organization {
                        id
                        email
                    }
                    ... on User {
                        id
                        email
                    }
                    }
                }
                }
            }
        }
    """
    variables = {"user": user}
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


def parse_gh_user_gh_sponsors_json(gh_user_gh_sponsors_json: Any) -> int:
    """
    Retrieves GitHub sponsors statistics for a GitHub organization.
    :param gh_user_gh_sponsors_json: JSON of GitHub user GitHub sponsor info
    :return: int of number of sponsors
    """
    num_sponsors = len(gh_user_gh_sponsors_json["data"]["user"]["sponsors"]["edges"])
    return num_sponsors


if __name__ == "__main__":
    assert os.environ.get(API_KEY), "Please `export GITHUB_TOKEN=<your GitHub token>"
    assert os.environ.get(
        "GITHUB_USERNAME"
    ), "Please `export GITHUB_USERNAME=<your GitHub username>"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo",
        help="GitHub org and repo, e.g. psf/requests",
    )
    args = parser.parse_args()

    print(f"Repo: {args.repo}")

    org = get_org_from_github_url(args.repo)
    stats = get_gh_org_funding_json(org)
    print(
        f"The number of organizational sponsors of {org} is {stats['data']['organization']['sponsors']['totalCount']}"
    )

    top_contribs = get_gh_top_contributors_json(args.repo)
    for contrib in top_contribs:
        sponsors_json = get_gh_user_gh_sponsors(contrib)
        num_sponsors = parse_gh_user_gh_sponsors_json(sponsors_json)
        print(f"Top contributor {contrib} has {num_sponsors} sponsors")
