"""html2dash

Converts HTML to Dash components.

Usage:
    from html2dash import html2dash
    app.layout = html2dash(Path("layout.html").read_text())

"""
from __future__ import annotations
from typing import Mapping
from bs4 import BeautifulSoup, element, Comment
from dash import html, dcc
import re
import logging
import json

logger = logging.getLogger(__name__)

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


def html2dash(
    html_str: str,
    module_list: list | None = None,
    element_map: Mapping[str, object] | None = None,
    parent_div: bool = True,
    on_missing_element: str = "warn",
    on_missing_attribute: str = "warn",
) -> html.Div | list[object]:
    """Convert the HTML string to dash components.

    Args:
        html_str (str): The HTML string to convert.
        module_list (list, optional): A list of modules to search for elements.
            Defaults to [html, dcc].
        element_map (dict, optional): A dictionary mapping HTML elements to dash
            components. Defaults to {}.
        parent_div (bool, optional): Whether to enclose the converted Dash components
        on_missing_element (str, optional): What to do when an element is not found.
            Defaults to "warn". Can be "warn", "raise", or "ignore".
        on_missing_attribute (str, optional): What to do when an attribute is not found.
            Defaults to "warn". Can be "warn", "raise", or "ignore".

    Returns:
        html.Div: The converted Dash components enclosed inside a html.Div object.
    """
    html_str_iter = f"<body>{html_str}</body>"
    soup = BeautifulSoup(html_str_iter, "xml")
    if soup.body is not None:
        soup = soup.body
    if module_list is None:
        module_list = [html, dcc]
    if element_map is None:
        element_map = {}
    settings = {
        "module-list": module_list,
        "element-map": element_map,
        "on-missing-element": on_missing_element,
        "on-missing-attribute": on_missing_attribute,
    }
    children = [parse_element(child, **settings) for child in soup.children]  # type: ignore
    if parent_div:
        return html.Div(children=children)
    return children


def parse_element(tag: element.Tag, **settings) -> object:
    """Parse the HTML element and return the Dash component.

    Args:
        tag (element.Tag): The HTML element to parse.
        settings (dict): The settings to use.

    Returns:
        object: The Dash component.
    """
    if tag is None or isinstance(tag, Comment):
        return None
    elif isinstance(tag, element.NavigableString):
        text = str(tag)
        if text.strip():
            return text
        return None
    dash_element = None
    for module in settings.get("module-list", []):
        mapped_element = settings["element-map"].get(tag.name)
        if mapped_element is not None:
            dash_element = mapped_element
            break
        elif hasattr(module, tag.name):
            dash_element = getattr(module, tag.name)
            break
        elif hasattr(module, tag.name.title()):
            dash_element = getattr(module, tag.name.title())
            break
    if not dash_element:
        if settings.get("on-missing-element") == "warn":
            logger.warning(
                f"Could not find the element '{tag.name}'" f" in any of the modules."
            )
        elif settings.get("on-missing-element") == "raise":
            raise ValueError(
                f"Could not find the element '{tag.name}'" f" in any of the modules."
            )
        return None
    attrs = {k: v for k, v in tag.attrs.items()}
    attrs = fix_attrs(attrs)
    children = []
    for child in tag.children:
        child_object = parse_element(child, **settings)  # type: ignore
        if child_object is not None:
            children.append(child_object)
    if children:
        attrs["children"] = children
    while True:
        try:
            return dash_element(**attrs)
        except TypeError as e:
            match = re.search(
                r"received an unexpected keyword argument: `(.*)`", str(e)
            )
            if match is None:
                raise e
            attrs.pop(match.group(1))
            if settings["on-missing-attribute"] == "warn":
                logger.warning(
                    f"Removed the attribute '{match.group(1)}' from the element '{tag.name}'"
                    f" because it was not valid."
                )
            elif settings.get("on-missing-attribute") == "raise":
                raise ValueError(
                    f"Unrecognized attribute '{match.group(1)}' in the element '{tag.name}'"
                )


def fix_attrs(attrs: dict) -> dict:
    """Fix the attributes to be valid Dash attributes.

    Args:
        attrs (dict): The attributes to fix.

    Returns:
        dict: The fixed attributes.
    """
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
    """Fix the hyphenated attribute to be camel case.

    Args:
        attr (str): The attribute to fix.

    Returns:
        str: The fixed attribute.
    """
    return re.sub(r"-(\w)", lambda m: m.group(1).upper(), attr)


def style_str_to_dict(style_str: str) -> dict:
    """Convert the style string to a dictionary.

    Args:
        style_str (str): The style string to convert.

    Returns:
        dict: The converted style dictionary.
    """
    style_dict = {}
    for item in style_str.split(";"):
        if ":" in item:
            key, value = item.split(":")
            style_dict[fix_hyphenated_attr(key.strip())] = value.strip()
    return style_dict
