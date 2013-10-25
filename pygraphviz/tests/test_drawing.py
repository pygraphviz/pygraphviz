# -*- coding: utf-8 -*-
from nose.tools import *
import pygraphviz as pgv

@raises(AttributeError)
def test_drawing_error():
    A = pgv.AGraph(name='test graph')
    A.add_path([1,2,3,4])
    d = A.draw()

# this is not a very good way to test...
#def test_drawing():
#    A = pgv.AGraph(name='test graph')
#    A.add_path([1,2,3,4])
#    d = A.draw(prog='neato')
#    assert_equal(len(d.splitlines()),19)
# FIXME
# smoke test
# >>> (fd,fname)=tempfile.mkstemp()
# >>> A.draw(fname,format='ps',prog='neato')
# >>> A.draw(fname,prog='neato')

@raises(ValueError)
def test_name_error():
    A = pgv.AGraph(name='test graph')
    A.draw('foo',prog='foo')
