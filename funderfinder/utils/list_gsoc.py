import argparse
import json
import os
import re
import time
from itertools import chain

import bs4
import requests

from .utils import GITHUB_ORG_PATTERN, GITHUB_REPO_PATTERN, SLEEP_INTERVAL

"""
We will scrape Google Summer of Code's:

  * 2009-2015 archive (https://www.google-melange.com/archive/gsoc)
  * More recent projects, 2016 onward (https://summerofcode.withgoogle.com/archive)

For each project, we will affiliate the project with specific repos or entire organizations
(if no repo is specified) that are found in:

  * The project page
  * The student project pages
"""


def extract_listing_link(link_container: bs4.BeautifulSoup) -> str:
    """
    Extracts a GSOC listing link from its container and prepends the GSOC domain
    :param link_container: BeautifulSoup container that may contain GSOC link
    :return: Cleaned GSOC link, if link was found
    """
    link = link_container.find("a", href=True)
    if link:
        return "https://www.google-melange.com" + link["href"]
    return None


def get_early_archive_listing_links(soup: bs4.BeautifulSoup) -> list:
    """
    Extract listing link containers from an old-format GSOC page. These currently always
    appear in spans with the class shown below
    :param soup: BeautifulSoup element containing GSOC links
    :return: A list of BeautifulSoup elements corresponding to GSOC link containers
    """
    return soup.find_all("span", {"class": "mdl-list__item-primary-content"})


def get_link_matches(text: str) -> list:
    """
    Extract any github orgs (if not repo specified) or repos in text
    :param text: Text that may contain github links
    :return: List of orgs and/or repos
    """
    repo_matches = re.findall(GITHUB_REPO_PATTERN, text)
    if repo_matches:
        return list(set([repo_match for repo_match in repo_matches]))
    org_matches = re.findall(GITHUB_ORG_PATTERN, text)
    if org_matches:
        return list(set([org_match[0] for org_match in org_matches]))
    return []


def get_early_archive_repos(link: str) -> list:
    """
    Extracts repos/orgs for a pre-2016 project.
    :param link: Link to GSOC's detail page
    :return: List of github repos associated with the project
    """
    project_page = requests.get(link)
    soup = bs4.BeautifulSoup(project_page.text, features="html.parser")
    links = [
        extract_listing_link(link_elt) for link_elt in soup.find_all("a", href=True)
    ]
    repos = []
    for link in links:
        if not link:
            continue
        gh_links = get_link_matches(link)
        repos.extend(gh_links)
    page_link = get_link_matches(project_page.text)
    repos.extend(page_link)
    student_projects = get_early_archive_listing_links(soup)
    student_project_links = [
        extract_listing_link(link_container) for link_container in student_projects
    ]
    for student_project_link in student_project_links:
        if not student_project_link:
            continue
        student_project_page = requests.get(student_project_link)
        student_page_links = get_link_matches(student_project_page.text)
        if student_page_links:
            repos.extend(student_page_links)
            print("!!!!1!!!!!!!!!!!!!!FOUND ONE!!!!1!!!!!!!!!!!!!!")
            print(student_page_links)
        time.sleep(SLEEP_INTERVAL)
    return list(set(repos))


def get_early_archive_project(container: bs4.BeautifulSoup) -> dict:
    """
    Get a pre-2016 project's metadata
    :param container: BeautifulSoup container containing the project's name and link to GSOC's detail page
    :return: Dict containing project's name, link to detail page, and any repos/orgs we found for the project
    """
    name = container.find("a").text.strip()
    link = extract_listing_link(container)
    repos = get_early_archive_repos(link)
    return {"name": name, "link": link, "repos": repos}


def get_early_archive_year_projects(link: str) -> iter:
    """
    Retrieves all project metadata for a pre-2016 GSOC yearly project listing link
    :param link: Link to the year's listing page (e.g. https://www.google-melange.com/archive/gsoc/2015)
    :return: A generator of dicts containing project metadata
    """
    listing_page = requests.get(link)
    soup = bs4.BeautifulSoup(listing_page.text, features="html.parser")
    project_containers = get_early_archive_listing_links(soup)
    for container in project_containers:
        meta = get_early_archive_project(container)
        print(meta)
        yield meta
        time.sleep(SLEEP_INTERVAL)


def get_projects_before_2016() -> iter:
    """
    Retrieves projects from before 2016. GSOC uses an older website format for these
    :return: A generator of dicts containing project metadata
    """
    listing_page = requests.get("https://www.google-melange.com/archive/gsoc")
    soup = bs4.BeautifulSoup(listing_page.text, features="html.parser")
    year_link_containers = get_early_archive_listing_links(soup)
    for container in year_link_containers:
        year_link = extract_listing_link(container)
        if not year_link:
            continue
        print(f"Getting projects for {year_link}")
        year_projects = get_early_archive_year_projects(year_link)
        for project in year_projects:
            yield project


def get_projects_2016_onward() -> iter:
    """
    Retrieves projects from 2016 onward (GSOC displays these with different website structure from earlier years)
    :return: A generator of dicts containing project metadata
    """
    return []


def get_projects(output_file: str) -> None:
    """
    Retrieves all GSOC projects
    :param output_file: File to write project metadata to
    :return: None
    """
    projects = chain(get_projects_before_2016(), get_projects_2016_onward())
    with open(output_file, mode="w") as out:
        for project in projects:
            out.write(json.dumps(project))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_file", default=os.path.join("..", "data", "gsoc.jsonl")
    )
    args = parser.parse_args()

    get_projects(args.output_file)
