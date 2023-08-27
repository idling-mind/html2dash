"""html2dash

Converts HTML to Dash components.

Usage:
    from html2dash import html2dash, settings
    settings["modules"] = [html, dcc] + settings["modules"]
    app.layout = html2dash(Path("layout.html").read_text())

"""
from bs4 import BeautifulSoup, element, Comment
from dash import html, dcc
import re
import logging
import json

logger = logging.getLogger(__name__)

settings = {
    "modules": [html, dcc],
    "element-map": {},
}

ATTRIBUTE_MAP = {
    "autocomplete": "autoComplete",
    "autofocus": "autoFocus",
    "class": "className",
    "colspan": "colSpan",
    "for": "htmlFor",
    "maxlength": "maxLength",
    "minlength": "minLength",
    "novalidate": "noValidate",
    "readonly": "readOnly",
    "rowspan": "rowSpan",
    "tabindex": "tabIndex",
}


def html2dash(html_str: str) -> html.Div:
    soup = BeautifulSoup(html_str, "xml")
    if soup.body is not None:
        soup = soup.body
    children = [parse_element(child) for child in soup.children]
    return html.Div(children=children)


def parse_element(tag: element.Tag):
    if tag is None or isinstance(tag, Comment):
        return None
    elif isinstance(tag, element.NavigableString):
        text = str(tag)
        if text.strip():
            return text
        return None
    dash_element = None
    for module in settings["modules"]:
        mapped_element = settings["element-map"].get(tag.name)
        if mapped_element is not None:
            dash_element = mapped_element
        elif hasattr(module, tag.name):
            dash_element = getattr(module, tag.name)
        elif hasattr(module, tag.name.title()):
            dash_element = getattr(module, tag.name.title())
    if not dash_element:
        logger.warning(
            f"Could not find the element '{tag.name}'" f" in any of the modules."
        )
        return None
    attrs = {k: v for k, v in tag.attrs.items()}
    attrs = fix_attrs(attrs)
    children = []
    for child in tag.children:
        child_object = parse_element(child)
        if child_object is not None:
            children.append(child_object)
    if children:
        attrs["children"] = children
    return dash_element(**attrs)


def fix_attrs(attrs: dict) -> dict:
    return_attrs = {}
    for k, v in attrs.items():
        if v in ["true", "false"]:
            v = eval(v.title())
        if k == "style":
            return_attrs[k] = style_str_to_dict(v)
        elif k in ATTRIBUTE_MAP:
            return_attrs[ATTRIBUTE_MAP[k]] = v
        elif k.startswith("data-") or k.startswith("aria-"):
            return_attrs[k] = v
        elif isinstance(v, list):
            return_attrs[k] = " ".join(v)
        else:
            if isinstance(v, str) and any([s in v for s in ["{", "["]]):
                try:
                    return_attrs[fix_hyphenated_attr(k)] = json.loads(v)
                except Exception:
                    return_attrs[fix_hyphenated_attr(k)] = v
            else:
                return_attrs[fix_hyphenated_attr(k)] = v
    return return_attrs


def fix_hyphenated_attr(attr: str) -> str:
    return re.sub(r"-(\w)", lambda m: m.group(1).upper(), attr)


def style_str_to_dict(style_str: str) -> dict:
    """Convert the style string to a dictionary."""
    style_dict = {}
    for item in style_str.split(";"):
        if ":" in item:
            key, value = item.split(":")
            style_dict[fix_hyphenated_attr(key.strip())] = value.strip()
    return style_dict
