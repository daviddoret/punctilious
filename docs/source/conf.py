import os
import sys

# Add the root folder (where punctilious/ lives) to sys.path
sys.path.insert(0, os.path.abspath('../../src'))
print(sys.path)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Punctilious'
copyright = '2025, David Doret'
author = 'David Doret'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_autodoc2',
    'sphinx.ext.napoleon',  # if using Google or NumPy-style docstrings
    'sphinx.ext.viewcode',  # optional: link to source code
    'sphinx.ext.mathjax',  # Enables math rendering in HTML
    'sphinx.ext.imgmath',  # Generates images of equations
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# Enable autodoc to generate separate pages
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'member-order': 'bysource',
    'special-members': '__init__',  # Include __init__ if needed
}

# Enable separate pages for each function/class
autodoc_member_order = 'bysource'  # Keep members in source order
autodoc_typehints = 'description'  # Show type hints
