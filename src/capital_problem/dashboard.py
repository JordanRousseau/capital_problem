import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table


def build_app_report(dash_components_list: list):
    external_stylesheets = [
        {
            "href": "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap",
            "rel": "stylesheet",
        },
    ]
    app = dash.Dash(
        __name__, external_stylesheets=external_stylesheets, assets_url_path="/assets/"
    )
    app.title = "Avocado Analytics: Understand Your Avocados!"

    app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.P(children="🌤", className="header-emoji"),
                    html.H1(
                        children="Capital's Climate Problem", className="header-title"
                    ),
                    html.P(
                        children="Resolve a capital's climate problem by Simon Huet & Théo Levalet.",
                        className="header-description",
                    ),
                    html.P(
                        children="Compare two climate datasets to find the european capital for which temperatures are provided in the file Climate.xlsx. We will use the file Savukoskikirkonkyla.xlsx from open data as a reference.",
                        className="header-description",
                    ),
                ],
                className="header",
            ),
        ]
        + dash_components_list
    )

    return app


def build_table_component(array: list):
    dash_table


if __name__ == "__main__":
    build_app_report(dash_components_list=[]).run_server(debug=True)