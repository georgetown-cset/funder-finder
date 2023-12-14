import argparse
import os
from typing import Union

import requests

from ._finder import Finder

"""
Retrieves project funding statistics from Opencollective. To run this script, you must first set
an OPENCOLLECTIVE_API_KEY environment variable. See: https://graphql-docs-v2.opencollective.com/access
"""


class OpenCollectiveFinder(Finder):
    name = "Open Collective"
    API_KEY_NAME = "OPENCOLLECTIVE_API_KEY"

    def __init__(self):
        assert os.environ.get(
            self.API_KEY_NAME
        ), "Please `export OPENCOLLECTIVE_API_KEY=<your opencollective api key>"
        self.api_key = os.environ.get(self.API_KEY_NAME)

    def get_funding_stats(self, project_slug: str) -> dict:
        """
        Retrives funding statistics for a project. See: https://graphql-docs-v2.opencollective.com/queries/collective
        :param project_slug: identifier for the project (like 'babel' in 'https://opencollective.com/babel')
        :return: Dict of funding stats
        """
        # query = """
        #   query ($slug: String) {
        #     collective (slug: $slug) {
        #       totalFinancialContributors
        #       stats {
        #         totalAmountReceived {
        #           currency
        #           value
        #         }
        #       }
        #     }
        #   }
        # """
        result_arr = []
        dates = [
            ("2018-01-01T00:00:00Z", "2018-07-01T00:00:00Z"),
            ("2018-07-01T00:00:00Z", "2019-01-01T00:00:00Z"),
            ("2019-01-01T00:00:00Z", "2019-07-01T00:00:00Z"),
            ("2019-07-01T00:00:00Z", "2020-01-01T00:00:00Z"),
            ("2020-01-01T00:00:00Z", "2020-07-01T00:00:00Z"),
            ("2020-07-01T00:00:00Z", "2021-01-01T00:00:00Z"),
            ("2021-01-01T00:00:00Z", "2021-07-01T00:00:00Z"),
            ("2021-07-01T00:00:00Z", "2022-01-01T00:00:00Z"),
            ("2022-01-01T00:00:00Z", "2022-07-01T00:00:00Z"),
            ("2022-07-01T00:00:00Z", "2023-01-01T00:00:00Z"),
            ("2023-01-01T00:00:00Z", "2023-07-01T00:00:00Z"),
            ("2023-07-01T00:00:00Z", "2024-01-01T00:00:00Z"),
        ]
        # dates=[
        # ("2015-01-01T00:00:00Z", "2015-07-01T00:00:00Z"),
        # ("2015-07-01T00:00:00Z", "2016-01-01T00:00:00Z"),
        # ("2016-01-01T00:00:00Z", "2016-07-01T00:00:00Z"),
        # ("2016-07-01T00:00:00Z", "2017-01-01T00:00:00Z"),
        # ("2017-01-01T00:00:00Z", "2017-07-01T00:00:00Z"),
        # ("2017-07-01T00:00:00Z", "2018-01-01T00:00:00Z"),
        # ("2018-01-01T00:00:00Z", "2018-07-01T00:00:00Z"),
        # ("2018-07-01T00:00:00Z", "2019-01-01T00:00:00Z"),
        # ("2019-01-01T00:00:00Z", "2019-07-01T00:00:00Z"),
        # ("2019-07-01T00:00:00Z", "2020-01-01T00:00:00Z")
        # ]

        # dates=[
        # ("2020-01-01T00:00:00Z",  "2024-01-01T00:00:00Z")]
        # query= """
        # query ($slug: String) {
        #     collective (slug: $slug) {
        #     totalFinancialContributors
        #       stats {
        #         totalAmountReceived(
        #           dateFrom: "2020-01-01T00:00:00Z"
        #           dateTo: "2024-01-01T00:00:00Z"
        #         ) {
        #           currency
        #           value
        #         }
        #       }
        #     }
        #   }"""
        for date_range in dates:
            query = f"""
            query ($slug: String) {{
                collective (slug: $slug) {{
                    totalFinancialContributors
                    stats {{
                        totalAmountReceived(
                            dateFrom: "{date_range[0]}"
                            dateTo: "{date_range[1]}"
                        ) {{
                            currency
                            value
                        }}
                    }}
                }}
            }}
            """
            # print(query)
            variables = {"slug": project_slug}

            result = requests.post(
                f"https://api.opencollective.com/graphql/v2/{self.api_key}",
                json={"query": query, "variables": variables},
            )
            data = result.json()
            # print(data)
            stats = data["data"]["collective"]
            # print("--------")
            # print("Stats",stats)
            if stats:
                result_arr.append(
                    {
                        "num_contributors": stats["totalFinancialContributors"],
                        "Amount_of_funding_usd": stats["stats"]["totalAmountReceived"][
                            "value"
                        ],
                        "datesFrom": date_range[0],
                        "datesTo": date_range[1],
                    }
                )
        print("result_arr", result_arr)
        return result_arr

    def run(self, gh_project_slug: Union[str, None] = None) -> list:
        stats = self.get_funding_stats(self.get_repo_name(gh_project_slug))
        return [stats] if stats else []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project_slug",
        help="identifier for the project (like 'babel' in 'https://opencollective.com/babel')",
    )
    args = parser.parse_args()
    finder = OpenCollectiveFinder()
    stats = finder.get_funding_stats(args.project_slug)
    print(stats)
