import argparse
import json
import logging
import os
import re
import time

import bs4
import requests
from utils import GITHUB_ORG_PATTERN, GITHUB_REPO_PATTERN, SLEEP_INTERVAL

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

    :param link_container:
    :return:
    """
    link = link_container.find("a", href=True)
    if link:
        return "https://www.google-melange.com" + link["href"]
    return None


def get_early_archive_listing_links(soup: bs4.BeautifulSoup) -> list:
    """

    :param soup:
    :return:
    """
    return soup.find_all("span", {"class": "mdl-list__item-primary-content"})


def get_link_match(text: str) -> str:
    """

    :param text:
    :return:
    """
    repo_match = re.search(GITHUB_REPO_PATTERN, text)
    if repo_match and repo_match.group(1):
        return repo_match.group(1)
    org_match = re.search(GITHUB_ORG_PATTERN, text)
    if org_match and org_match.group(1):
        return org_match.group(1)


def get_early_archive_repos(link: str) -> list:
    """

    :param link:
    :return:
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
        gh_link = get_link_match(link)
        if gh_link:
            repos.append(gh_link)
    page_link = get_link_match(project_page.text)
    if page_link:
        repos.append(page_link)
    student_projects = get_early_archive_listing_links(soup)
    student_project_links = [
        extract_listing_link(link_container) for link_container in student_projects
    ]
    for student_project_link in student_project_links:
        if not student_project_link:
            continue
        student_project_page = requests.get(student_project_link)
        student_page_link = get_link_match(student_project_page.text)
        if student_page_link:
            repos.append(student_page_link)
        print(student_project_link)
        time.sleep(SLEEP_INTERVAL)
    return repos


def get_early_archive_projects(link: str) -> list:
    """

    :param link:
    :return:
    """
    listing_page = requests.get(link)
    soup = bs4.BeautifulSoup(listing_page.text, features="html.parser")
    project_containers = get_early_archive_listing_links(soup)
    projects = []
    for container in project_containers:
        name = container.text.strip()
        link = extract_listing_link(container)
        repos = get_early_archive_repos(link)
        print({"name": name, "link": link, "repos": repos})
        projects.append({"name": name, "link": link, "repos": repos})
        time.sleep(SLEEP_INTERVAL)
    return projects


def get_projects_before_2016() -> list:
    """

    :return:
    """
    listing_page = requests.get("https://www.google-melange.com/archive/gsoc")
    soup = bs4.BeautifulSoup(listing_page.text, features="html.parser")
    year_link_containers = get_early_archive_listing_links(soup)
    projects = []
    for container in year_link_containers:
        year_link = extract_listing_link(container)
        if not year_link:
            continue
        print(f"Getting projects for {year_link}")
        year_projects = get_early_archive_projects(year_link)
        projects.extend(year_projects)
    return projects


def get_projects_2016_onward() -> list:
    """

    :return:
    """
    return []


def get_projects(output_file: str) -> None:
    """

    :param output_file:
    :return:
    """
    projects = get_projects_before_2016() + get_projects_2016_onward()
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
