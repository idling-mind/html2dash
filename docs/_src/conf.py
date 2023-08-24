#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from html2dash import __version__

__title__ = "html2dash"
__author__ = "Najeem Muhammed"
__description__ = "Convert an html layout to a dash layout"

from datetime import datetime

tls_verify = False
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_click",
]

autosummary_generate = True
autoclass_content = "both"
add_module_names = False
autosummary_imported_members = True
autodoc_default_options = {
    "members": True,
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = __title__
copyright = f"{datetime.now().year}, {__author__}"
author = __author__

version = __version__
# The full version, including alpha/beta/rc tags.
release = __version__

exclude_patterns = ["_build", "**.ipynb_checkpoints"]

pygments_style = "sphinx"

todo_include_todos = True


html_theme = "furo"
html_title = f"{__title__} v{__version__}"
html_logo = ""
html_theme_options = {
    "navigation_with_keys": True,
}
html_static_path = ["_static"]
htmlhelp_basename = f"{__title__}doc"
latex_elements = {
}
latex_documents = [
    (
        master_doc,
        f"{__title__}.tex",
        f"{__title__} Documentation",
        __author__,
        "manual",
    ),
]
man_pages = [
    (master_doc, __title__, f"{__title__} Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        __title__,
        f"{__title__} Documentation",
        author,
        __title__,
        __description__,
        "Miscellaneous",
    ),
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
