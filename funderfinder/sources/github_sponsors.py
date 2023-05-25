import argparse
import json
import os
from typing import Any, Union

import requests

from funderfinder.utils.github_sources import get_funding_sources

from ._finder import Finder


class GitHubSponsorsFinder(Finder):
    name = "Github Sponsors"
    API_KEY = "GITHUB_TOKEN"

    def __init__(self, run_checks=True):
        if run_checks:
            assert os.environ.get(
                self.API_KEY
            ), "Please `export GITHUB_TOKEN=<your GitHub token>"
            assert os.environ.get(
                "GITHUB_USERNAME"
            ), "Please `export GITHUB_USERNAME=<your GitHub username>"

    def get_gh_org_funding_json(self, org: str) -> Any:
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
        headers = {"Authorization": "bearer " + os.environ.get(self.API_KEY)}
        result = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        data = result.json()
        return data

    def get_org_funder_count(self, org: str) -> int:
        """
        Retrieves GitHub sponsors statistics for a GitHub organization.
        :param org: identifier for the GitHub organization
        :return: Count of funding stats
        """
        stats = self.get_gh_org_funding_json(org)
        count = (
            0
            if not stats["data"]["organization"]
            else stats["data"]["organization"]["sponsors"]["totalCount"]
        )
        return count

    def get_gh_top_contributors_json(
        self, gh_url: str, num_top_contribs: int = 3
    ) -> list:
        """
        Retrieves JSON of top contributors to a GitHub repo and whether these
        contributors have GitHub sponsors. Needs to use GitHub REST API because
        GraphQL API doesn't return contributors (as of Dec. 2022).
        :param gh_url: GitHub repository URL
        :param num_top_contribs: number of contributors to check
        :return: list
        """
        org_and_owner = self.get_owner_and_repo_name_from_github_url(gh_url)
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
        else:
            return []

        top_contribs = []
        for contributor in contributors:
            top_contribs.append(contributor["login"])

        return top_contribs

    def get_gh_user_gh_sponsors(self, user: str) -> Any:
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
        headers = {"Authorization": "bearer " + os.environ.get(self.API_KEY)}
        result = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )
        data = result.json()
        return data

    @staticmethod
    def parse_gh_user_gh_sponsors_json(gh_user_gh_sponsors_json: Any) -> int:
        """
        Retrieves GitHub sponsors statistics for a GitHub organization.
        :param gh_user_gh_sponsors_json: JSON of GitHub user GitHub sponsor info
        :return: int of number of sponsors
        """
        num_sponsors = len(
            gh_user_gh_sponsors_json["data"]["user"]["sponsors"]["edges"]
        )
        return num_sponsors

    def get_funding_stats(self, repo_name: str) -> None:
        """
        Prints project funding stats for org and contributor-level funding
        :param repo_name: Repo we want to retrieve funding stats for
        :return: None
        """
        print(f"Repo: {repo_name}")

        org = self.get_owner_name(repo_name)
        num_org_funders = self.get_org_funder_count(org)
        print(f"The number of organizational sponsors of {org} is {num_org_funders}")

        top_contribs = self.get_gh_top_contributors_json(repo_name)
        for contrib in top_contribs:
            sponsors_json = self.get_gh_user_gh_sponsors(contrib)
            num_sponsors = self.parse_gh_user_gh_sponsors_json(sponsors_json)
            print(f"Top contributor {contrib} has {num_sponsors} sponsors")

    def has_sponsor_this_project(
        self, repo: str, num_org_funders: int, top_contribs: list
    ) -> bool:
        """
        Checks links listed under "sponsor this project", and filters to those
        that are (a) github sponsor links and (b) are not organizational or user pages we've already detected.
        Returns True if any such sponsor links are present.
        :param repo: GitHub repo slug
        :param num_org_funders: Number of organizational funders this project has
        :param top_contribs: List of top contributors
        :return: True if has other "sponsor this project" sponsors, False otherwise
        """
        sources = get_funding_sources(repo)
        for source in sources:
            # Check whether we're looking at a github sponsors link
            if "github.com/sponsors" not in source:
                continue
            # Given a sponsor page link like https://github.com/sponsors/babel, get "babel"
            sponsored_entity = source.strip("/").split("/")[-1]
            if (sponsored_entity == self.get_owner_name(repo)) and num_org_funders:
                # then we're already counting this under organizational sponsors and we can skip it
                continue
            # If the sponsored entity is one of the top contributors, then we're already counting them and can skip
            return sponsored_entity not in top_contribs

    def run(self, gh_project_slug: Union[str, None] = None) -> list:
        sources = []
        org = self.get_owner_name(gh_project_slug)
        num_org_funders = self.get_org_funder_count(org)
        if num_org_funders:
            sources.append(
                {"funding_type": "organizational", "num_contributors": num_org_funders}
            )
        top_contribs = self.get_gh_top_contributors_json(gh_project_slug)
        has_contributor_sponsors = False
        for contrib in top_contribs:
            sponsors_json = self.get_gh_user_gh_sponsors(contrib)
            num_sponsors = self.parse_gh_user_gh_sponsors_json(sponsors_json)
            if num_sponsors:
                has_contributor_sponsors = True
        if has_contributor_sponsors:
            # num_contributors is tricky to include here because we would have to deduplicate across users
            sources.append({"funding_type": "individual"})
        is_sponsor_this_project = self.has_sponsor_this_project(
            gh_project_slug, num_org_funders, sources
        )
        if is_sponsor_this_project:
            sources.append({"funding_type": "sponsor_this_project"})
        return sources


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo",
        help="GitHub org and repo, e.g. psf/requests",
    )
    args = parser.parse_args()

    finder = GitHubSponsorsFinder()
    finder.get_funding_stats(args.repo)
