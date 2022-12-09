import argparse
import json
import os
import re

import bs4
import requests

"""
We will scrape Numfocus's:

  * Sponsored projects (https://numfocus.org/sponsored-projects)
  * Affiliated projects (https://numfocus.org/sponsored-projects/affiliated-projects)

Currently, we do not also retrieve the small development grant information from
https://numfocus.org/programs/small-development-grants since the funded projects are a subset of the
Sponsored and Affiliated projects, but we can add this later
"""


def get_github_link(text: str) -> str:
    match = re.search(
        r"(?i)github.com/([A-Za-z0-9-_.]+/[A-Za-z0-9-_.]*[A-Za-z0-9-_])", text
    )
    return None if not match else match.group(1)


def get_sponsored_projects() -> list:
    """
    Retrieve all numfocus sponsored projects
    :return:
    """
    sponsored_projects = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:107.0) Gecko/20100101 Firefox/107.0",
        "From": "jm3312@georgetown.edu",
    }
    page = requests.get("https://numfocus.org/sponsored-projects", headers=headers)
    soup = bs4.BeautifulSoup(page.text, features="html.parser")
    for project_box in soup.find_all("div", class_="search-result-item-inner"):
        link_parent = project_box.find("a", href=True)
        link = link_parent["href"]
        project_detail_page = requests.get(link, headers=headers)

        github_ref = get_github_link(project_detail_page.text)
        sponsored_projects.append(
            {
                "id": link.strip().strip("/").split("/")[-1],
                "github_id": github_ref,
                "affiliation_type": "sponsored",
            }
        )
    return sponsored_projects


def get_funding_stats(output_file: str) -> None:
    with open(output_file, mode="w") as f:
        sponsored_projects = get_sponsored_projects()
        for project in sponsored_projects:
            f.write(json.dumps(project) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_file", default=os.path.join("..", "data", "numfocus.jsonl")
    )
    args = parser.parse_args()

    get_funding_stats(args.output_file)
