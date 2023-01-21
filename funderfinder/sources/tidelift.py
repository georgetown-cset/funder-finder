import requests

import funderfinder.sources.github_sponsors as gs


def check_tidelift_funding(gh_url):
    """
    Retrieve tidelift funding. Check README for tidelift
    e.g. https://github.com/georgetown-cset/funder-finder -> georgetown-cset/funder-finder
    :param gh_url: identifier for GitHub, e.g. linus/linux
    :return: str
    """
    gh = gs.get_org_and_owner_from_github_url(gh_url)
    org = gh.split("/")[0]
    repo = gh.split("/")[1]

    # try most likely README names
    readme_names = ["README.md", "readme.md", "README.rst", "readme.rst"]
    for name in readme_names:
        r = requests.get(f"https://raw.githubusercontent.com/{org}/{repo}/main/{name}")
        if r.status_code != 200:
            continue
        if "tidelift" in r.text:
            return True
        else:
            return False
