from nose.tools import assert_equal, raises
import pygraphviz as pgv


def stringify(agraph):
    result = agraph.string().split()
    if '""' in result:
        result.remove('""')
    return " ".join(result)


def test_name():
    A = pgv.AGraph(name="")
    assert_equal(stringify(A), "strict graph { }")
    assert_equal(A.__repr__()[0:7], "<AGraph")


def test_string_representation_small():
    A = pgv.AGraph(name="test")
    A.add_path([1, 2])
    assert_equal(stringify(A), "strict graph test { 1 -- 2; }")


def test_string_representation_large():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    A.add_node(11)
    ans = """strict graph "test graph" {
             1 -- 2;
             2 -- 3;
             3 -- 4;
             4 -- 5;
             5 -- 6;
             6 -- 7;
             7 -- 8;
             8 -- 9;
             9 -- 10;
             11; }"""
    assert_equal(stringify(A), " ".join(ans.split()))


@raises(pgv.DotError)
def test_bad_dot_input():
    A = pgv.AGraph(string="graph {1--1")
