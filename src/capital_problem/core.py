import pandas
from decouple import config
import numpy
import dashboard


def column_summary(
    dataframe: pandas.DataFrame, print_: bool = True, columns_meaning: str = "Month"
):
    """Get Mean, Standard Deviation, Minimum and Maximum for dataframe's columns
    Args:
        dataframe (pandas.DataFrame): dataframe of columns (NaN values are not a problem)
        print_ (bool, optional): Print summary infos on console. Defaults to True.
        columns_meaning (str, optional): Meaning for all the columns, it will appears on the summary headers. Defaults to "Month".

    Returns:
        dict: contains headers and data `{"summary_headers": list(str), "summary_data": list(list(str, float, float, float, float))}`
    """

    # Convert the dataframe to beatiful numpy array
    numpy_array = dataframe.to_numpy().astype(float)

    # Extract headers
    dataframe_headers = list(dataframe.columns.values)

    # Extract mean
    means = numpy.nanmean(numpy_array, axis=0)

    # Extract standard deviation
    stds = numpy.nanstd(numpy_array, axis=0)

    # Initiate summary data and headers lists
    summary = []
    summary_headers = [
        columns_meaning,
        "Mean",
        "Standard Deviation",
        "Minimum",
        "Maximum",
    ]

    if print_:
        print(columns_meaning, "Summary:\n")

    # Itterate on columns
    for index, header in enumerate(dataframe_headers, start=0):

        # Extract minimum
        current_min = numpy.nanmin(numpy_array[:, index])

        # Extract maximum
        current_max = numpy.nanmax(numpy_array[:, index])
        summary.append([header, means[index], stds[index], current_min, current_max])

        # Print infos
        if print_:
            print(
                header,
                ": { mean :",
                str(means[index]),
                ", std :",
                str(stds[index]),
                ", min :",
                str(current_min),
                ", max :",
                str(current_max),
                "}",
            )

    return {"summary_headers": summary_headers, "summary_data": summary}


def run():
    reference_spreadsheets = pandas.read_excel(
        io=config("CLIMATE_PATH"),
        sheet_name=config("CLIMATE_SHEET_SI"),
        skiprows=int(config("CLIMATE_HEADER")) - 1,
        usecols=config("CLIMATE_COL_RANGE"),
    )

    # select rows wich day on column 0 starting with 'Jn' where n is a number
    reference_spreadsheets = reference_spreadsheets[
        reference_spreadsheets.iloc[:, int(config("DAY_COL_INDEX"))].str.contains(
            "^J[0-9]+$"
        )
        == True
    ]

    print(reference_spreadsheets)

    # Make mean of month columns
    month_summary = column_summary(
        dataframe=reference_spreadsheets.iloc[
            :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ]
    )

    dashboard.build_app_report(
        [
            dashboard.build_table_component(
                headers=month_summary.get("summary_headers", []),
                data=month_summary.get("summary_data", []),
                id="summary-table",
            ),
        ]
    ).run_server(debug=True)


if __name__ == "__main__":
    run()