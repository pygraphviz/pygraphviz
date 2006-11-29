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

# Release data
import release 
__version__  = release.version
__date__     = release.date
__author__   = '%s <%s>\n%s <%s>\n%s <%s>' % \
              ( release.authors['Hagberg'] + release.authors['Schult'] + \
                release.authors['Renieris'] )
__license__  = release.license

from agraph import AGraph, Node, Edge, Attribute, ItemAttribute

__all__=[
    'AGraph',
    'Node',
    'Edge',
    'Attribute',
    'ItemAttribute'
    ]

def version():
    from agraph import _get_prog
    import os
    print "pygraphviz-"+__version__
    neato=_get_prog('neato')
    os.system(neato+' -V')

# import tests: run as pygraphviz.test()
from tests import run as test
