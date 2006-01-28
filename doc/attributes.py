#!/usr/bin/python
import sys
from pygraphviz import *

A=Agraph()

nodelist=['a','b','c','d','e']
edgelist=[['a','b'],['a','a'],['c','d']]

for node in nodelist:
    A.add_node(node)

for (source,target) in edgelist:
    label=source+"-"+target # label with e.g. a-b
    A.add_edge(source,target,label)

# default attributes for graph
A.set_attr(label='pygraphviz',fontsize=26)
# default attributes for nodes
A.set_node_attr(color='blue',style='filled',shape='polygon',sides=4)
# default attributes for edges
A.set_edge_attr(color='black')

# node a should be red
nodea=A.get_node('a')
nodea.set_attr(color='red',sides=8)

# edge c-d should be green
edgecd=A.get_edge('c','d')
edgecd.set_attr(color='green')


A.write(sys.stdout)
