import argparse
import logging

import bs4
import requests

"""
Retrieves funding links listed under "Sponsor this project" on a GitHub repo
"""


def clean_link(repo: str, link: bs4.element.Tag) -> str:
    """
    Extracts href from bs4 element and converts to absolute url
    :param repo: GitHub repo identifier in the format `owner/repo_name`
    :param link: bs4 element corresponding to a tag containing sponsor link
    :return: Cleaned link string
    """
    href = link["href"]
    if href == "/sponsors":
        owner = repo.split("/")[0]
        return f"https://github.com/sponsors/{owner}"
    return href


def get_funding_sources(repo: str) -> list:
    """
    Retrives links to each of the funding sources listed under "Sponsor this project" on a GitHub repo
    :param repo: GitHub repo identifier in the format `owner/repo_name`
    :return: List of links to the repo's funding sources
    """
    page = requests.get(f"https://github.com/{repo}")
    soup = bs4.BeautifulSoup(page.text, features="html.parser")
    sponsor_elems = soup(text="Sponsor this project")
    if len(sponsor_elems) == 0:
        logging.warning(f"No sponsors found for {repo}")
        return []
    if len(sponsor_elems) > 1:
        logging.warning(
            f"Multiple elements found for {repo} with text 'Sponsor this project'"
        )
    sponsor_links = sponsor_elems[0].parent.parent.find_all("a", href=True)
    return [clean_link(repo, link) for link in sponsor_links]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo", help="GitHub repo owner and name in the format 'owner/name'"
    )
    args = parser.parse_args()

    sources = get_funding_sources(args.repo)
    print(f"{len(sources)} sources found: {sources}")
