import unittest

import bs4

from funderfinder.utils.list_gsoc import (
    get_curr_year_project,
    get_curr_year_projects,
    get_early_archive_project,
    get_link_matches,
    get_modern_archive_projects,
)

from ..context import funderfinder


class TestListGSOC(unittest.TestCase):
    def test_get_link_match_org(self):
        self.assertEqual(
            ["EOL"],
            get_link_matches(
                """<p>The Encyclopedia of Life (EOL) is a free, online
        collaborative encyclopedia intended to document all of the 1.9 million living speciesÂ known to science.
        It is compiled from existing databases and from contributions by experts and non-experts
        throughout the world.</p>
        <p>EOL developers are spread between United States, United Kingdom, Egypt and Philippines. Organization's
        code is located atÂ https://github.com/EOL</p>"""
            ),
        )

    def test_get_link_match_repo(self):
        self.assertEqual(
            ["beamcommunity/beamcommunity.github.com"],
            get_link_matches(
                """https://github.com/beamcommunity/beamcommunity.github.com/wiki"""
            ),
        )

    def test_get_link_match_gist(self):
        # github gists should not match as we're only searching for standard github repositories
        self.assertEqual(
            [],
            get_link_matches(
                "https://gist.github.com/sniok/fb6a1bcf4cf78303a874fa2389739764"
            ),
        )

    def test_get_early_archive_project_ext_link(self):
        fragment = """
        <span class="mdl-list__item-primary-content">
        <span class="small-logo-box mdl-list__item-icon">
        <i class="material-icons small-logo">business</i>
        </span>
        <a href="/archive/gsoc/2015/orgs/beamcommunity">BEAM Community</a>
        </span>
                """
        soup = bs4.BeautifulSoup(fragment, features="html.parser")
        self.assertEqual(
            {
                "name": "BEAM Community",
                "link": "https://www.google-melange.com/archive/gsoc/2015/orgs/beamcommunity",
                "repos": ["beamcommunity/beamcommunity.github.com"],
                "year": 2015,
            },
            get_early_archive_project(soup, 2015),
        )

    def test_get_early_archive_project_body_link(self):
        fragment = """
        <span class="mdl-list__item-primary-content">
        <span class="small-logo-box mdl-list__item-icon">
        <img alt="Encyclopedia of Life logo" class="small-logo" src="/archive/gsoc/2015/orgs/eol/logo-30.png"/>
        </span>
        <a href="/archive/gsoc/2015/orgs/eol">Encyclopedia of Life</a>
        </span>
        """
        soup = bs4.BeautifulSoup(fragment, features="html.parser")
        self.assertEqual(
            {
                "name": "Encyclopedia of Life",
                "link": "https://www.google-melange.com/archive/gsoc/2015/orgs/eol",
                "repos": ["EOL"],
                "year": 2015,
            },
            get_early_archive_project(soup, 2015),
        )

    def test_get_early_archive_project_student_project_link(self):
        fragment = """
        <span class="mdl-list__item-primary-content">
        <span class="small-logo-box mdl-list__item-icon">
        <img alt="Mono Project logo" class="small-logo" src="/archive/gsoc/2015/orgs/mono/logo-30.png"/>
        </span>
        <a href="/archive/gsoc/2015/orgs/mono">Mono Project</a>
        </span>
        """
        soup = bs4.BeautifulSoup(fragment, features="html.parser")
        self.assertEqual(
            {
                "name": "Mono Project",
                "link": "https://www.google-melange.com/archive/gsoc/2015/orgs/mono",
                "repos": ["ddobrev/QtSharp"],
                "year": 2015,
            },
            get_early_archive_project(soup, 2015),
        )

    def test_get_modern_archive_projects_has_expected_size(self):
        projects = get_modern_archive_projects(2016)
        self.assertEqual(178, len(projects))

    def test_get_curr_year_project(self):
        self.assertEqual(
            {
                "name": "Eclipse Foundation",
                "link": "https://summerofcode.withgoogle.com/api/organization/eclipse-foundation/",
                "repos": ["eclipse"],
                "year": 2023,
            },
            get_curr_year_project(2023, "eclipse-foundation"),
        )

    def test_get_curr_year_projects_empty(self):
        self.assertEqual([], [p for p in get_curr_year_projects(3000)])
