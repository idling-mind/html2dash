# html2dash

Write your dash layout in html/xml form.

## Why does this package exist?

Dash is a great framework for building web apps using only python (no html/css/
javascript). If you have used dash long enough, you must have noticed some of the
following.

- For larger layouts, the python code becomes very long and hard to read.
- Cannot copy paste html code from examples on the web.
- Cannot use tools like emmet to generate html code.

html2dash solves these problems by allowing you to write your dash layout in
html/xml form. It converts the html/xml code to equivalent dash layout code.

## Installation

```bash
git clone https://github.com/idling-mind/html2dash.git
cd html2dash
pip install .
```

## Examples

Here is a simple example:

```python
from dash import Dash
from html2dash import html2dash

app = Dash(__name__)

layout = """
<div>
    <h1>Hello World</h1>
    <p>This is a paragraph</p>
    <div>
        <h2>Subheading</h2>
        <p>Another paragraph</p>
    </div>
</div>
"""

app.layout = html2dash(layout)
```

You can define attributes like `id`, `class`, `style` etc. These
will be converted to equivalent dash attributes. For example:

```python
layout = """
<div id="my-div" class="my-class" style="color: red;">
    <h1>Hello World</h1>
    <p>This is a paragraph</p>
    <div>
        <h2>Subheading</h2>
        <p>Another paragraph</p>
    </div>
</div>
"""
```

This is equivalent to:

```python
layout = html.Div(
    id="my-div",
    className="my-class",
    style={"color": "red"},
    children=[
        html.H1("Hello World"),
        html.P("This is a paragraph"),
        html.Div(
            children=[
                html.H2("Subheading"),
                html.P("Another paragraph"),
            ]
        )
    ]
)
```

You can use any html tag that appears in `dash.html` module. If `html2dash` does
not find the tag in `dash.html`, it will search in the `dash.dcc` module.

```python
from html2dash import html2dash

layout = html2dash("""
<div>
    <h1>Hello World</h1>
    <p>This is a paragraph</p>
    <Input id="my-input" value="Hello World" />
</div>
""")
```

Here, `Input` is not found in `dash.html` module. So, it will search in `dash.dcc`
module and find `dcc.Input` and convert it to `dcc.Input(id="my-input", value="Hello World")`.

The order in which `html2dash` searches for tags is:

1. `dash.html`
2. `dash.dcc`

You can add additional component libraries to the module list as follows.

```python
from html2dash import html2dash, settings
import dash_mantine_components as dmc

# settings["modules"] is a list of modules to search for tags.
# Default value is [html, dcc]
settings["modules"].append(dmc)

layout = html2dash("""
<div>
    <h1>Hello World</h1>
    <p>This is a paragraph</p>
    <div>
        <Badge>Default</Badge>
        <Badge variant="outline">Outline</Badge>
    </div>
</div>
""")
```

You can also map html tags to dash components. For example, if you dont want to
use `<icon>` tag, you can map it to `DashIconify` as follows.

```python
from html2dash import html2dash, settings
from dash_iconify import DashIconify

settings["element-map"]["icon"] = DashIconify

layout = html2dash("""
<div>
    <h1>Icon example</h1>
    <icon icon="mdi:home"/>
</div>
""")
```

## Case sensitivity of html tags

html tags are case insensitive. So, `<div>` and `<DIV>` are equivalent. But,
html2dash is partly case sensitive. For any tag, it first tries to find the tag
with the given case. If it does not find the tag, it tries to find the tag with
the first letter capitalized.

For example, if you have the following layout:

```python
layout = html2dash("""
<div>
    <h1>Hello World</h1>
    <p>This is a paragraph</p>
    <input id="my-input" value="Hello World"/>
</div>
""")
```

In the above, all tags except `input` are found in `dash.html` module. 
And for input tag, the following will be the sequence of searches:

1. Search for `input` in `dash.html` >> Not found
2. Search for `Input` in `dash.html` >> Not found
3. Search for `input` in `dash.dcc` >> Not found
4. Search for `Input` in `dash.dcc` >> Found