from numpy.lib import index_tricks
import pandas
from decouple import config
import numpy
import dashboard
import summary


def get_stacked_temperatures(dataframe: pandas.DataFrame, print_=False):
    """Stack temperatures stored in multiple columns with days represented by rows

    Args:
        dataframe (pandas.DataFrame): Dataframe with columns as month and rows as days
        print_ (bool, optional): Print param to print the dataframe. Defaults to False.

    Returns:
        pandas.DataFrame: dataframe with temperatures stacked, a column for days and a column for months
    """

    # Stack temperature
    only_temperature = pandas.melt(
        dataframe,
        id_vars=[dataframe.columns[0]],
        value_vars=[
            dataframe.columns[index]
            for index in list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ],
    )

    if print_:
        print("stack\n", only_temperature)

    return only_temperature


def get_reference_spreadsheets(print_: bool = False) -> pandas.DataFrame:
    """Get the reference spreadsheets

    Args:
        print_ (bool, optional): Print param to print the dataframe. Defaults to False.

    Returns:
        pandas.DataFrame: Reference spreadsheets
    """
    # Import XLSX
    reference_spreadsheets: pandas.DataFrame = pandas.read_excel(
        io=config("CLIMATE_PATH"),
        sheet_name=config("CLIMATE_SHEET_SI"),
        skiprows=int(config("CLIMATE_HEADER")) - 1,
        usecols=config("CLIMATE_COL_RANGE"),
    )

    # Select rows wich day on column 0 starting with 'Jn' where n is a number
    reference_spreadsheets = reference_spreadsheets[
        reference_spreadsheets.iloc[:, int(config("DAY_COL_INDEX"))].str.contains(
            "^J[0-9]+$"
        )
        == True
    ]

    # Put a trailling zero
    def pad_number(match):
        number = int(match.group(1))
        return format(number, "02d")

    reference_spreadsheets[
        reference_spreadsheets.columns[int(config("DAY_COL_INDEX"))]
    ] = reference_spreadsheets[
        reference_spreadsheets.columns[int(config("DAY_COL_INDEX"))]
    ].str.replace(
        r"^J([0-9]+)$", pad_number
    )

    if print_:
        print(reference_spreadsheets)

    return reference_spreadsheets


def run(debug: bool = bool(int(config("DEBUG")))):
    """core main run

    Args:
        debug (bool, optional): Parameter to run on debug. Defaults to `bool(int(config("DEBUG")))`.
    """
    # Get reference spreadsheets
    reference_spreadsheets = get_reference_spreadsheets(print_=debug)

    # Make summary of month columns
    month_summary = summary.column_summary(
        dataframe=reference_spreadsheets.iloc[
            :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ],
        print_=debug,
        columns_meaning="Months",
    )

    # Make a year summary
    year_summary = summary.dataframe_summary(
        dataframe=reference_spreadsheets.iloc[
            :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ],
        print_=debug,
        dataframe_meaning="Year",
    )

    year_summary_without_meaning = year_summary
    year_summary_without_meaning.pop("dataframe_meaning", None)

    # Stack all the temperatures with corresponding date
    get_stacked_temperatures(reference_spreadsheets, print_=debug)

    dashboard.build_app_report(
        [
            dashboard.build_card_group(year_summary_without_meaning, "year-cards"),
            dashboard.build_table_component(
                headers=month_summary.get("summary_headers", []),
                data=month_summary.get("summary_data", []),
                id="summary-table",
            ),
        ]
    ).run_server(debug=debug)


if __name__ == "__main__":
    run()