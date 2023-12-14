# Retrieves all funding information for a project from supported sources

import argparse
from datetime import datetime

import matplotlib.pyplot as plt
from sources.config import PRODUCTION_FINDERS


def get_project_funders(repo_name: str) -> list:
    """
    Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
    source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
    metadata of each source of funding that was found
    :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
    :return: An array of funding metadata
    """
    project_funders = []
    datesFrom = []
    datesTo = []
    values = []
    for finder_class in PRODUCTION_FINDERS:
        finder = finder_class()
        funding = finder.run(repo_name)
        # print(funding,repo_name)
        if funding:
            for source in funding:
                # print(source)
                # source["type"] = finder_class.name
                # source["is_funded"] = True
                # source["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")

                project_funders.append(source)
                print("------------------", project_funders)
                # try:
                if len(project_funders) > 2:
                    print("------------------")
                    datesFrom.append(project_funders[2][0]["datesFrom"])
                    # print(datesFrom)

                    datesTo.append(project_funders[2][0]["datesTo"])
                    values.append(project_funders[2][0]["Amount_of_funding_usd"])
                    # print(datesFrom)
                    print(values[0], datesTo, datesFrom)
                    print("----------------")
                # # Plotting

                # except:
                #     continue
    # print(project_funders)
    return project_funders, datesFrom, datesTo, values


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repo_name",
        help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
        "(e.g. georgetown-cset/funder-finder)",
    )
    args = parser.parse_args()
    v0 = get_project_funders(args.repo_name)
    print("v0", v0)
    datesFrom = [f'({i["datesFrom"]},{i["datesTo"]})' for i in v0[0][2]]
    # datesTo=[i["datesTo"] for i in v0[0][2]]
    values = [i["Amount_of_funding_usd"] for i in v0[0][2]]
    print("datesFrom", datesFrom)

    print(v0)
    plt.figure(figsize=(10, 6))
    plt.plot(datesFrom, values, label="datesRange", marker="o")
    # plt.plot(datesTo, values,label="datesTo", marker='o')  # To show dateTo points as well
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Total Amount Received Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
