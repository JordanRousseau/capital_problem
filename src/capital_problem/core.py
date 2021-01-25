import pandas
from decouple import config
import numpy
import dashboard
import summary


def get_reference_spreadsheets(print_: bool = False):
    """Get the reference spreadsheets

    Args:
        print_ (bool, optional): print param to print the dataframe. Defaults to True.

    Returns:
        pandas.DataFrame: reference spreadsheets
    """
    # Import XLSX
    reference_spreadsheets = pandas.read_excel(
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

    if print_:
        print(reference_spreadsheets)

    return reference_spreadsheets


def run(debug: bool = bool(int(config("DEBUG")))):
    # Get reference spreadsheets
    reference_spreadsheets = get_reference_spreadsheets(print_=debug)

    # Make mean of month columns
    month_summary = summary.column_summary(
        dataframe=reference_spreadsheets.iloc[
            :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
        ],
        print_=debug,
        columns_meaning="Months",
    )

    dashboard.build_app_report(
        [
            dashboard.build_table_component(
                headers=month_summary.get("summary_headers", []),
                data=month_summary.get("summary_data", []),
                id="summary-table",
            ),
        ]
    ).run_server(debug=debug)


if __name__ == "__main__":
    run()