"""
PyGraphviz
==========

A Python wrapper for the graphviz Agraph data structure.

See https://pygraphviz.github.io for complete documentation.
See pygraphviz.AGraph for detailed documentation.
"""

import sys

# https://docs.python.org/3/whatsnew/3.8.html#bpo-36085-whatsnew
if sys.version_info >= (3, 8, 0) and sys.platform == "win32":
    import os

    # Wheel install: delvewheel places DLLs in pygraphviz.libs/
    _libs_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "pygraphviz.libs"
    )
    if os.path.isdir(_libs_dir):
        os.add_dll_directory(_libs_dir)
    # Dev install: find graphviz on PATH
    for path in os.environ.get("PATH", "").split(os.pathsep):
        if "graphviz" in path.lower() and os.path.exists(path):
            os.add_dll_directory(path)


__version__ = "2.0beta0.dev0"

from .agraph import AGraph, Attribute, DotError, Edge, ItemAttribute, Node

__all__ = ["AGraph", "Attribute", "DotError", "Edge", "ItemAttribute", "Node"]

from . import testing

# Per contract with Sphinx-Gallery, this method must be available at top level
from pygraphviz.scraper import _get_sg_image_scraper

del sys
