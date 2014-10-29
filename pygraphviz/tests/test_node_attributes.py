# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from nose.tools import *
import pygraphviz as pgv
from os import linesep

def test_node_attribute():
    A = pgv.AGraph()
    A.add_node(1,label='test',spam='eggs')
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  node [label="\\N"];
  1  [label=test,
    spam=eggs];
}
""".replace('\n', linesep))

def test_node_attributes2():
    A = pgv.AGraph()
    A.add_node(1)
    one = A.get_node(1)
    one.attr['label'] = 'test'
    one.attr['spam'] = 'eggs'
    assert_true('label' in one.attr)
    assert_equal(one.attr['label'],'test')
    assert_equal(sorted(one.attr.keys()), ['label', 'spam'])
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  node [label="\\N"];
  1  [label=test,
    spam=eggs];
}
""".replace('\n', linesep)
)
    one.attr['label'] = ''
    one.attr['spam'] = ''
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  node [label="\\N"];
  1  [label=""];
}
""".replace('\n', linesep))
    one.attr['label'] = 'test'
    del one.attr['label']
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  node [label="\\N"];
  1  [label=""];
}
""".replace('\n', linesep))

def test_node_attribute_update():
    A = pgv.AGraph()
    A.add_node(1,label='test',spam='eggs')
    A.add_node(1,label='updated')
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  node [label="\\N"];
  1  [label=updated,
    spam=eggs];
}
""".replace('\n', linesep))

def test_node_attribute_remove():
    A = pgv.AGraph()
    A.add_node(1,label='test',spam='eggs')
    A.add_node(1,label=r'\N',spam='') # use \N to signify null label, otherwise ''
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  node [label="\\N"];
  1;
}
""".replace('\n', linesep))
