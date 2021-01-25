import pandas
from decouple import config
import numpy


def mean(dataframe: pandas.DataFrame):
    headers = list(dataframe.columns.values)
    months_mean = numpy.nanmean(dataframe.to_numpy(), axis=0)
    print("Moyenne par mois:\n")
    for i, months_mean in enumerate(months_mean, start=0):
        print(headers[i] + " : " + str(months_mean))


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

    mean(
        reference_spreadsheets.iloc[
            :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ]
    )


if __name__ == "__main__":
    run()