# html2dash

Write your dash layout in html/xml form.

## Why does this package exist?

Dash is a great framework for building web apps using only python (no html/css/
javascript). If you have used dash long enough, you must have noticed some of the
following.

- For larger layouts, the python code becomes very long and hard to read.
- Sometimes I get the html form of a class (like pandas dataframe), but I
  cannot easily display that in dash.
- Use html from markdown parsers
- Cannot copy paste html code from examples on the web.
- Cannot use tools like emmet to generate html code.

html2dash solves these problems by allowing you to write your dash layout in
html/xml form. It converts the html/xml code to equivalent dash layout code.

## Installation

```bash
pip install html2dash
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

You can change the list of modules that `html2dash` searches for tags by
passing in `module_list` argument.

```python
from dash import Dash, html, dcc
from html2dash import html2dash
import dash_mantine_components as dmc

modules = [html, dcc, dmc]

layout = html2dash("""
<div>
    <h1>Hello World</h1>
    <p>This is a paragraph</p>
    <div>
        <Badge>Default</Badge>
        <Badge variant="outline">Outline</Badge>
    </div>
</div>
""", module_list=modules)
```

You can also map html tags to dash components. For example, if you dont want to
use `<icon>` tag, you can map it to `DashIconify` as follows.

```python
from html2dash import html2dash
from dash_iconify import DashIconify

element_map = {"icon": DashIconify}

layout = html2dash("""
<div>
    <h1>Icon example</h1>
    <icon icon="mdi:home"/>
</div>
""", element_map=element_map)
```

The `element_map` is a dictionary that maps html tags to dash components.
The `element_map` will be searched first before searching in the `module_list`.

The mapped component does not have to be a dash component. It can be any
function that takes `children` and `**kwargs` as arguments and returns a dash
component.

```python
from html2dash import html2dash

def my_component(children, **kwargs):
    return html.Div(children=children, **kwargs)

element_map = {"my-component": my_component}

layout = html2dash("""
<div>
    <h1>My component</h1>
    <my-component id="my-component">
        <h2>My component</h2>
        <p>This is my component</p>
    </my-component>

    <my-component id="my-component-2">
        <h2>My component 2</h2>
        <p>This is my component 2</p>
    </my-component>
</div>
""", element_map=element_map)
```

## Example usecase: Display a pandas dataframe in dash

Since pandas dataframes come with a `to_html` method, you can easily display
them in dash using `html2dash`.

```python
import pandas as pd
from html2dash import html2dash

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
layout = html2dash(df.to_html())
```

If you want to use `dash_mantine_components` to display the dataframe, you can
do the following.

```python
import pandas as pd
from html2dash import html2dash
import dash_mantine_components as dmc

# <table> would have been mapped to dash.html.Table
# But, we want to use dmc.Table instead.
element_map = {"table": dmc.Table}

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
layout = html2dash(df.to_html(), element_map=element_map)
```

`html2dash` can handle multi-index dataframes as well.

```python
import pandas as pd
from html2dash import html2dash, settings
import dash_mantine_components as dmc

df = pd.DataFrame(
    {
        ("a", "b"): [1, 2, 3],
        ("a", "c"): [4, 5, 6],
        ("d", "e"): [7, 8, 9],
    }
)

element_map = {"table": dmc.Table}

layout = html2dash(df.to_html(), element_map=element_map)
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