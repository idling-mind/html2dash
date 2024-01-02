# You'll have to install markdownit to run this example
# pip install markdown-it-py[plugins]
from dash import Dash, html, dcc
from html2dash import html2dash
import dash_mantine_components as dmc
from markdown_it import MarkdownIt
from mdit_py_plugins.attrs.index import attrs_block_plugin, attrs_plugin
from functools import partial
from dash_iconify import DashIconify

md = MarkdownIt().enable("table").use(attrs_block_plugin).use(attrs_plugin)
h = md.render(
    """
# Hello World
This is a paragraph.

{#subtitle}
## This is a subtitle with an ID
**Bold text** and *italic text*.


## This is a table

{striped=True withBorder=True}
| Name | Age |
| ---- | --- |
| John | 30  |
| Jane | 28  |

## This is a list
- Item 1
- Item 2
- Item 3

## This is a code block

{language=python withLineNumbers=True}
```python
if __name__ == "__main__":
    print("Hello World")
```

## This is a link
[Click here](https://google.com)

## This is a blockquote
> This is a blockquote

## This is a horizontal rule
---

"""
)

modules = [dmc, html, dcc]

element_map = {
    "h1": dmc.Title,
    "h2": partial(dmc.Title, order=2),
    "p": partial(dmc.Text, weight=500),
    "img": dmc.Image,
    "ul": partial(dmc.List, icon=dmc.ThemeIcon(DashIconify(icon="mdi:check"))),
    "li": dmc.ListItem,
    "code": dmc.Prism,
}

app = Dash(__name__)


app.layout = html2dash(h, module_list=modules, element_map=element_map)

if __name__ == "__main__":
    app.run_server(debug=True)
