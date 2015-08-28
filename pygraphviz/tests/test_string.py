# -*- coding: utf-8 -*-
from nose.tools import assert_equal, raises
import pygraphviz as pgv
from os import linesep


def test_name():
    A = pgv.AGraph(name='')
    assert_equal(A.string(),
"""strict graph {
}
""".replace('\n', linesep))


    assert_equal(A.string().expandtabs(),
"""strict graph {
}
""".replace('\n', linesep))

    assert_equal( A.__repr__()[0:7],'<AGraph')


def test_string_representation_small():
    A = pgv. AGraph(name='test')
    A.add_path([1,2])
    assert_equal(A.string().expandtabs(),
"""strict graph test {
        1 -- 2;
}
""".replace('\n', linesep)
)

def test_string_representation_large():
    A = pgv.AGraph(name='test graph')
    A.add_path([1,2,3,4,5,6,7,8,9,10])
    A.add_node(11)
    assert_equal(A.string().expandtabs(),
"""strict graph "test graph" {
        1 -- 2;
        2 -- 3;
        3 -- 4;
        4 -- 5;
        5 -- 6;
        6 -- 7;
        7 -- 8;
        8 -- 9;
        9 -- 10;
        11;
}
""".replace('\n', linesep))

@raises(pgv.DotError)
def test_bad_dot_input():
    A = pgv.AGraph(string='graph {1--1')
