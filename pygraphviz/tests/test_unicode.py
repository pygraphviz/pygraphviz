# -*- coding: utf-8 -*-
from nose.tools import *
import pygraphviz as pgv

def test_name_unicode():
    A = pgv.AGraph(name=u'unicode')
    assert_equal(A.name,u'unicode')

def test_node_encoding():
    A = pgv.AGraph(encoding='UTF-8')
    hello='Здравствуйте!'.decode('UTF-8')
    A.add_node(hello)
    n=A.get_node(hello)
    assert_equal(n.name, hello)

    n.attr['goodbye']="До свидания".decode('UTF-8')
    assert_equal(n.attr['goodbye'],"До свидания".decode('UTF-8'))

def test_edge_encoding():
    A = pgv.AGraph(encoding='UTF-8')
    hello="שלום".decode('UTF-8')
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
    ug = unicode(G)
    sg = str(G)
    G1 = pgv.AGraph(ug)
    G2 = pgv.AGraph(sg)
    assert_equal(unicode(G1),unicode(G2))
