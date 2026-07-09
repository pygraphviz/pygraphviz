"""
Subgraph with Boundaries
========================

Draw a subgraph with bounding boxes demarcating both the nodes and the subgraphs
"""

import pygraphviz as pgv

# A graph in `.dot` format specifying two nodes, each within their own subgraph,
# and a bi-directional edge between them
dot_str = """
digraph G {
    graph [compound=true];

    node [shape=box];

    subgraph cluster_A {
        label="A";
        a1 [pos="50,100!"];
    }

    subgraph cluster_B {
        label="B";
        b1 [pos="200,100!"];
    }

    a1 -> b1 [lhead=cluster_B, ltail=cluster_A, dir=both];

    graph [bb="0,0,300,200"];
}
"""

A = pgv.AGraph(dot_str)
A.layout("dot")
A.draw("subgraph_bdries.png")
