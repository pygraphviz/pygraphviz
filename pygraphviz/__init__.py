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
#    Copyright (C) 2004-2010 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

# Release data
from . import release

if release.revision is None:
    # we probably not running in an svn directory   
    try:
        # use release data stored at installatation time.
        from . import version
        __version__ = version.__version__
        __revision__ = version.__revision__
        __date__ = version.__date__
    except ImportError:
        # version.py was not created or no longer exists
        __version__ = release.version
        __revision__ = release.revision
        __date__ = release.date
else:
    # use dynamic values, even if version.py exists
    __version__ = release.version
    __revision__ = release.revision
    __date__ = release.date

__author__   = '%s <%s>\n%s <%s>\n%s <%s>' % \
              ( release.authors['Hagberg'] + release.authors['Schult'] + \
                release.authors['Renieris'] )
__license__  = release.license

from .agraph import AGraph, Node, Edge, Attribute, ItemAttribute, DotError

__all__=[
    'AGraph',
    'Node',
    'Edge',
    'Attribute',
    'ItemAttribute',
    'DotError'
    ]


from pygraphviz.tests.test import run as test
