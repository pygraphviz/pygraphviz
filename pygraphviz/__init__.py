"""
A Python wrapper for the graphviz Agraph data structure.

Quick example:

from pygraphviz import *
import sys
A=Agraph()
A.add_node("a")
A.add_edge("a","b",None)
A.write(sys.stdout)

See pygraphviz.pygraphviz for detailed documentation.

"""
#    Copyright (C) 2004,2005 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

import os, sys
sys.path.append(os.path.join(os.path.split(__file__)[0], sys.platform))
del os
del sys

#
# pygraphviz package modules
#
from pygraphviz import *

