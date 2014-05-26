# -*- coding: utf-8 -*-
from nose.tools import *
import pygraphviz as pgv
from os import linesep

def test_html():
    G = pgv.AGraph(label='<Hello<BR/>Graph>')
    G.add_node('a', label='<Hello<BR/>Node>')
    s = G.add_subgraph('b', label='<Hello<BR/>Subgraph>')
    s.add_node('sa', label='<Hello<BR/>Subgraph Node b>')
    G.add_edge('a','b', label='<Hello<BR/>Edge>')
    assert_equal(G.string().expandtabs(2),
"""strict graph {
  graph [label=<Hello<BR/>Graph>];
  node [label="\\N"];
  {
    graph [label=<Hello<BR/>Subgraph>];
    sa     [label=<Hello<BR/>Subgraph Node b>];
  }
  a  [label=<Hello<BR/>Node>];
  a -- b   [label=<Hello<BR/>Edge>];
}
""".replace('\n', linesep))
