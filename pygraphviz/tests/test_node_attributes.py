from nose.tools import *
import pygraphviz as pgv


def stringify(agraph):
    result = agraph.string().split()
    if '""' in result:
        result.remove('""')
    return " ".join(result)


def test_node_attribute():
    A = pgv.AGraph()
    A.add_node(1, label="test", spam="eggs")
    ans = """strict graph { node [label="\\N"]; 1 [label=test, spam=eggs]; }"""
    assert_equal(stringify(A), ans)


def test_node_attributes2():
    A = pgv.AGraph()
    A.add_node(1)
    one = A.get_node(1)
    one.attr["label"] = "test"
    one.attr["spam"] = "eggs"
    assert_true("label" in one.attr)
    assert_equal(one.attr["label"], "test")
    assert_equal(sorted(one.attr.keys()), ["label", "spam"])
    ans = """strict graph { node [label="\\N"]; 1 [label=test, spam=eggs]; }"""
    assert_equal(stringify(A), ans)

    one.attr["label"] = ""
    one.attr["spam"] = ""
    ans = """strict graph { node [label="\\N"]; 1 [label=""]; }"""
    assert_equal(stringify(A), ans)

    one.attr["label"] = "test"
    del one.attr["label"]
    ans = """strict graph { node [label="\\N"]; 1 [label=""]; }"""
    assert_equal(stringify(A), ans)


def test_node_attribute_update():
    A = pgv.AGraph()
    A.add_node(1, label="test", spam="eggs")
    A.add_node(1, label="updated")
    ans = """strict graph { node [label="\\N"]; 1 [label=updated, spam=eggs]; }"""
    assert_equal(stringify(A), ans)


def test_node_attribute_remove():
    A = pgv.AGraph()
    A.add_node(1, label="test", spam="eggs")
    A.add_node(1, label=r"\N", spam="")  # use \N to signify null label, else ''
    ans = """strict graph { node [label="\\N"]; 1; }"""
    assert_equal(stringify(A), ans)
