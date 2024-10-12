# Configuration file for the Sphinx documentation builder.
import datetime
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("../../."))

# Load version
root_path = Path(__file__).parents[2]
version_file_path = root_path / "fauxpy" / "version.py"
__version__ = ""
exec(version_file_path.read_text())
assert __version__ != ""
print(__version__)

# -- Project information

project = "FauxPy"
author = "Mohammad Rezaalipour"
copyright = f"2023-{datetime.date.today().year}, {author}"

release = __version__
version = __version__

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"
