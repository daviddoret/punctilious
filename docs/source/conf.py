import os
import sys

# https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../src/punctilious'))

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
extensions = [  # 'sphinxcontrib-inlinesyntaxhighlight',
    'sphinx.ext.autodoc',  # 'sphinx-autodoc-typehints',
    'sphinx.ext.mathjax', 'sphinxcontrib.bibtex', 'sphinx_autodoc_typehints', 'sphinx.ext.graphviz',
    'sphinx_togglebutton', 'sphinx_rtd_theme', 'sphinx_favicon']
# 'sphinxawesome_theme',
# 'sphinx_exec_code',
bibtex_bibfiles = ['bibliography_bibtex.bib']
bibtex_encoding = 'utf-8-sig'
# https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html#bibliography-style
bibtex_default_style = 'alpha'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML data -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_theme = 'sphinxawesome_theme'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_css_files = ['css/custom.css', ]

# sphinx-exec-code
# URL: https://sphinx-exec-code.readthedocs.io/en/latest/configuration.html#installation
# exec_code_set_utf8_encoding: True  # enforces utf-8 encoding (can fix encoding errors). Default is False except on Windows where it is True.
# exec_code_working_dir = '../../sample/working_dir'
# exec_code_source_folders = ['../..']
# exec_code_example_dir = '../../sample'

favicons = [{'href': 'punctilious-logo-compact-light.svg'},  # => use `_static/icon.svg`
    {'href': 'punctilious-logo-compact-light-16x16-white.png'},
    {'href': 'punctilious-logo-compact-light-32x32-white.png'},
    {'rel': 'apple-touch-icon', 'href': 'punctilious-logo-compact-light-180x180-white.png', }, ]
