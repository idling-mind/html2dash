from pathlib import Path
from dash import Dash
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

if __name__ == "__main__":
    app.run_server(debug=True)
