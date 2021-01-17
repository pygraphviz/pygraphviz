"""
PyGraphviz
==========

A Python wrapper for the graphviz Agraph data structure.

See https://pygraphviz.github.io for complete documentation.
See pygraphviz.AGraph for detailed documentation.
"""

import sys

if sys.version_info >= (3, 8, 0) and sys.platform == "win32":
    import os

    for path in os.environ["PATH"].split(";"):
        if path and os.path.exists(path):
            os.add_dll_directory(path)

__version__ = "1.7rc2.dev0"

from pygraphviz.agraph import AGraph, Node, Edge, Attribute, ItemAttribute, DotError

__all__ = ["AGraph", "Node", "Edge", "Attribute", "ItemAttribute", "DotError"]

from pygraphviz import testing

# Per contract with Sphinx-Gallery, this method must be available at top level
from pygraphviz.scraper import _get_sg_image_scraper
