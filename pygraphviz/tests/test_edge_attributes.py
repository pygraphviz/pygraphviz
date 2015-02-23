# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from nose.tools import *
import pygraphviz as pgv
from os import linesep

def test_edge_attributes():
    A = pgv.AGraph()
    A.add_edge(1,2,label='test',spam='eggs')
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  1 -- 2   [label=test,
    spam=eggs];
}
""".replace('\n', linesep)
)

def test_edge_attributes2():
    A = pgv.AGraph()
    A.add_edge(1,2)
    one = A.get_edge(1,2)
    one.attr['label'] = 'test'
    one.attr['spam'] = 'eggs'
    assert_true('label' in one.attr)
    assert_equal(one.attr['label'], 'test')
    assert_equal(sorted(one.attr.keys()), ['label', 'spam'])
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  1 -- 2   [label=test,
    spam=eggs];
}
""".replace('\n', linesep)
)
    one.attr['label'] = ''
    one.attr['spam'] = ''
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  1 -- 2;
}
""".replace('\n', linesep)
)
    one.attr['label'] = 'test'
    del one.attr['label']
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  1 -- 2;
}
""".replace('\n', linesep)
)

def _test_anonymous_edges():
    """graph test {\n a -- b [label="edge1"];\n a -- b [label="edge2"];\n }"""

    import os,tempfile
    fd, fname = tempfile.mkstemp()
    #os.write(d)
    #os.close(fd)
    #A = AGraph(fname)

    assert_equal(A.string().expandtabs(2),
"""graph test {
   a -- b   [label=edge1];
   a -- b   [label=edge2];
}
""".replace('\n', linesep))
    os.unlink(fname)

def test_edge_attribute_update():
    A = pgv.AGraph(strict=True)
    A.add_edge(1,2,label='test',spam='eggs')
    A.add_edge(1,2,label='update',spam='')
    assert_equal(A.string().expandtabs(2),
"""strict graph {
  1 -- 2   [label=update];
}
""".replace('\n', linesep)
)

def test_edge_attribute_update_nonstrict():
    A = pgv.AGraph(strict=False)
    A.add_edge(1,2,label='test',spam='eggs',key='one')
    A.add_edge(1,2,label='update',spam='',key='one')
    assert_equal(A.string().expandtabs(2),
"""graph {
  1 -- 2 [key=one,
  label=update];
}
""".replace('\n', linesep)
)
