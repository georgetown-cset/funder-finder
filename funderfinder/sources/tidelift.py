"""Retrieve funding stats related to Tidelift funding."""
import argparse
from typing import Union

import requests

# from funderfinder.utils.github_sources import get_funding_sources
from utils.github_sources import get_funding_sources

from ._finder import Finder


class TideliftFinder(Finder):
    name = "Tidelift"

    @staticmethod
    def is_funded(text: str) -> bool:
        """
        Checks whether text indicates that project is funded by Tidelift
        :param text: Text that may include tidelift funding statement
        :return: True if project is funded by tidelift
        """
        return "tidelift" in text.lower()

    def get_funding_stats(self, params: dict, dates: list = None) -> dict:
        """
        Retrieve tidelift funding. Check README for tidelift
        e.g. https://github.com/georgetown-cset/funder-finder -> georgetown-cset/funder-finder
        :param params: Dict of user-provided metadata
        :return: dict
        """
        # try most likely README names
        readme_names = [
            "README.md",
            "Readme.md",
            "readme.md",
            "README.rst",
            "Readme.rst",
            "readme.rst",
        ]
        for name in readme_names:
            for branch in ["main", "master"]:
                r = requests.get(
                    f"https://raw.githubusercontent.com/{params['owner']}/{params['repo']}/{branch}/{name}"
                )
                if r.status_code != 200:
                    continue
                params["is_funded"] = self.is_funded(r.text)
                if params["is_funded"]:
                    return params
        sponsor_links = get_funding_sources(f"{params['owner']}/{params['repo']}")
        for link in sponsor_links:
            params["is_funded"] |= self.is_funded(link)
        return params

    def run(self, gh_project_slug: Union[str, None] = None, dates: list = None) -> list:
        stats = self.get_funding_stats(
            {
                "owner": self.get_owner_name(gh_project_slug),
                "repo": self.get_repo_name(gh_project_slug),
                "is_funded": False,
            },
            dates,
        )
        return [stats] if stats["is_funded"] else []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo",
        help="GitHub org and repo, e.g. psf/requests",
    )
    args = parser.parse_args()

    finder = TideliftFinder()
    print(
        finder.get_funding_stats(
            {
                "owner": finder.get_owner_name(args.repo),
                "repo": finder.get_repo_name(args.repo),
                "is_funded": False,
            }
        )
    )
