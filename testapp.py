from pathlib import Path
from dash import Dash, callback, Input, Output, State
from html2dash import html2dash, settings
import dash_mantine_components as dmc
from dash_iconify import DashIconify

settings["modules"].append(dmc)
settings["element-map"]["icon"] = DashIconify
settings["element-map"]["rprogress"] = dmc.RingProgress
settings["element-map"]["lprogress"] = dmc.Progress

app = Dash(
    __name__,
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/js/tabler.min.js"
    ],
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/css/tabler.min.css",
        "https://rsms.me/inter/inter.css",
    ]
)

app.layout = html2dash(Path("tabler.html").read_text())

# @callback(
#     Output("checkbox_output", "children"),
#     Input("checkbox", "checked"),
# )
# def checkbox_output(checked):
#     if checked:
#         return f"Checkbox is {checked}"
#     return f"Checkbox is {checked}"

# @callback(
#     Output("lprogress", "sections"),
#     Input("button", "n_clicks"),
# )
# def lprogress(n_clicks):
#     if not n_clicks:
#         return [
#             {"value": 10, "color": "blue", "tooltip": "10 blue"},
#         ]
#     return [
#         {"value": 10, "color": "blue", "tooltip": "10 blue"},
#         {"value": 10, "color": "green", "tooltip": "10 green"},
#         {"value": 20, "color": "yellow", "tooltip": "20 yellow"},
#     ]

if __name__ == "__main__":
    app.run_server(debug=True)
