import json
import os
import unittest

from funderfinder.utils.list_numfocus import get_github_link, get_numfocus_slug

from ..context import funderfinder


class TestListNumfocus(unittest.TestCase):
    SCRAPED_DATA = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "funderfinder",
        "data",
        "numfocus.jsonl",
    )

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

    def test_gensim_affiliated(self):
        # The goal of this test is to fail if something goes very wrong with list_numfocus and a large, stable
        # affiliated project disappears
        gensim_present = False
        with open(self.SCRAPED_DATA) as f:
            for line in f:
                meta = json.loads(line.strip())
                gensim_present |= (meta["name"] == "Gensim") and (
                    meta["relationship"] == "affiliated"
                )
        self.assertTrue(gensim_present)

    def test_jupyter_sponsored(self):
        # The goal of this test is to fail if something goes very wrong with list_numfocus and a large, stable
        # sponsored project disappears
        jupyter_present = False
        with open(self.SCRAPED_DATA) as f:
            for line in f:
                meta = json.loads(line.strip())
                jupyter_present |= (meta["name"] == "Project Jupyter") and (
                    meta["relationship"] == "sponsored"
                )
        self.assertTrue(jupyter_present)

    def test_get_numfocus_slug(self):
        self.assertEqual(
            "numpy", get_numfocus_slug("https://numfocus.org/project/numpy")
        )
