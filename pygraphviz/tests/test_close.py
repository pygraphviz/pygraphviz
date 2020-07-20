# -*- coding: utf-8 -*-
from nose.tools import *
import pygraphviz as pgv


def test_context_manager():
    with pgv.AGraph() as ag:
        ag0 = ag
    assert_not_equal(ag0.handle, None)


def test_double_close():
    ag = pgv.AGraph()
    ag.close()
    assert_equal(ag.handle, None)
    ag.close()
