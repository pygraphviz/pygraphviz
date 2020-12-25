"""
A Python wrapper for the graphviz Agraph data structure.

Quick example::

>>> from pygraphviz import *
>>> G=AGraph()
>>> G.add_node('a')
>>> G.add_edge('b','c')
>>> print G  # doctest: +SKIP 
strict graph {
    a;
    b -- c;
}
<BLANKLINE>

See pygraphviz.AGraph for detailed documentation.

"""

# Release data
from . import release

__date__ = release.date
__version__ = release.version

__author__ = (
    f"{release.authors['Hagberg'][0]} <{release.authors['Hagberg'][1]}>\n"
    f"{release.authors['Schult'][0]} <{release.authors['Schult'][1]}>\n"
    f"{release.authors['Renieris'][0]} <{release.authors['Renieris'][1]}>"
)

__license__ = release.license

from .agraph import AGraph, Node, Edge, Attribute, ItemAttribute, DotError

__all__ = ["AGraph", "Node", "Edge", "Attribute", "ItemAttribute", "DotError"]

from . import testing

# Per contract with Sphinx-Gallery, this method must be available at top level
from pygraphviz.scraper import _get_sg_image_scraper
