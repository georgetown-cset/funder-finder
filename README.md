# Funder Finder

This project allows you to retrieve funding information for a GitHub repository of interest to you. Current
funding sources we support include:

- [Open Collective](funderfinder/sources/opencollective.py)
- [Github Sponsors](funderfinder/sources/github_sponsors.py)
- [NumFOCUS](funderfinder/sources/numfocus.py)
- [Tidelift](funderfinder/sources/tidelift.py)

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

Add a GitHub username and a [GitHub API token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) as environment variables:

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
python3 funderfinder/get_funders.py repo_name=georgetown-cset/funder-finder
```

## How to contribute

Before getting started, please install the project dependencies and set up the pre-commit hooks:

```
pip install -r requirements.txt
pre-commit install
```

You can run the unit tests by running `pytest` from the root of the project directory. For all tests to pass, the user must add a GITHUB_TOKEN environment variable (see "How to use" section above).
