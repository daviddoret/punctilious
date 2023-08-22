# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'punctilious'
copyright = '2023, David Doret'
author = 'David Doret'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Bibliography configuration:
# https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html
# https://pypi.org/project/sphinxcontrib-bibtex/
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.mathjax', 'sphinxcontrib.bibtex',
    'sphinx_autodoc_typehints', 'sphinx.ext.graphviz', 'sphinxawesome_theme']
bibtex_bibfiles = ['bibliography_bibtex.bib']
bibtex_encoding = 'utf-8-sig'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinxawesome_theme'
html_static_path = ['_static']
