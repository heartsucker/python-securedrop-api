# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..')) ## noqa

import securedrop_api

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

project = 'securedrop_api'
copyright = '2018, heartsucker'
author = 'heartsucker'
version = securedrop_api.__version__
release = version

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'
master_doc = 'index'
language = None
todo_include_todos = True
exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'

if on_rtd:
    html_theme = 'default'
else:
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except ImportError:
        html_theme = 'alabaster'

htmlhelp_basename = 'securedrop_apidoc'

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
