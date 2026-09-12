"""Sphinx configuration for perfect_maze."""

from importlib.metadata import version as _dist_version

project = "perfect_maze"
copyright = "2015-2026, Michaël Launay"
author = "Michaël Launay"
release = _dist_version("perfect-maze")
version = ".".join(release.split(".")[:2])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {"members": True, "undoc-members": False}
napoleon_google_docstring = True
napoleon_numpy_docstring = False
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "alabaster"
html_static_path: list[str] = []
