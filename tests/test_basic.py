from dash import html
from html2dash import html2dash


def test_html2dash_empty():
    assert html2dash("").to_plotly_json() == html.Div([]).to_plotly_json()


