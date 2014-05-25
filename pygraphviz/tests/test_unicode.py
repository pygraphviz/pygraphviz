# -*- coding: utf-8 -*-
from nose.tools import *
import pygraphviz as pgv
from pygraphviz.agraph import _TEXT_TYPE

def test_name_unicode():
    A = pgv.AGraph(name=u'unicode')
    assert_equal(A.name,u'unicode')

def test_node_encoding():
    A = pgv.AGraph(encoding='UTF-8')
    hello=u'Здравствуйте!'
    A.add_node(hello)
    n=A.get_node(hello)
    assert_equal(n.name, hello)

    n.attr['goodbye']=u"До свидания"
    assert_equal(n.attr['goodbye'],u"До свидания")

def test_edge_encoding():
    A = pgv.AGraph(encoding='UTF-8')
    hello=u"שלום"
    A.add_edge(hello,hello,key=1) # self loop
    e=A.get_edge(hello,hello)
    assert_equal(e.name,u'1')
    assert_equal(e,(hello,hello))

    e.attr['hello']=hello
    assert_equal(e.attr['hello'], hello)

def test_from_string():
    # test unicode in from_string()
    t = u'测试'
    G =pgv.AGraph()
    G.add_node(t)
    ug = _TEXT_TYPE(G)
    sg = str(G)
    G1 = pgv.AGraph(ug)
    G2 = pgv.AGraph(sg)
    assert_equal(_TEXT_TYPE(G1),_TEXT_TYPE(G2))
