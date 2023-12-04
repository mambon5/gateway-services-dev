
            
# Generate code documentation
This is how we generated the code documentation for the gateway backend python code.

Follow this guide

- [Generate code documentation](#generate-code-documentation)
  - [Install Sphinx](#install-sphinx)
  - [Set up files](#set-up-files)
  - [Set up the .rst modules](#set-up-the-rst-modules)
  - [Create the html files](#create-the-html-files)
  - [See the documentation](#see-the-documentation)
  - [All in once](#all-in-once)
  - [Conceptual maps](#conceptual-maps)



## Install Sphinx

Install sphinx and sphinx-apidoc from here https://www.sphinx-doc.org/en/master/usage/installation.html

## Set up files

Set up the *conf.py* and *index.rst* files that say how the configuration will be in all the documentation. More info on this here: 

1. **conf.py** > https://sphinx-doc-zh.readthedocs.io/en/latest/config.html
2. **index.rst** > https://eikonomega.medium.com/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365

If you want to avoid reading a lot, I use these configurations, adapt them to your file system:

1. **conf.py**:
   
        ```
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
        sys.path.append('/home/roma/smartec/gateway-services/single_transport/backend') # add this to the main sys.path to allow sphinx to find the modules


        # -- Project information -----------------------------------------------------

        project = 'Gateway communication'
        copyright = '2023, Romà Masana'
        author = 'Romà Masana'

        # The full version, including alpha/beta/rc tags
        release = '01-02-2023'


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
        napoleon_google_docstring = True
        napoleon_use_param = True
        napoleon_use_ivar = True

        autodoc_default_options = {
            'show-inheritance': False,
            'members': True,
            'member-order': 'bysource',
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
        ```

2. The **index.rst** file I use as a template:
        ```
        .. Gateway communication documentation master file, created by
        sphinx-quickstart on Wed Feb  1 10:44:52 2023.
        You can adapt this file completely to your liking, but it should at least
        contain the root `toctree` directive.

        Welcome to Gateway communication's documentation!
        =================================================

        .. autosummary::
        :toctree: modules
        :recursive:

        



        .. summarize every module and class in it: https://stackoverflow.com/questions/2701998/sphinx-autodoc-is-not-automatic-enough/62613202#62613202

        Indices and tables
        ==================

        * :ref:`genindex`
        * :ref:`modindex`
        * :ref:`search`
        ```

## Set up the .rst modules
Once the two files *conf.py* and an index.rst is set up, it is time to build the modules running the

```
sphinx-apidoc -o source/ ../<package>
```

command. In my case I run:

```
sphinx-apidoc -o source/modules/ ../backend/
```

Because I have all my python code at `../backend` and I want to save the `.rst` modules at `source/modules`

## Create the html files
Just place yourself in the docuemntation root folder (the folder where we did all the other operations) and perform the command

`make html`

## See the documentation
Just run the file 

`build/html/index.html`

In any browser.

## All in once

If you want to perform all the previous steps at once, just run the following linux shell script that I wrote:

`./create_html.sh`

And all the steps above will be run.

## Conceptual maps

Use *xmind*