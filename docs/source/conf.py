# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'xit'
copyright = '2025, Medardo Antonio Rodriguez'
author = 'Medardo Antonio Rodriguez'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for sphinx.ext.intersphinx --------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

intersphinx_mapping = {
    'py': ('https://docs.python.org/', None),  # Python standard library
}

intersphinx_cache_limit = 365  # maintain the cache forever

# -- Options for sphinx.ext.autosummary --------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html

autosummary_generate = True

# -- Options for sphinx.ext.todo ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html
todo_include_todos = True
