# -*- coding: utf-8 -*-
from nose.tools import *
import pygraphviz as pgv

def test_readwrite():
    A = pgv.AGraph(name='test graph')
    A.add_path([1,2,3,4,5,6,7,8,9,10])

#FIXME
# >>> (fd,fname)=tempfile.mkstemp()
    # A.write(fname)
    # A.read(fname)
    # assert_equal(B, AGraph(fname))
    # assert_true(B == A)
    # assert_false(B is A)
# >>> os.close(fd)
# >>> os.unlink(fname)
