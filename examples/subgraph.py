#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import pygraphviz as pgv

A=pgv.AGraph()
# add some edges
A.add_edge(1,2)
A.add_edge(2,3)
A.add_edge(1,3)
A.add_edge(3,4)
A.add_edge(3,5)
A.add_edge(3,6)
A.add_edge(4,6)
# make a subgraph with rank='same'
B=A.add_subgraph([4,5,6],name='s1',rank='same')
B.graph_attr['rank']='same'
print(A.string()) # print dot file to standard output
