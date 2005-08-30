#!/usr/bin/python
import sys
from pygraphviz import *

A=Agraph()

nodelist=['a','b','c','d','e']
edgelist=[['a','b'],['a','a'],['c','d']]

for node in nodelist:
    A.add_node(node)

for (source,target) in edgelist:
    A.add_edge(source,target,None)

for n in A.nodes():
    print n

for e in A.edges():
    print e.source(),e.target()

A.write(sys.stdout)
