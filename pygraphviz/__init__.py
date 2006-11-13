"""
A Python wrapper for the graphviz Agraph data structure.

Quick example::

 >>> from pygraphviz import *
 >>> G=AGraph()
 >>> G.add_node('a')
 >>> G.add_edge('b','c')
 >>> G
 strict graph {
         a;
         b -- c;
 }


See pygraphviz.AGraph for detailed documentation.

"""
#    Copyright (C) 2004-2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

from agraph import AGraph, Node, Edge, Attribute, ItemAttribute

__all__=[
    'AGraph',
    'Node',
    'Edge',
    'Attribute',
    'ItemAttribute'
    ]

# import tests: run as pygraphviz.test()
from tests import run as test
