GITHUB_PREFIX = "(^|[^.])github.com/([A-Za-z0-9-_.]+"
GITHUB_REPO_PATTERN = rf"(?i){GITHUB_PREFIX}/[A-Za-z0-9-_.]*[A-Za-z0-9-_])"
GITHUB_ORG_PATTERN = rf"(?i){GITHUB_PREFIX})(\b)"

SCRAPE_DELAY = 2
