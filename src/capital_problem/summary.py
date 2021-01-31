import pandas
import numpy
import sys


def column_summary(
    dataframe: pandas.DataFrame, columns_meaning: str, print_: bool = False
):
    """Get Mean, Standard Deviation, Minimum and Maximum for dataframe's columns
    Args:
        dataframe (pandas.DataFrame): dataframe of columns (NaN values are not a problem)
        print_ (bool, optional): Print summary infos on console. Defaults to False.
        columns_meaning (str, optional): Meaning for all the columns, it will appears on the summary headers.

    Returns:
        dict: contains headers and data `{"summary_headers": list(str), "summary_data": list(list(str, float, float, float, float))}`
    """

    # Convert the dataframe to beautiful numpy array
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


if __name__ == "__main__":
    globals()[sys.argv[1]]()


def dataframe_summary(
    dataframe: pandas.DataFrame, dataframe_meaning: str, print_: bool = False
):
    """Get Minimum and Maximum for a dataframe

    Args:
        dataframe (pandas.DataFrame): dataframe (NaN values are not a problem)
        dataframe_meaning (str): Meaning for all the data.
        print_ (bool, optional): Print summary infos on console. Defaults to False.

    Returns:
        dict: Summary of a dataframe, will return `{"dataframe_meaning": str, "Minimum": float, "Maximum": float}`
    """

    # Convert the dataframe to beatiful numpy array
    numpy_array = dataframe.to_numpy().astype(float)

    # Extract minimum
    min = numpy.nanmin(numpy_array)

    # Extract maximum
    max = numpy.nanmax(numpy_array)

    if print_:
        print(
            "dataframe_meaning :",
            dataframe_meaning,
            ", Minimum :",
            min,
            ", Maximum :",
            max,
        )

    return {"dataframe_meaning": dataframe_meaning, "Minimum": min, "Maximum": max}