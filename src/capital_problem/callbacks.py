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
    @app.callback(Output(graph.id, "figure"), Input(graph.id, event))
    def display_click_data(clickData):
        if (
            clickData
            and clickData.get("points")
            and clickData.get("points")[0].get("pointIndex")
        ):
            x_axis = graph.figure.data[0].x
            range_min = int(clickData.get("points")[0].get("pointIndex")) - granularity
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

        return graph.figure
