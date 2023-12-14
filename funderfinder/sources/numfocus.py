import argparse
import json
import os
from typing import Union

from ._finder import Finder

"""
Get funding stats for NumFOCUS-affiliated or sponsored projects. At the moment, this is equivalent to a boolean
"is_affiliated" field that is true if the project is sponsored by or affiliated with NumFOCUS.

To determine whether a project is affiliated with NumFOCUS, we compare its name, slug, or github identifier
to the list of NumFOCUS-affiliated projects maintained in ../data/numfocus.jsonl. This dataset is automatically
updated on a weekly basis via a Github Action (.github/workflows/update_datasets.yml).
"""


class NumFocusFinder(Finder):
    name = "NumFOCUS"

    @staticmethod
    def get_funding_stats(search_params: dict, dates: list = None) -> Union[dict, None]:
        """
        Determines whether a project is sponsored or affiliated with NumFOCUS based on our scraped dataset and
        a project name, slug, or github owner and repo name
        :param search_params: Dict of user-provided metadata that we can use to match a numfocus project
        :return: Dict of funding stats
        """
        is_affiliated = False
        listing_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "numfocus.jsonl"
        )
        with open(listing_file) as f:
            for line in f:
                project_metadata = json.loads(line.strip())
                for key in search_params:
                    # In this block, we iterate through metadata fields provided by the user to match a numfocus project.
                    # Some of these fields may be null either in the user-provided input (`search_params`), or in the
                    # metadata we have for the current numfocus project (`project_metadata`). If either of these values
                    # are null, run no further checks
                    if not (project_metadata[key] and search_params[key]):
                        continue
                    is_affiliated |= (
                        project_metadata[key].lower() == search_params[key].lower()
                    )
                    # In some cases the NumFOCUS affiliation is at the GitHub organization level rather than at the repo
                    # level. So also allow match on repo owner
                    if key == "github_name":
                        owner = search_params[key].split("/")[0].lower()
                        is_affiliated |= project_metadata[key].lower() == owner
        if is_affiliated:
            return {
                "is_funded": True,
            }

    def run(self, gh_project_slug: Union[str, None] = None, dates: list = None) -> list:
        stats = self.get_funding_stats(
            {
                "name": None,
                "slug": self.get_repo_name(gh_project_slug),
                "github_name": gh_project_slug,
            },
            dates,
        )
        return [stats] if stats else []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", help="Case-insensitive name of the project, for example NiBabel"
    )
    parser.add_argument(
        "--slug", help="Case-insensitive project slug, for example nibabel"
    )
    parser.add_argument(
        "--github_name",
        help="Case-insensitive github owner and repo name, for example nipy/nibabel",
    )
    args = parser.parse_args()

    assert (
        args.name or args.slug or args.github_name
    ), "You must specify at least one of name, slug, or github_name"
    finder = NumFocusFinder()
    stats = finder.get_funding_stats(vars(args))
    print(stats)
