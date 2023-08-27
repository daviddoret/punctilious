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
    'sphinx_autodoc_typehints', 'sphinx.ext.graphviz', 'sphinxawesome_theme', 'sphinx_togglebutton']
# 'sphinx_exec_code',
bibtex_bibfiles = ['bibliography_bibtex.bib']
bibtex_encoding = 'utf-8-sig'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinxawesome_theme'
html_static_path = ['_static']

html_css_files = ['css/custom.css', ]

# sphinx-exec-code
# URL: https://sphinx-exec-code.readthedocs.io/en/latest/configuration.html#installation
# exec_code_set_utf8_encoding: True  # enforces utf-8 encoding (can fix encoding errors). Default is False except on Windows where it is True.
# exec_code_working_dir = '../../sample/working_dir'
# exec_code_source_folders = ['../..']
# exec_code_example_dir = '../../sample'
