from pathlib import Path
from dash import Dash, callback, Input, Output, State
from html2dash import html2dash

app = Dash(
    __name__,
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/js/tabler.min.js"
    ],
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/css/tabler.min.css"
    ]
)

app.layout = html2dash(Path("layout.html").read_text())


if __name__ == "__main__":
    app.run_server(debug=True)
