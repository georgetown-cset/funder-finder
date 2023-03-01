import unittest

import bs4

from funderfinder.utils.list_gsoc import get_early_archive_project, get_link_match

from ..context import funderfinder


class TestListGSOC(unittest.TestCase):
    def test_get_link_match_org(self):
        self.assertEqual(
            "EOL",
            get_link_match(
                """<p>The Encyclopedia of Life (EOL) is a free, online
        collaborative encyclopedia intended to document all of the 1.9 million living speciesÂ known to science.
        It is compiled from existing databases and from contributions by experts and non-experts
        throughout the world.</p>
        <p>EOL developers are spread between United States, United Kingdom, Egypt and Philippines. Organization's
        code is located atÂ https://github.com/EOL</p>"""
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
            },
            get_early_archive_project(soup),
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
            },
            get_early_archive_project(soup),
        )
