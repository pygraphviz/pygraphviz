#!/usr/bin/python
import os, tempfile
from pygraphviz import *

A=Agraph()

nodelist=['a','b','c','d','e']
edgelist=[['a','b'],['a','a'],['c','d']]

for node in nodelist:
    A.add_node(node)

for (source,target) in edgelist:
    A.add_edge(source,target,None)

fh=open('test.dot','w')
A.write(fh)
os.system("neato -Tpng test.dot >test.png")



