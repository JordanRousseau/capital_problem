import dash
import dash_core_components
import dash_html_components
from dash_html_components.Div import Div
import dash_table
import dash_bootstrap_components
import pandas
import plotly.graph_objects
import json
from decouple import config


def build_app_report(
    si_dash_components_list: list,
    si_error_dash_components_list: list,
    alternate_dash_components_list: list,
):
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

    app.layout = dash_html_components.Div(
        children=[
            dash_html_components.Div(
                children=[
                    dash_html_components.P(children="🌤", className="header-emoji"),
                    dash_html_components.H1(
                        children="Capital's Climate Problem", className="header-title"
                    ),
                    dash_html_components.P(
                        children="Resolve a capital's climate problem by Simon Huet & Théo Levalet.",
                        className="header-description",
                    ),
                    dash_html_components.P(
                        children="Compare two climate datasets to find the european capital for which temperatures are provided in the file Climate.xlsx. We will use the file Savukoskikirkonkyla.xlsx from open data as a reference.",
                        className="header-description",
                    ),
                ],
                className="header",
            ),
            dash_core_components.Tabs(
                id="data-selector-tabs",
                value="tab-1",
                children=[
                    dash_core_components.Tab(
                        label="SI",
                        value="tab-1",
                        children=dash_html_components.Div(
                            children=si_dash_components_list,
                            className="visuals",
                        ),
                    ),
                    dash_core_components.Tab(
                        label="SI-erreur",
                        value="tab-2",
                        children=dash_html_components.Div(
                            children=si_error_dash_components_list,
                            className="visuals",
                        ),
                    ),
                    dash_core_components.Tab(
                        label="Resolution",
                        value="tab-3",
                        children=dash_html_components.Div(
                            children=alternate_dash_components_list,
                            className="visuals",
                        ),
                    ),
                ],
            ),
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


def build_card_group(data_dict: dict, id: str):
    return dash_html_components.Div(
        children=[
            dash_bootstrap_components.Card(
                children=dash_bootstrap_components.CardBody(
                    [
                        dash_html_components.H4(
                            str(
                                round(element, 2)
                                if type(element) == int or float
                                else element
                            ),
                            className="card-title",
                        ),
                        dash_html_components.H6(str(key), className="card-subtitle"),
                    ]
                ),
                className="card-" + str(key),
            )
            for key, element in data_dict.items()
        ],
        className="summary-cards",
    )


def build_time_series_chart(
    dates: pandas.Series, data_list: list, layout: dict, id: str, all_: bool = False
):
    graph_figure = plotly.graph_objects.Figure(layout=layout)

    for key, data in enumerate(data_list, start=0):
        graph_figure.add_trace(
            trace=plotly.graph_objects.Scatter(
                x=dates,
                y=data,
                mode="lines+markers",
                line_shape="spline",
                name=data.name,
                visible="legendonly" if key and not all_ else None,
            )
        )

    graph_figure.update_layout(clickmode="event+select")

    return dash_core_components.Graph(animate=True, figure=graph_figure, id=id)


if __name__ == "__main__":
    build_app_report(dash_components_list=[]).run_server(debug=True)


def map_display():
    with open("src/capital_problem/assets/capitals.geojson") as file:
        data = json.loads(file.read())

    if data:
        dataframe = pandas.DataFrame({"col1": ["FR", "GB"], "col2": [3, 4]})

        thelist = data["features"]
        locations = [item["id"] for item in thelist]

        mapboxt = config("MAP_TOKEN")

        figure = plotly.graph_objects.Figure(
            plotly.graph_objects.Choropleth(
                z=dataframe,  # This is the data.
                geojson=data,
                locations=locations,
                colorscale="reds",
                colorbar=dict(thickness=20, ticklen=3),
                text=locations,
                hoverinfo="all",
                marker_line_width=1,
                marker_opacity=0.75,
            )
        )
        figure.update_layout(
            height=300,
            mapbox=dict(
                accesstoken=mapboxt,
                style="basic",
            ),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )
        return dash_core_components.Graph(id="yolo", figure=figure)