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
    stats_SI = content.get_statistics(sheet_name=config("CLIMATE_SHEET_SI"), print_=debug)
    stats_SI_ERRORS = content.get_statistics(sheet_name=config("CLIMATE_SHEET_SI_ERROR"), print_=debug)

    report = dashboard.build_app_report(
        si_dash_components_list = dash_html_components.Div(
            id='si-container',
            children=[
                stats_SI['year_summary'],
                stats_SI['month_summary'],
                stats_SI['monthly_graph'],
                stats_SI['annual_graph'],
            ],
            className="visuals"
        ),
        si_error_dash_components_list = dash_html_components.Div(
            id='si-error-container',
            children= [
                stats_SI_ERRORS['year_summary'],
                stats_SI_ERRORS['month_summary'],
                stats_SI_ERRORS['monthly_graph'],
                stats_SI_ERRORS['annual_graph']
            ],
            className="visuals"
        )
    )

    callbacks.zoom_in_dates_graph(
        graph=stats_SI['annual_graph'], app=report, event="selectedData", granularity=15
    )

    callbacks.zoom_in_dates_graph(
        graph=stats_SI_ERRORS['annual_graph'], app=report, event="selectedData", granularity=15
    )

    report.run_server(debug=debug)


if __name__ == "__main__":
    run()