from .github_sponsors import GitHubSponsorsFinder
from .numfocus import NumFocusFinder
from .opencollective import OpenCollectiveFinder

PRODUCTION_FINDERS = [GitHubSponsorsFinder, NumFocusFinder, OpenCollectiveFinder]
