import dash_html_components
from decouple import config
import dashboard
import callbacks
import content


def run(debug: bool = bool(int(config("DEBUG")))):
    """core main run

    Args:
        debug (bool, optional): Parameter to run on debug. Defaults to `bool(int(config("DEBUG")))`.
    """
    stats_SI = content.get_statistics(
        sheet_name=config("CLIMATE_SHEET_SI"), print_=debug
    )
    stats_SI_ERRORS = content.get_statistics(
        sheet_name=config("CLIMATE_SHEET_SI_ERROR"), print_=debug
    )

    dtw_proof = content.get_statistics_dtw_proof(
        stacked_temperatures=[
            stats_SI["stacked_temperatures"],
            stats_SI_ERRORS["stacked_temperatures"],
        ],
        print_=debug,
    )

    stats_similarities = content.get_savukoski_statistics(
        stacked_temperatures=[
            stats_SI["stacked_temperatures"],
            stats_SI_ERRORS["stacked_temperatures"],
        ],
        print_=debug,
    )

    stats_resolution = content.get_references_statistics(
        stacked_temperatures=[
            stats_SI["stacked_temperatures"],
            stats_SI_ERRORS["stacked_temperatures"],
        ],
        print_=debug,
    )

    stats_resolution_divs = []

    if stats_resolution:
        stats_resolution_divs.append(
            dash_html_components.H2(
                "Best result is the city of " + stats_resolution[0]["name"],
                className="visuals",
            )
        )
        stats_resolution_divs.append(
            dash_html_components.P(
                "Best result is the city of "
                + stats_resolution[0]["name"]
                + " with a marvelous score of "
                + str(round(stats_resolution[0]["score"], 2))
                + ".",
                className="visuals",
            )
        )

    for key, reference in enumerate(stats_resolution, start=0):
        stats_resolution_divs.append(
            dash_html_components.Div(
                id="resolution-container-" + str(key),
                children=[
                    reference["visual_header"],
                    reference["annual_graph"],
                    reference["comparision_summary"],
                ],
                className="visuals",
            )
        )

    report = dashboard.build_app_report(
        si_dash_components_list=[
            stats_SI["year_summary"],
            stats_SI["month_summary"],
            stats_SI["monthly_graph"],
            stats_SI["annual_graph"],
        ],
        si_error_dash_components_list=[
            stats_SI_ERRORS["year_summary"],
            stats_SI_ERRORS["month_summary"],
            stats_SI_ERRORS["monthly_graph"],
            stats_SI_ERRORS["annual_graph"],
        ],
        alternate_dash_components_list=[
            dtw_proof["visual_header"],
            dtw_proof["similarities"],
            dtw_proof["annual_graph"],
            dtw_proof["comparision_summary"],
        ]
        + [
            stats_similarities["visual_header"],
            stats_similarities["similarities"],
            stats_similarities["annual_graph"],
            stats_similarities["comparision_summary"],
        ]
        + stats_resolution_divs,
    )

    callbacks.zoom_in_dates_graph(
        graph=stats_SI["annual_graph"], app=report, event="selectedData", granularity=15
    )

    callbacks.zoom_in_dates_graph(
        graph=stats_SI_ERRORS["annual_graph"],
        app=report,
        event="selectedData",
        granularity=15,
    )

    report.run_server(debug=debug)


if __name__ == "__main__":
    run()