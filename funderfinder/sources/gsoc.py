import argparse
import json
import os
from typing import Union

from ._finder import Finder

"""
Get funding stats for projects that participated in Google Summer of Code (GSOC). At the moment, this is equivalent
to a boolean "is_affiliated" field that is true if the project participated.

To determine whether a project is affiliated with GSOC, we compare its owner or github slug (owner/repo)
to the list of GSOC-affiliated projects maintained in ../data/gsoc.jsonl. This dataset is automatically
updated on a weekly basis via a Github Action (.github/workflows/update_datasets.yml).
"""


class GSOCFinder(Finder):
    name = "Google Summer of Code"

    def get_funding_stats(self, search_params: dict) -> Union[dict, None]:
        """
        Determines whether a project is sponsored or affiliated with GSOC based on our scraped dataset and
        a project owner or slug (owner/repo)
        :param search_params: Dict of user-provided metadata that we can use to match a GSOC project
        :return: Dict of funding stats
        """
        listing_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "gsoc.jsonl"
        )
        years_matched = set()
        slug = search_params["slug"]
        slug_is_org = "/" not in slug
        with open(listing_file) as f:
            for line in f:
                project_metadata = json.loads(line.strip())
                is_exact_match = slug in project_metadata["repos"]
                is_owner_match = slug in [
                    self.get_owner_name(proj) for proj in project_metadata["repos"]
                ]
                if is_exact_match or (slug_is_org and is_owner_match):
                    years_matched.add(project_metadata["year"])
        if years_matched:
            # Put the "contribution date" in May since this is when GSOC starts
            return {
                "contributions": [
                    {"date_contribution_made": f"{year}-05-01"}
                    for year in years_matched
                ]
            }

    def run(self, gh_project_slug: Union[str, None] = None) -> list:
        stats = self.get_funding_stats(
            {
                "slug": self.get_repo_name(gh_project_slug),
            }
        )
        return [stats] if stats else []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--github_name",
        help="Case-insensitive github owner and repo name, for example nipy/nibabel",
        required=True,
    )
    args = parser.parse_args()
    finder = GSOCFinder()
    stats = finder.get_funding_stats({"slug": args.github_name})
    print(stats)
