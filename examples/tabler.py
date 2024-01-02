from pathlib import Path
from dash import Dash, html, dcc
from html2dash import html2dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

modules = [html, dcc, dmc]
element_map = {}
element_map["icon"] = DashIconify
element_map["rprogress"] = dmc.RingProgress
element_map["lprogress"] = dmc.Progress

app = Dash(
    __name__,
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/js/tabler.min.js"
    ],
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/css/tabler.min.css",
        "https://rsms.me/inter/inter.css",
    ],
)

app.layout = html2dash(
    Path("tabler.html").read_text(), module_list=modules, element_map=element_map
)

if __name__ == "__main__":
    app.run_server(debug=True)
