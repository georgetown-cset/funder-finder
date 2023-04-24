"""Retrieve funding stats related to Tidelift funding."""
import argparse
from typing import Union

import requests

from ._finder import Finder


class TideliftFinder(Finder):
    name = "Tidelift"

    @staticmethod
    def get_funding_stats(params: dict) -> dict:
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
                if "tidelift" in r.text.lower():
                    params["is_funded"] = True
                    break

        return params

    def run(self, gh_project_slug: Union[str, None] = None) -> list:
        stats = self.get_funding_stats(
            {
                "owner": self.get_owner_name(gh_project_slug),
                "repo": self.get_repo_name(gh_project_slug),
                "is_funded": False,
            }
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
