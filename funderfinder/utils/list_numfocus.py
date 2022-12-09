import argparse
import json
import logging
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
Sponsored and Affiliated projects, but we can add this later.

For now, for each project we are recording three pieces of information:

  * id - this is the name of the project
  * github_id - this is the owner/repo string of any GitHub repo we were able to associate with the project
  * relationship - this is "sponsored" for sponsored projects, and "affiliated" for affiliated projects
  # TODO: separate id and name
"""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:107.0) Gecko/20100101 Firefox/107.0",
    "From": "jm3312@georgetown.edu",
}


def get_github_link(text: str) -> str:
    """
    Given some text, extract the first link to a page on github that contains an owner and repo name
    :param text: Text that may contain a github repo reference
    :return: The first reference found to a github repo, or None
    """
    match = re.search(
        r"(?i)github.com/([A-Za-z0-9-_.]+/[A-Za-z0-9-_.]*[A-Za-z0-9-_])", text
    )
    return None if not match else match.group(1)


def get_sponsored_projects() -> list:
    """
    Retrieve all numfocus sponsored projects
    :return: List of project metadata as specified in module-level documentation
    """
    projects = []
    page = requests.get("https://numfocus.org/sponsored-projects", headers=HEADERS)
    soup = bs4.BeautifulSoup(page.text, features="html.parser")
    for project_box in soup.find_all("div", class_="search-result-item-inner"):
        link_parent = project_box.find("a", href=True)
        link = link_parent["href"]
        name = link_parent.parent.parent.text.strip()
        project_page = requests.get(link, headers=HEADERS).text
        github_ref = get_github_link(project_page)
        if not github_ref:
            try:
                project_page_soup = bs4.BeautifulSoup(
                    project_page, features="html.parser"
                )
                project_homepage_candidates = project_page_soup.find_all(
                    string="Website"
                )
                project_homepage_elt = (
                    None
                    if not project_homepage_candidates
                    else project_homepage_candidates[0]
                )
                if project_homepage_elt:
                    project_homepage = project_homepage_elt.parent["href"]
                    project_homepage_response = requests.get(
                        project_homepage, headers=HEADERS
                    )
                    github_ref = get_github_link(project_homepage_response.text)
            except Exception as e:
                logging.warning(f"Exception when retrieving {link} for {name}: {e}")
        projects.append(
            {
                "id": name,
                "github_id": github_ref,
                "relationship": "sponsored",
            }
        )
    return projects


def get_affiliated_projects() -> list:
    """
    Retrieve all numfocus affiliated projects
    :return: List of project metadata as specified in module-level documentation
    """
    projects = []
    page = requests.get(
        "https://numfocus.org/sponsored-projects/affiliated-projects", headers=HEADERS
    )
    soup = bs4.BeautifulSoup(page.text, features="html.parser")
    for project_box in soup.find_all("div", class_="et_pb_blurb_content"):
        link_parent = project_box.find("a", href=True)
        link = link_parent["href"]
        name = (
            project_box.find("div", class_="et_pb_blurb_container")
            .find("a")
            .text.strip()
        )
        github_ref = get_github_link(link)
        if not github_ref:
            try:
                project_page = requests.get(link, headers=HEADERS)
                github_ref = get_github_link(project_page.text)
            except Exception as e:
                logging.warning(f"Exception when retrieving {link} for {name}: {e}")
        projects.append(
            {
                "id": name,
                "github_id": github_ref,
                "relationship": "affiliated",
            }
        )
    return projects


def get_funding_stats(output_file: str) -> None:
    with open(output_file, mode="w") as f:
        sponsored_projects = get_sponsored_projects()
        for project in sponsored_projects:
            f.write(json.dumps(project) + "\n")
        affiliated_projects = get_affiliated_projects()
        for project in affiliated_projects:
            f.write(json.dumps(project) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_file", default=os.path.join("..", "data", "numfocus.jsonl")
    )
    args = parser.parse_args()

    get_funding_stats(args.output_file)
