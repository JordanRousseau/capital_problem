import pandas
from decouple import config
import numpy
from dashboard import build_app_report


def mean(dataframe: pandas.DataFrame):
    """Make mean by column

    Args:
        dataframe (pandas.DataFrame): dataframe of columns (NaN values are not a problem)

    Returns:
        list: list of header and mean associated with
    """
    headers = list(dataframe.columns.values)
    means = numpy.nanmean(dataframe.to_numpy(), axis=0)
    means_enriched = []

    print("Moyenne par mois:\n")

    for i, mean in enumerate(means, start=0):
        print(headers[i] + " : " + str(mean))
        means_enriched.append([headers[i], mean])

    return means_enriched


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
    month_mean = mean(
        dataframe=reference_spreadsheets.iloc[
            :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ]
    )

    build_app_report([]).run_server(debug=True)


if __name__ == "__main__":
    run()