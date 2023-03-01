from .github_sponsors import GitHubSponsorsFinder
from .gsoc import GSOCFinder
from .numfocus import NumFocusFinder
from .opencollective import OpenCollectiveFinder
from .tidelift import TideliftFinder

PRODUCTION_FINDERS = [
    GitHubSponsorsFinder,
    NumFocusFinder,
    OpenCollectiveFinder,
    TideliftFinder,
    GSOCFinder,
]
