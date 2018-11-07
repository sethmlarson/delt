# -*- coding: utf-8 -*-

import os
import sys
import datetime
sys.path.insert(0, os.path.abspath("../../src"))
import delt

project = 'Delt'
copyright = '%d, Seth Michael Larson' % datetime.datetime.now().year
author = 'Seth Michael Larson'

version = delt.__version__
release = delt.__version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

language = None

exclude_patterns = []
pygments_style = "sphinx"


html_theme = 'sphinx_typlog_theme'
html_static_path = ['_static']
html_theme_options = {
    "logo_name": "Delt",
    "color": "#E8371A",
    "description": "Continuous Integration Environment Delta Tracking",
    "github_user": "delt-io",
    "github_repo": "delt",
}
html_sidebars = {
    "**": [
        "github.html"
    ]
}

intersphinx_mapping = {'https://docs.python.org/': None}
