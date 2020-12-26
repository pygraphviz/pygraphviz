from datetime import date
import sphinx_rtd_theme
from warnings import filterwarnings

filterwarnings(
    "ignore", message="Matplotlib is currently using agg", category=UserWarning
)

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.addons.*') or your custom ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.imgmath",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_gallery.gen_gallery",
    "numpydoc",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
source_encoding = "utf-8"

# The master toctree document.
master_doc = "index"

# General substitutions.
project = "PyGraphviz"
copyright = f"2004-{date.today().year}, PyGraphviz Developers"

# Sphinx gallery configuration
sphinx_gallery_conf = {
    "examples_dirs": "../../examples",
    "gallery_dirs": "auto_examples",
    "ignore_pattern": "skip_",
    "image_scrapers": ("pygraphviz",),
}


# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.
import pygraphviz

version = pygraphviz.__version__
# The full version, including alpha/beta/rc tags.
release = version


# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
unused_docs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# Options for HTML output
# -----------------------

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_theme_options = {
    "canonical_url": "https://pygraphviz.github.io/documentation/stable",
    "navigation_depth": 3,
}

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
# html_style = 'sphinxdoc.css'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Content template for the index page.
html_index = "contents.html"

# Custom sidebar templates, maps page names to templates.
# html_sidebars = {'index': 'indexsidebar.html'}

# Additional templates that should be rendered to pages, maps page names to
# templates.
# html_additional_pages = {'index': 'index.html'}

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = False

html_use_opensearch = "http://pygraphviz.github.io"

# Output file base name for HTML help builder.
htmlhelp_basename = "PyGraphviz"

pngmath_use_preview = True

# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
latex_paper_size = "letter"

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = [
    (
        "index",
        "pygraphviz.tex",
        "PyGraphviz Documentation",
        "PyGraphviz Developers",
        "manual",
        1,
    )
]


# latex_use_parts = True

# Additional stuff for the LaTeX preamble.
latex_elements = {"fontpkg": "\\usepackage{palatino}"}

# Documents to append as an appendix to all manuals.
# latex_appendices = []
