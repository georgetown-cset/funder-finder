from typing import Union


class Finder:
    name = "Abstract Funder Finder"

    @staticmethod
    def get_repo_name(project: str) -> str:
        """
        Extracts a repo name from a github identifier (i.e. funder-finder from georgetown-cset/funder-finder)
        :param project: Github project name
        :return: Repo name
        """
        return project.strip().split("/")[1]

    @staticmethod
    def get_owner_name(project: str) -> str:
        """
        Extracts an owner (user or organization) name from a github identifier (i.e. georgetown-cset
        from georgetown-cset/funder-finder)
        :param project: Github project name
        :return: Owner name
        """
        return project.strip().split("/")[0]

    def run(
        self,
        gh_project_slug: Union[str, None] = None,
        project_name: Union[str, None] = None,
    ) -> Union[dict, None]:
        """
        This method should be implemented for subclasses and, if funding is found for a given source, return a
        nonempty subset of the following information
        {
          "funding_type": string,
          "num_contributors": int,
          "total_funding_usd": int,
          "contributors": [{
                  "contributor_name": string,
                  "amount_received_usd": int,
                  "is_affiliated": bool
          }],
          "contributions": [{
                  "date_contribution_made": YYYY-MM-DD,
                  "amount_recieved_usd": int,
                  "contributor_name": string,
          }],
          If the only information available is whether the source funds the project or not, return
          { "is_funded": True }
        }
        :param gh_project_slug: Identifier for the project owner and repo, e.g. georgetown-cset/funder-finder
        :param project_name: Name of the project, e.g. Funder Finder
        :return: A dict of metadata about the project's funding, if funded, else None
        """
        pass
