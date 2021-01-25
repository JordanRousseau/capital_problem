import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy


def build_app_report(dash_components_list: list):
    external_stylesheets = [
        {
            "href": "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@100;400;700&display=swap",
            "rel": "stylesheet",
        },
    ]
    app = dash.Dash(
        __name__, external_stylesheets=external_stylesheets, assets_url_path="/assets/"
    )
    app.title = "Capital's Climate Problem"

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
            html.Div(children=dash_components_list, className="visuals"),
        ]
    )

    return app


def build_table_component(headers: list, data: list, id: str):
    # need to check dimensions
    return dash_table.DataTable(
        id=id,
        columns=[
            {"name": name, "id": "col-" + str(index)}
            for index, name in enumerate(headers, start=0)
        ],
        data=[
            {"col-" + str(index): value for index, value in enumerate(row, start=0)}
            for row in data
        ],
        style_as_list_view=True,
    )


if __name__ == "__main__":
    build_app_report(dash_components_list=[]).run_server(debug=True)