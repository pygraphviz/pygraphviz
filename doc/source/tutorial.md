---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Tutorial

The API is very similar to that of NetworkX. Much of the
[NetworkX tutorial](https://networkx.org/documentation/latest/tutorial.html)
is applicable to PyGraphviz.

## Start-up

Import PyGraphviz with

```{code-cell}
import pygraphviz as pgv
```

PyGraphviz wraps [graphviz](https://graphviz.org) providing a Python interface
to graphviz's functionality.
Information about the version of graphviz that is wrapped by pygraphviz can be
found with

```{code-cell}
pgv.__graphviz_version__
```

## Graphs

To make an empty pygraphviz graph use the AGraph class:

```{code-cell}
G = pgv.AGraph()
print(G)
```

You can use the strict and directed keywords to control what type of
graph you want. The default is to create a strict graph
(no parallel edges or self-loops). To create a digraph with possible
parallel edges and self-loops use

```{code-cell}
G = pgv.AGraph(strict=False, directed=True)
print(G)
```

You may specify a dot format file to be read on initialization:

```python
G = pgv.AGraph("Petersen.dot")
```

Other options for initializing a graph are using a string,

```{code-cell}
G = pgv.AGraph("graph {1 -- 2;}")
print(G)
```

using a dict of dicts,

```{code-cell}
d = {"1": {"2": None}, "2": {"1": None, "3": None}, "3": {"2": None}}
A = pgv.AGraph(d)
print(A)
```

or using a SWIG pointer to the AGraph datastructure,

```python
h = A.handle
C = pgv.AGraph(h)
```

## Nodes, and edges

Nodes and edges can be added one at a time

```{code-cell}
G = pgv.AGraph()
G.add_node("a")  # adds node 'a'
G.add_edge("b", "c")  # adds edge 'b'-'c' (and also nodes 'b', 'c')
print(G)
```

or from lists or containers.

```{code-cell}
nodelist = ["f", "g", "h"]
G.add_nodes_from(nodelist)
print(G)
```

If the node is not a string an attempt will be made to convert it
to a string

```{code-cell}
G.add_node(1)  # adds node '1'
G.nodes()
```

## Attributes

To set the default attributes for graphs, nodes, and edges use
the graph_attr, node_attr, and edge_attr dictionaries

```{code-cell}
G = pgv.AGraph()
G.graph_attr["label"] = "Name of graph"
G.node_attr["shape"] = "circle"
G.edge_attr["color"] = "red"
G.add_edge("A", "B")
print(G)
```

Graph attributes can be set when initializing the graph

```{code-cell}
G = pgv.AGraph(ranksep="0.1")
```

Attributes can be added when adding nodes or edges,

```{code-cell}
G.add_node(1, color="red")
G.add_edge("b", "c", color="blue")
print(G)
```

or through the node or edge attr dictionaries,

```{code-cell}
n = G.get_node(1)
n.attr["shape"] = "box"

e = G.get_edge("b", "c")
e.attr["color"] = "green"
print(G)
```

### Substitution Characters

The DOT language defines several special characters that substitute other values
during drawing.
These characters typically take the form of `\?` where `?` is a capital letter.
For example, the special character `\G`, if used in a node or edge label,
will be replaced with the graph name during drawing:

```{code-cell}
A = pgv.AGraph(name="foo")
A.add_node(1, label=r"my graph: \G")
A.add_edges_from([(1, 2), (2, 3)])
print(A)
```

Special characters have no effect during layout:

```{code-cell}
A.layout()
print(A)
```

Character substitution occurs during figure drawing:

```{code-cell}
A.draw("foo.png")
```

```{figure} foo.png

```

Character substitution can be disabled by escaping the special characters, e.g.
`\\G`.
See the [DOT language specification (pdf link)][dot_spec] for further details.

[dot_spec]: https://www.graphviz.org/pdf/dot.1.pdf

## Layout and Drawing

Pygraphviz provides several methods for layout and drawing of graphs.

To store and print the graph in dot format as a Python string use

```{code-cell}
s = G.string()
print(s)
```

To write to a file use

```{code-cell}
# Test round-tripping graph data to/from file
G.write("file.dot")

with open("file.dot") as fh:
    H = pgv.AGraph(fh.read())

H.string() == s
```

To add positions to the nodes with a Graphviz layout algorithm

```{code-cell}
G.layout()  # default to neato
print(G)
```

```{code-cell}
G.layout(prog="dot")  # use dot
print(G)
```

To render the graph to an image

```{code-cell}
G.draw("file.png")  # write previously positioned graph to PNG file
```

```{figure} file.png

```

```python
# Use `circo` layout to position, write to PostScript file for e.g. embedding
# in a LaTeX document
G.draw("file.ps", prog="circo")
```

```{code-cell}
# Or render directly to an image format
G.draw("file.svg", prog="circo")
```

```{figure} file.svg

```
