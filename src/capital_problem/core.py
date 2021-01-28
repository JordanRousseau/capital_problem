from numpy.core.arrayprint import str_format
from numpy.lib import index_tricks
import pandas
from decouple import config
import numpy
import dashboard
import summary
import datetime
import callbacks


def get_stacked_temperatures(dataframe: pandas.DataFrame, print_: bool = False):
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
        var_name="Month",
        value_name="Temperature",
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

    # Replace month name by month locale's full name
    reference_spreadsheets.columns = header_month_convertor(
        reference_spreadsheets.columns.values
    )

    # Rename day column
    reference_spreadsheets.columns = header_column_rename(
        reference_spreadsheets.columns.values, "Day", int(config("DAY_COL_INDEX"))
    )

    if print_:
        print(reference_spreadsheets)

    return reference_spreadsheets


def header_month_convertor(header_list: list):
    """Convert header month to locale's full name

    Args:
        header_list (list, required): header list param to convert the month.

    Returns:
        pandas.DataFrame: header list
    """
    for key, month_index in enumerate(
        list(map(int, str(config("MONTH_COLUMNS")).split(","))), start=1
    ):
        header_list[month_index] = datetime.date(1900, key, 1).strftime("%B")

    return header_list


def header_column_rename(header_list: list, column_name: str, column_index: int):
    """Rename column with a name

    Args:
        header_list (list, required): header list param to convert the month.
        column_name (str, required): New name for the column
        column_index (int, required): index of the column

    Returns:
        pandas.DataFrame: header list
    """
    header_list[column_index] = column_name

    return header_list


def create_date_column(year: pandas.Series, month: pandas.Series, day: pandas.Series):
    return pandas.to_datetime(
        year.astype(str) + "-" + month.astype(str) + "-" + day.astype(str),
        format="%Y-%B-%d",
        errors="coerce",
    )


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
    stacked_temperatures = get_stacked_temperatures(
        reference_spreadsheets, print_=debug
    )
    # Create year column
    stacked_temperatures["Year"] = 2018
    stacked_temperatures["full_date"] = create_date_column(
        stacked_temperatures["Year"],
        stacked_temperatures["Month"],
        stacked_temperatures["Day"],
    )

    stacked_temperatures = stacked_temperatures[
        pandas.notna(stacked_temperatures["full_date"])
    ]

    visual_year_summary = dashboard.build_card_group(
        year_summary_without_meaning, "year-cards"
    )
    visual_months_summary = dashboard.build_table_component(
        headers=month_summary.get("summary_headers", []),
        data=month_summary.get("summary_data", []),
        id="summary-table",
    )
    visual_monthly_graph = dashboard.build_time_series_chart(
        id="monthly-graph",
        dates=reference_spreadsheets["Day"],
        data_list=[
            reference_spreadsheets[column]
            for column in reference_spreadsheets.iloc[
                :, list(map(int, str(config("MONTH_COLUMNS")).split(",")))
            ]
        ],
        layout={
            "title": "Monthly temperatures",
            "xaxis": {"title": "Day"},
            "yaxis": {"title": "Temperature in °C"},
        },
    )
    visual_annual_graph = dashboard.build_time_series_chart(
        id="annual-graph",
        dates=stacked_temperatures["full_date"],
        data_list=[stacked_temperatures["Temperature"]],
        layout={
            "title": "Annual temperatures",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Temperature in °C"},
            "dragmode": "pan",
        },
    )
    visual_annual_graph_zoom = dashboard.build_time_series_chart(
        id="annual-graph-zoom",
        dates=stacked_temperatures["full_date"],
        data_list=[stacked_temperatures["Temperature"]],
        layout={
            "title": "Annual temperatures",
            "xaxis": {
                "title": "Date",
                "range": [
                    stacked_temperatures["full_date"][0],
                    stacked_temperatures["full_date"][29],
                ],
            },
            "yaxis": {"title": "Temperature in °C"},
        },
    )

    report = dashboard.build_app_report(
        [
            visual_year_summary,
            visual_months_summary,
            visual_monthly_graph,
            visual_annual_graph,
            visual_annual_graph_zoom,
        ]
    )

    callbacks.zoom_in_dates_graph(
        graph=visual_annual_graph_zoom, app=report, event="clickData", granularity=15
    )

    report.run_server(debug=debug)


if __name__ == "__main__":
    run()