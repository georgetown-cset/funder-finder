from .github_sponsors import run
from .numfocus import NumFocusFinder
from .opencollective import OpenCollectiveFinder

PRODUCTION_FINDERS = [NumFocusFinder, OpenCollectiveFinder]
