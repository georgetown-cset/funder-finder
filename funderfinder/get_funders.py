import argparse
from datetime import datetime

from sources.config import PRODUCTION_FINDERS

"""
Retrieves all funding information for a project from supported sources
"""


def get_project_funders(repo_name: str, project_name: str) -> list:
    """
    Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
    source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
    metadata of each source of funding that was found
    :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
    :param project_name: Name of the project (e.g. Funder Finder)
    :return: An array of funding metadata
    """
    project_funders = []
    for finder_class in PRODUCTION_FINDERS:
        finder = finder_class()
        funding = finder.run(repo_name, project_name)
        if funding:
            funding["type"] = finder_class.name
            funding["is_funded"] = True
            funding["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")
            project_funders.append(funding)
    return project_funders


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo_name",
        help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
        "(e.g. georgetown-cset/funder-finder)",
    )
    parser.add_argument(
        "--project_name", help="Name of the project, e.g. 'Funder finder'"
    )
    args = parser.parse_args()

    assert (
        args.repo_name or args.project_name
    ), "You must specify at least one of repo name or project name"

    print(get_project_funders(args.repo_name, args.project_name))
