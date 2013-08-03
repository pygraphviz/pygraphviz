Tutorial
========

The API is very similar to that of NetworkX.  Much of the 
NetworkX tutorial at http://networkx.github.io/documentation/latest/tutorial/
is applicable to PyGraphviz.  
See http://pygraphviz.github.io/documentation/latest/reference/api_notes.html  for major differences.

Start-up
--------

Import PyGraphviz with

>>> import pygraphviz as pgv

or to bring into the current namespace without the "pgv" prefix

>>> from pygraphviz import *


Graphs
------

To make an empty pygraphviz graph use the AGraph class:

>>> G=pgv.AGraph()

You can use the strict and directed keywords to control what type of
graph you want.  The default is to create a strict graph 
(no parallel edges or self-loops).  To create a digraph with possible
parallel edges and self-loops use

>>> G=pgv.AGraph(strict=False,directed=True)

You may specify a dot format file to be read on initialization:

>>> G=pgv.AGraph("Petersen.dot")  # doctest: +SKIP 

Other options for intializing a graph are using a string,

>>> G=pgv.AGraph('graph {1 - 2}')

using a dict of dicts,

>>> d={'1': {'2': None}, '2': {'1': None, '3': None}, '3': {'2': None}}
>>> A=pgv.AGraph(d)

or using a SWIG pointer to the AGraph datastructure,

>>> h=A.handle
>>> C=pgv.AGraph(h)


Nodes, and edges
----------------

Nodes and edges can be added one at a time 

>>> G.add_node('a') # adds node 'a'
>>> G.add_edge('b','c') # adds edge 'b'-'c' (and also nodes 'b', 'c')

or from lists or containers.

>>> nodelist=['f','g','h']
>>> G.add_nodes_from(nodelist)

If the node is not a string an attempt will be made to convert it
to a string

>>> G.add_node(1)  # adds node '1'


Attributes
----------

To set the default attributes for graphs, nodes, and edges use
the graph_attr, node_attr, and edge_attr dictionaries

>>> G.graph_attr['label']='Name of graph'
>>> G.node_attr['shape']='circle'
>>> G.edge_attr['color']='red'

Graph attributes can be set when initializing the graph

>>> G=pgv.AGraph(ranksep='0.1')

Attributes can be added when adding nodes or edges,

>>> G.add_node(1, color='red')
>>> G.add_edge('b','c',color='blue')

or through the node or edge attr dictionaries, 

>>> n=G.get_node(1)
>>> n.attr['shape']='box'


>>> e=G.get_edge('b','c')
>>> e.attr['color']='green'

Layout and Drawing
------------------
Pygraphviz provides several methods for layout and drawing of graphs.

To store and print the graph in dot format as a Python string use

>>> s=G.string()

To write to a file use

>>> G.write("file.dot")

To add positions to the nodes with a Graphviz layout algorithm

>>> G.layout() # default to neato
>>> G.layout(prog='dot') # use dot

To render the graph to an image 

>>> G.draw('file.png')  # write previously positioned graph to PNG file
>>> G.draw('file.ps',prog='circo') # use circo to position, write PS file





