import unittest

from funderfinder.utils.list_numfocus import get_github_link

from ..context import funderfinder


class TestListNumfocus(unittest.TestCase):
    def test_get_github_link_manual_override(self):
        link = get_github_link(
            "Theano",
            "Here is some text containing a reference to a "
            "github repo: https://github.com/an-owner/a-project",
        )
        self.assertEqual(link, "aesara-devs/aesara")

    def test_get_github_link_from_text(self):
        link = get_github_link(
            "A project that isn't manually mapped",
            "Here is some text containing a reference to a "
            "github repo: https://github.com/an-owner/a-project",
        )
        self.assertEqual(link, "an-owner/a-project")
