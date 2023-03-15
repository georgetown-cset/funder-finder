import argparse
import json
import os
import re
import time
from datetime import datetime
from itertools import chain

import bs4
import requests

from .utils import GITHUB_ORG_PATTERN, GITHUB_REPO_PATTERN, SCRAPE_DELAY

"""
We will scrape Google Summer of Code's:

  * 2009-2015 archive (https://www.google-melange.com/archive/gsoc)
  * More recent projects, 2016 onward (https://summerofcode.withgoogle.com/archive)
  * The current year's project, if not yet archived (https://summerofcode.withgoogle.com/programs/2023/organizations)

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
        return list(set([repo_match[1] for repo_match in repo_matches]))
    # At the moment, we only look for org matches if we didn't find a specific repo in the text
    org_matches = re.findall(GITHUB_ORG_PATTERN, text)
    if org_matches:
        return list(set([org_match[1] for org_match in org_matches]))
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
        time.sleep(SCRAPE_DELAY)
    return list(set(repos))


def get_early_archive_project(container: bs4.BeautifulSoup, year: int) -> dict:
    """
    Get a pre-2016 project's metadata
    :param container: BeautifulSoup container containing the project's name and link to GSOC's detail page
    :param year: Year the project appeared (a project may appear in more than one year)
    :return: Dict containing project's name, link to detail page, and any repos/orgs we found for the project
    """
    name = container.find("a").text.strip()
    link = extract_listing_link(container)
    repos = get_early_archive_repos(link)
    return {"name": name, "link": link, "repos": repos, "year": year}


def get_early_archive_year_projects(link: str) -> iter:
    """
    Retrieves all project metadata for a pre-2016 GSOC yearly project listing link
    :param link: Link to the year's listing page (e.g. https://www.google-melange.com/archive/gsoc/2015)
    :return: A generator of dicts containing project metadata
    """
    listing_page = requests.get(link)
    soup = bs4.BeautifulSoup(listing_page.text, features="html.parser")
    project_containers = get_early_archive_listing_links(soup)
    year = int(link.strip().strip("/").split("/")[-1])
    for container in project_containers:
        meta = get_early_archive_project(container, year)
        yield meta
        time.sleep(SCRAPE_DELAY)


def get_projects_before_2016() -> iter:
    """
    Retrieves project metadata from before 2016. GSOC uses an older website format for these
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


def get_modern_archive_project(year: int, slug: str) -> dict:
    """
    Retrieves project metadata for a project and year after 2016.
    :param year: Year we want to retrieve project metadata from
    :param slug: The GSOC project slug, retrieved from their API
    :return: Dict of project metadata
    """
    time.sleep(SCRAPE_DELAY)
    project_url = f"https://summerofcode.withgoogle.com/api/archive/programs/{year}/organizations/{slug}/"
    meta = requests.get(project_url).json()
    repos = []
    repos.extend(get_link_matches(meta["description_html"]))
    repos.extend(get_link_matches(meta["ideas_list_url"]))
    for student_project in meta["projects"]:
        repos.extend(get_link_matches(student_project["abstract_html"]))
        repos.extend(get_link_matches(student_project["project_code_url"]))
    return {
        "name": meta["name"],
        "link": project_url,
        "repos": list(set(repos)),
        "year": year,
    }


def get_modern_archive_projects(year: int) -> tuple:
    """
    Retrieves project metadata for a year after 2016, if available
    :param year: Year to retrieve project metadata from
    :return: A tuple, with the first element a boolean which is True if we found project metadata for the year and
    false otherwise (which it may be for the current year), and the second element an iterable of project metadata
    """
    org_url = f"https://summerofcode.withgoogle.com/api/archive/programs/{year}/organizations/"
    orgs = requests.get(org_url).json()
    is_ok = (type(orgs) == list) and (len(orgs) > 0)
    if not is_ok:
        return False, []
    meta = (get_modern_archive_project(year, org["slug"]) for org in orgs)
    return True, meta


def get_curr_year_project(year: int, slug: str) -> dict:
    """
    Get project metadata for a project in the current year
    :param year: The current year
    :param slug: GSOC project slug
    :return: Dict of project metadata
    """
    time.sleep(SCRAPE_DELAY)
    project_url = f"https://summerofcode.withgoogle.com/api/organization/{slug}/"
    meta = requests.get(project_url).json()
    repos = []
    repos.extend(get_link_matches(meta["description"]))
    repos.extend(get_link_matches(meta["ideas_link"]))
    repos.extend(get_link_matches(meta["source_code"]))
    repos.extend(get_link_matches(meta["website_url"]))
    return {
        "name": meta["name"],
        "link": project_url,
        "repos": list(set(repos)),
        "year": year,
    }


def get_curr_year_projects(year: int) -> iter:
    """
    Get projects for the current year, if available
    :param year: The current year
    :return: An generator (possibly empty) of project metadata
    """
    org_url = f"https://summerofcode.withgoogle.com/api/program/{year}/organizations/"
    orgs = requests.get(org_url).json()
    if type(orgs) == list:
        return (get_curr_year_project(year, org["slug"]) for org in orgs)
    return ()


def get_projects_2016_onward() -> iter:
    """
    Retrieves projects from 2016 onward (GSOC displays these with different website structure from earlier years)
    :return: A generator of dicts containing project metadata
    """
    curr_year = datetime.now().year
    for year in range(2016, curr_year + 1):
        print(f"Getting projects for {year}")
        success, projects = get_modern_archive_projects(year)
        if success:
            for project in projects:
                yield project
        # If there isn't an archive page for the current year, we may still have active projects with some
        # metadata we can scrape from the current year's page
        else:
            projects = get_curr_year_projects(year)
            for project in projects:
                yield project


def get_projects(output_file: str) -> None:
    """
    Retrieves all GSOC projects
    :param output_file: File to write project metadata to
    :return: None
    """
    projects = chain(get_projects_before_2016(), get_projects_2016_onward())
    with open(output_file, mode="w") as out:
        for project in projects:
            out.write(json.dumps(project) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_file", default=os.path.join("..", "data", "gsoc.jsonl")
    )
    args = parser.parse_args()

    get_projects(args.output_file)
