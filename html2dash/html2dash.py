from bs4 import BeautifulSoup, element, Comment
from dash import html, dcc
import re
import logging

element_modules = [html, dcc]


def html2dash(html_str: str, fallback=None) -> html.Div:
    if fallback is None:
        fallback = []
    soup = BeautifulSoup(html_str, "html.parser")
    children = [parse_element(child, fallback) for child in soup.children]
    return html.Div(children=children)


def parse_element(tag: element.Tag, fallback=None):
    if fallback is None:
        fallback = []
    if tag is None:
        return str(tag)
    elif isinstance(tag, Comment):
        return None
    elif isinstance(tag, element.NavigableString):
        return str(tag).strip()
    attrs = {k: v for k, v in tag.attrs.items()}
    attrs = fix_attrs(attrs)
    children = []
    for child in tag.children:
        child_object = parse_element(child)
        if child_object is not None:
            children.append(child_object)
    if children:
        attrs["children"] = children
    for module in element_modules:
        if hasattr(module, tag.name.title()):
            return getattr(module, tag.name.title())(**attrs)
    logging.warning(
        f"Could not find the element '{tag.name}'"
        f" in any of the modules."
    )


def fix_attrs(attrs: dict) -> dict:
    return_attrs = {}
    for k, v in attrs.items():
        if k == "class":
            return_attrs["className"] = " ".join(v)
        elif k == "style":
            return_attrs[k] = style_str_to_dict(v)
        elif k == "for":
            return_attrs["htmlFor"] = v
        elif k == "autocomplete":
            return_attrs["autoComplete"] = v
        elif k == "tabindex":
            return_attrs["tabIndex"] = v
        elif k == "novalidate":
            return_attrs["noValidate"] = bool(v)
        elif k.startswith("data-") or k.startswith("aria-"):
            return_attrs[k] = v
        elif isinstance(v, list):
            return_attrs[k] = " ".join(v)
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
