# Funder Finder

This project allows you to retrieve funding information for a GitHub repository of interest to you. Current
funding sources we support include:

- [Open Collective](funderfinder/sources/opencollective.py)

We also have some general-purpose [utilities](funderfinder/utils).

See our issue list for funding sources we plan to retrieve in the future. We welcome your contributions!

## How to contribute

Before getting started, please install the project dependencies and set up the pre-commit hooks:

```
pip install -r requirements.txt
pre-commit install
```

You can run the unit tests by running `python3 -m pytest tests` from the root of the project directory.
