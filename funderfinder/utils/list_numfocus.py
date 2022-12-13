import argparse
import json
import logging
import os
import re
import time

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

  * name - this is the name of the project
  * slug - for numfocus sponsored pages, this is the numfocus detail page slug (e.g. "nibabel" for "https://numfocus.org/project/nibabel")
  * github_name - this is the owner/repo string of any GitHub repo we were able to associate with the project
  * relationship - this is "sponsored" for sponsored projects, and "affiliated" for affiliated projects
"""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:107.0) Gecko/20100101 Firefox/107.0",
    "From": "jm3312@georgetown.edu",
}
REQUESTS_TIMEOUT = 5
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("list_numfocus")
with open(os.path.join("..", "data", "manual_repo_mapping.json")) as f:
    GITHUB_OVERRIDES = json.loads(f.read())


def get_github_link(project_name: str, text: str) -> str:
    """
    Given the project name and some text, use a manual mapping between the project name and the github repo if
    available, or extract the first link to a page on github that contains an owner and repo name
    :param project_name: Name of the GitHub project
    :param text: Text that may contain a github repo reference
    :return: The first reference found to a github repo, or None
    """
    if project_name in GITHUB_OVERRIDES:
        return GITHUB_OVERRIDES[project_name]
    match = re.search(
        r"(?i)github.com/([A-Za-z0-9-_.]+/[A-Za-z0-9-_.]*[A-Za-z0-9-_])", text
    )
    return None if not match else match.group(1)


def get_sponsored_projects() -> list:
    """
    Retrieve all numfocus sponsored projects
    :return: List of project metadata as specified in module-level documentation
    """
    LOGGER.info("Retrieving sponsored projects")
    projects = []
    page = requests.get(
        "https://numfocus.org/sponsored-projects",
        headers=HEADERS,
        timeout=REQUESTS_TIMEOUT,
    )
    soup = bs4.BeautifulSoup(page.text, features="html.parser")
    for project_box in soup.find_all("div", class_="search-result-item-inner"):
        link_parent = project_box.find("a", href=True)
        link = link_parent["href"]
        name = link_parent.parent.parent.text.strip()
        project_page = requests.get(
            link, headers=HEADERS, timeout=REQUESTS_TIMEOUT
        ).text
        github_ref = get_github_link(name, project_page)
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
                        project_homepage, headers=HEADERS, timeout=REQUESTS_TIMEOUT
                    )
                    github_ref = get_github_link(name, project_homepage_response.text)
            except Exception as e:
                LOGGER.warning(f"Exception when retrieving {link} for {name}: {e}")
        projects.append(
            {
                "name": name,
                "slug": link.strip().strip("/").split("/")[-1],
                "github_name": github_ref,
                "relationship": "sponsored",
            }
        )
        # don't make requests any faster than every 2 seconds
        time.sleep(2)
    return projects


def get_affiliated_projects() -> list:
    """
    Retrieve all numfocus affiliated projects
    :return: List of project metadata as specified in module-level documentation
    """
    LOGGER.info("Retrieving affiliated projects")
    projects = []
    page = requests.get(
        "https://numfocus.org/sponsored-projects/affiliated-projects",
        headers=HEADERS,
        timeout=REQUESTS_TIMEOUT,
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
        github_ref = get_github_link(name, link)
        if not github_ref:
            try:
                project_page = requests.get(
                    link, headers=HEADERS, timeout=REQUESTS_TIMEOUT
                )
                github_ref = get_github_link(name, project_page.text)
            except Exception as e:
                LOGGER.warning(f"Exception when retrieving {link} for {name}: {e}")
        projects.append(
            {
                "name": name,
                "slug": None,
                "github_name": github_ref,
                "relationship": "affiliated",
            }
        )
    return projects


def get_projects(output_file: str) -> None:
    """
    Get numfocus affiliated and sponsored projects, along with some basic metadata
    :param output_file: File where jsonl of project metadata should be written
    :return: None
    """
    seen_projects = set()
    with open(output_file, mode="w") as f:
        sponsored_projects = sorted(get_sponsored_projects(), key=lambda p: p["name"])
        for project in sponsored_projects:
            seen_projects.add(project["name"])
            f.write(json.dumps(project) + "\n")
        affiliated_projects = sorted(get_affiliated_projects(), key=lambda p: p["name"])
        for project in affiliated_projects:
            # if a project is both sponsored and affiliated, only list it under sponsored
            if project["name"] not in seen_projects:
                f.write(json.dumps(project) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_file", default=os.path.join("..", "data", "numfocus.jsonl")
    )
    args = parser.parse_args()

    get_projects(args.output_file)
