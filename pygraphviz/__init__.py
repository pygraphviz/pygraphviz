"""
PyGraphviz
==========

A Python wrapper for the graphviz Agraph data structure.

See https://pygraphviz.github.io for complete documentation.
See pygraphviz.AGraph for detailed documentation.
"""

__version__ = "1.7rc1.dev0"

from .agraph import AGraph, Node, Edge, Attribute, ItemAttribute, DotError

__all__ = ["AGraph", "Node", "Edge", "Attribute", "ItemAttribute", "DotError"]

from . import testing

# Per contract with Sphinx-Gallery, this method must be available at top level
from pygraphviz.scraper import _get_sg_image_scraper
