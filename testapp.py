from pathlib import Path
from dash import Dash, callback, Input, Output, State
from html2dash import html2dash

app = Dash(
    __name__,
    external_scripts=[
        "https://cdn.tailwindcss.com"
    ],
)

app.layout = html2dash(Path("layout.html").read_text())


if __name__ == "__main__":
    app.run_server(debug=True)
