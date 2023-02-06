from .github_sponsors import GitHubSponsorsFinder
from .numfocus import NumFocusFinder
from .opencollective import OpenCollectiveFinder
from .tidelift import TideliftFinder

PRODUCTION_FINDERS = [
    GitHubSponsorsFinder,
    NumFocusFinder,
    OpenCollectiveFinder,
    TideliftFinder,
]
