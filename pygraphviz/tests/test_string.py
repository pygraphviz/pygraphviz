import pygraphviz as pgv
import pytest

stringify = pgv.testing.stringify


def test_name():
    A = pgv.AGraph(name="")
    assert stringify(A) == "strict graph { }"
    assert A.__repr__()[0:7] == "<AGraph"


def test_string_representation_small():
    A = pgv.AGraph(name="test")
    A.add_path([1, 2])
    assert stringify(A) == "strict graph test { 1 -- 2; }"


def test_string_representation_large():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    A.add_node(11)
    ans1 = """strict graph "test graph" {
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
    ans2 = """strict graph "test graph" {
             11;
             1 -- 2;
             2 -- 3;
             3 -- 4;
             4 -- 5;
             5 -- 6;
             6 -- 7;
             7 -- 8;
             8 -- 9;
             9 -- 10;
             }"""
    result = stringify(A)
    assert result in {" ".join(a.split()) for a in (ans1, ans2)}


def test_bad_dot_input():
    with pytest.raises(pgv.DotError):
        A = pgv.AGraph(string="graph {1--1")
