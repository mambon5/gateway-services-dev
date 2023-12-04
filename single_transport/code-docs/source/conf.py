# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
sys.path.append('/home/roma/smartec/gateway-services-development/single_transport/backend') # add this to 
                                        #  the main sys.path to allow sphinx to find the modules


# -- Project information -----------------------------------------------------

project = "Gateway communication's code"
copyright = '2023, Romà Masana'
author = 'Romà Masana'

# The full version, including alpha/beta/rc tags
release = '01-05-2023'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.duration',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz'
    # 'breathe',
    # 'exhale'
    # 'sphinx_js'
]

graphviz_output_format = 'svg'
autosummary_generate = True  # Turn on sphinx.ext.autosummary
autosummary_imported_members = False
napoleon_google_docstring = True
napoleon_use_param = True
napoleon_use_ivar = True


autodoc_default_options = {
    'show-inheritance': False,
    'members': True,
    'member-order': 'alphabetical',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
autoclass_content = 'both'

add_module_names = False # delete the prepended module name in front of every variable and function

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# ADC theme:
# import sphinx_adc_theme
# html_theme = 'sphinx_adc_theme'
# html_theme_path = [sphinx_adc_theme.get_html_theme_path()]

# html_theme = 'groundwork'

html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_css_files = [
    'style.css',
]
html_static_path = ['_static']