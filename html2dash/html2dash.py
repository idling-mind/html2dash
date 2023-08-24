from bs4 import BeautifulSoup, element
from dash import html, Dash
import re


def html2dash(html_str: str) -> html.Div:
    soup = BeautifulSoup(html_str, "html.parser")
    children = [parse_element(child) for child in soup.children]
    return html.Div(children=children)


def parse_element(tag: element.Tag):
    if tag is None:
        return str(tag)
    elif isinstance(tag, element.NavigableString):
        return str(tag).strip()
    attrs = {k: v for k, v in tag.attrs.items()}
    attrs = fix_attrs(attrs)
    children = []
    for child in tag.children:
        child_object = parse_element(child)
        if child_object:
            children.append(child_object)
    return getattr(html, tag.name.title())(children=children, **attrs)


def fix_attrs(attrs: dict) -> dict:
    return_attrs = {}
    for k, v in attrs.items():
        if k == "class":
            return_attrs["className"] = " ".join(v)
        elif k == "style":
            return_attrs[k] = v
        else:
            return_attrs[fix_hyphenated_attr(k)] = v
    return return_attrs


def fix_hyphenated_attr(attr: str) -> str:
    return re.sub(r"-(\w)", lambda m: m.group(1).upper(), attr)
