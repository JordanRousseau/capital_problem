import pandas
from decouple import config
import numpy
import dashboard


def summary(dataframe: pandas.DataFrame):
    """Make mean by column

    Args:
        dataframe (pandas.DataFrame): dataframe of columns (NaN values are not a problem)

    Returns:
        list: list of header and mean associated with
    """
    headers = list(dataframe.columns.values)
    means = numpy.nanmean(dataframe.to_numpy(), axis=0)
    stds = numpy.nanstd(dataframe.to_numpy(), axis=0)
    summary = []

    print("Summary:\n")

    for i, header in enumerate(headers, start=0):
        print(header, ": { mean :", str(means[i]), ", std :", str(stds[i]), "}")
        summary.append([header, means[i], stds[i]])

    return summary


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
    month_summary = summary(
        dataframe=reference_spreadsheets.iloc[
            :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ]
    )

    dashboard.build_app_report(
        [
            dashboard.build_table_component(
                headers=["Month", "Mean", "Standard Deviation"],
                data=month_summary,
                id="summary-table",
            ),
        ]
    ).run_server(debug=True)


if __name__ == "__main__":
    run()