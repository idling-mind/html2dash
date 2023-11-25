from bs4 import BeautifulSoup
from dash import html
from dash.development.base_component import Component
from html2dash import (
    html2dash,
)
from html2dash.html2dash import (
    parse_element,
    fix_hyphenated_attr,
)
from .utils import dash_to_dict


def test_is_dash_component():
    assert isinstance(html.Div(), Component)


def test_fix_hyphenated_attr():
    assert fix_hyphenated_attr("foo-bar") == "fooBar"
    assert fix_hyphenated_attr("baz-qux-quux") == "bazQuxQuux"


def test_parse_element_none():
    assert parse_element(None) is None


def test_parse_element_comment():
    assert (
        parse_element(BeautifulSoup("<!-- comment -->", "xml").comment) is None
    )


def test_html2dash_empty():
    assert html2dash("").to_plotly_json() == html.Div([]).to_plotly_json()


def test_html2dash_simple():
    a = dash_to_dict(html2dash("<div>hi</div>"))
    b = dash_to_dict(html.Div([html.Div(["hi"])]))
    assert a == b
