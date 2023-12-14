import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Assume PRODUCTION_FINDERS is defined somewhere in your code
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
                if type(source) == list:
                    project_funders.append(source)
                print("------------------", project_funders)
                # try:
                # if len(project_funders)>2:
                #     print("------------------")
                #     datesFrom.append(project_funders[2][0]['datesFrom'])
                #     # print(datesFrom)

                #     datesTo.append(project_funders[2][0]["datesTo"])
                #     values.append(project_funders[2][0]["Amount_of_funding_usd"])
                #     # print(datesFrom)
                #     print(values[0],datesTo,datesFrom)
                #     print("----------------")
                # # Plotting

                # except:
                #     continue
    # print(project_funders)
    # return project_funders,datesFrom,datesTo,values
    return project_funders


def plot_graph(dates_from, values):
    plt.figure(figsize=(10, 6))
    plt.plot(dates_from, values, label="Value", marker="o")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Total Amount Received Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)


def main():
    st.title("Funding Graph Streamlit App")

    repo_name = st.text_input(
        "Enter Github repository name (e.g., georgetown-cset/funder-finder):"
    )

    if st.button("Plot Graph"):
        v0 = get_project_funders(repo_name)
        datesFrom = []
        values = []
        # if v0:
        #         print("v0",v0[0])
        #         datesFrom=[f'({i["datesFrom"]},{i["datesTo"]})' for i in v0[0][2]]
        #         # datesTo=[i["datesTo"] for i in v0[0][2]]
        #         values=[i["Amount_of_funding_usd"] for i in v0[0][2]]
        #         print("datesFrom",datesFrom)
        if v0:
            print("v0", v0)
            print(type(v0))
            if type(v0) != tuple:
                v0 = [v0]
            print(type(v0))

            # try:
            print("v0", v0)

            for i in v0[0][0]:
                print(i)
                try:
                    if "datesFrom" in i.keys():
                        datesFrom.append(f'({i["datesFrom"]},{i["datesTo"]})')
                        # datesTo=[i["datesTo"] for i in v0[0][2]]
                        values.append(i["Amount_of_funding_usd"])
                except:
                    continue
            print("datesFrom", datesFrom)
            # except:
            #     datesFrom=[]
            #     values=[]
            # print("v0",v0[0])
            # datesFrom=[f'({i["datesFrom"]},{i["datesTo"]})' for i in v0[0][2]]
            # # datesTo=[i["datesTo"] for i in v0[0][2]]
            # values=[i["Amount_of_funding_usd"] for i in v0[0][2]]
            # print("datesFrom",datesFrom)

            # print(v0)
            # plt.figure(figsize=(10, 6))
            # plt.plot(datesFrom, values, label="datesRange", marker='o')
            # # plt.plot(datesTo, values,label="datesTo", marker='o')  # To show dateTo points as well
            # plt.xlabel("Date")
            # plt.ylabel("Value")
            # plt.title("Total Amount Received Over Time")
            # plt.xticks(rotation=45)
            # plt.legend()
            # plt.tight_layout()
            # plt.show()

            plot_graph(datesFrom, values)
        else:
            st.warning("No funding data found for the given repository.")


if __name__ == "__main__":
    main()
