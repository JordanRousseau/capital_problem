import dash
import dash_core_components
import dash_html_components
import dash_table
import dash_bootstrap_components
import pandas
import plotly.graph_objects
import json
from dash.dependencies import Input, Output


def zoom_in_dates_graph(
    graph: dash_core_components.Graph, app, event, granularity: int
):
    # Store the previous state on the page
    app.layout.children.append(
        dash_html_components.Div(
            id=graph.id + "-previous-state", style={"display": "none"}
        )
    )

    @app.callback(
        Output(graph.id, "figure"),
        Output(graph.id + "-previous-state", "children"),
        Input(graph.id, event),
        Input(graph.id + "-previous-state", "children"),
    )
    def display_click_data(clickData, previous_state):

        previous = None

        # Parse jsonify previous state
        if previous_state:
            previous = json.loads(previous_state)

        x_axis = graph.figure.data[0].x

        if previous and previous == clickData or (previous and not clickData):
            # Click on the same point or unselect : unzoom and reset previous state
            graph.figure.update_layout({"xaxis": {"range": [x_axis[0], x_axis[-1]]}})
            previous = None
        else:
            # Click on a point : update the range
            if (
                clickData
                and clickData.get("points")
                and clickData.get("points")[0].get("pointIndex")
            ):
                range_min = (
                    int(clickData.get("points")[0].get("pointIndex")) - granularity
                )
                range_max = (
                    int(clickData.get("points")[0].get("pointIndex"))
                    + granularity
                    - (range_min if range_min < 0 else 0)
                )
                range_min -= range_max if range_max > len(x_axis) else 0
                range_min = range_min if range_min > 0 else 0
                range_max = range_max if range_max < len(x_axis) else len(x_axis) - 1

                graph.figure.update_layout(
                    {"xaxis": {"range": [x_axis[range_min], x_axis[range_max]]}}
                )
            previous = clickData

        return graph.figure, json.dumps(previous)
