# -*- coding: utf-8 -*-
from nose.tools import *
import pygraphviz as pgv


def test_del():
    A = pgv.AGraph()
    A.add_node(1,foo='bar')
    # For some reasons after porting to Python 3 clear often cause infinite loop
    A.delete_node('1')
    assert_equal(len(A), 0)

def test_clear_node_with_attributes():
    A = pgv.AGraph()
    A.add_node(1,foo='bar')
    # For some reasons after porting to Python 3 clear often cause infinite loop
    A.clear()
    assert_equal(len(A), 0)
    assert_equal(A.nodes(), [])
    assert_equal(A.node_attr.keys(), [])

def test_clear_graph_attributes():
    A = pgv.AGraph()
    A.add_node(1,foo='bar')
    A.graph_attr.update(landscape='true',ranksep='0.1')
    # For some reasons after porting to Python 3 clear often cause infinite loop
    A.clear()
    assert_equal(len(A), 0)
    assert_equal(A.nodes(), [])
    assert_equal(A.node_attr.keys(), [])
    assert_equal(A.graph_attr.keys(), [])