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
#    All rights reserved, see COPYING for details.
#
#    pygraphviz is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    pygraphviz is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pygraphviz; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import os, sys
sys.path.append(os.path.join(os.path.split(__file__)[0], sys.platform))
del os
del sys

#
# pygraphviz package modules
#
from pygraphviz import *

