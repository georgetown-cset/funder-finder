![Build Status](https://github.com/georgetown-cset/funder-finder/actions/workflows/main.yml/badge.svg)

# Funder Finder

This project allows you to retrieve funding information for a GitHub repository of interest to you. Current
funding sources we support include:

- [Open Collective](funderfinder/sources/opencollective.py)
- [Github Sponsors](funderfinder/sources/github_sponsors.py)
- [NumFOCUS](funderfinder/sources/numfocus.py)
- [Tidelift](funderfinder/sources/tidelift.py)
- [Google Summer of Code](fundefinder/sources/gsoc.py)

We also have some general-purpose [utilities](funderfinder/utils).

See our issue list for funding sources we plan to retrieve in the future. We welcome your contributions!

## How to use

Download the project and switch to the project directory:

```bash
git clone https://github.com/georgetown-cset/funder-finder
cd funder-finder
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Add a GitHub username and a [GitHub API token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) as environment variables. For the API token, make sure to enable these scopes: `admin:org`, `read:user`, `repo`, `user:email`, and `workflow`.

```bash
export GITHUB_USERNAME=YOUR_GITHUB_USERNAME
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
```

Also add an [Open Collective API key](https://blog.opencollective.com/open-collective-graphql-api-preview/):

```bash
export OPENCOLLECTIVE_API_KEY=YOUR_OPENCOLLECTIVE_API_KEY
```

Change to `funderfinder` directory and run `get_funders.py` with the `--help` flag.

```bash
cd funderfinder
python get_funders.py --help
```

An example usage is:

```bash
PYTHONPATH='.' python3 funderfinder/get_funders.py georgetown-cset/funder-finder
```

## How to contribute

Before getting started, please install the project dependencies and set up the pre-commit hooks:

```
pip install -r requirements.txt
pre-commit install
```

You can run the unit tests by running `pytest` from the root of the project directory. For all tests to pass, the user must add a GITHUB_TOKEN environment variable (see "How to use" section above).


## Requirements:
To work on this or to understand this you need to have the knowledge of python and its libraries along GraphQL
Funder & Finder
This initiative enables you to obtain financial details for a GitHub repository that captures your interest. The existing channels we facilitate include:
•	Open Collective
•	Github Sponsors
•	NumFOCUS
•	Tidelift
Furthermore, we offer versatile tools for various purposes.
Refer to our issue list for upcoming funding sources we intend to incorporate.

## How to Use this step by step:
Download the project and switch to the project directory:
```bash
git clone https://github.com/georgetown-cset/funder-finder
cd funder-finder
```

Install the dependencies:
```bash
pip install -r requirements.txt
pre-commit install
```
If you are using “bash” Add a GitHub username and a GitHub API token as environment variables. For the API token, make sure to enable these scopes: admin:org, read:user, repo, user:email, and workflow.:
```bash
set GITHUB_TOKEN=<your GitHub token>
set GITHUB_USERNAME=<your GitHub username>
```
Also add an Open Collective API key:
```bash
set OPENCOLLECTIVE_API_KEY=YOUR_OPENCOLLECTIVE_API_KEY
pip install matplotlib
pip install streamlit
pip install --upgrade streamlit
streamlit run your_app.py which is our webPage.py
```
Change to funderfinder directory and run webpage.py with streamlit as shown below as example:
```bash
D:\open@rit\funder-finder\funderfinder> streamlit run webPage.py
```

### How to use the webpage:
Give the github names in the search bar and click on thh plot graph you will get the funding information for every six months in the given duration which is mentioned in opencollective.py you change the duration as per your requirements.
