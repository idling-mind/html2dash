from dash import Dash, callback, Input, Output, State
from html2dash import html2dash

app = Dash(
    __name__,
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/js/tabler.min.js"
    ],
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/css/tabler.min.css",
    ],
)

app.layout = html2dash(
    """
    <div class="col">
                <!-- Page pre-title -->
                <div class="page-pretitle">
                  Overview
                </div>
                <h2 class="page-title">
                  Dashboard
                </h2>
              </div>
    <div>
        <h1>Hello World</h1>
        <p>This is a paragraph</p>
        <p id="callback">This is another paragraph</p>
        <button id="button">Click me</button>
    </div>
    """
)


@callback(
    Output("callback", "children"),
    Input("button", "n_clicks"),
)
def callback(n_clicks):
    return f"Button clicked {n_clicks} times"


if __name__ == "__main__":
    app.run_server(debug=True)
