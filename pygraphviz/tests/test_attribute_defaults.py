from nose.tools import *
import pygraphviz as pgv


def stringify(agraph):
    result = agraph.string().split()
    if '""' in result:
        result.remove('""')
    return " ".join(result)


def test_default_attributes():
    A = pgv.AGraph()
    A.graph_attr["label"] = "test"
    A.graph_attr["spam"] = "eggs"
    assert_true("label" in A.graph_attr)
    assert_equal(A.graph_attr["label"], "test")
    assert_equal(A.graph_attr.keys(), ["label", "spam"])
    assert_equal(
        sorted(list(A.graph_attr.iteritems())), [("label", "test"), ("spam", "eggs")]
    )
    ans = """strict graph { graph [label=test, spam=eggs ]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    A.graph_attr["label"] = ""
    A.graph_attr["spam"] = ""
    ans = """strict graph { }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    A.graph_attr["label"] = "test"
    del A.graph_attr["label"]
    ans = """strict graph { }"""
    assert_equal(stringify(A), " ".join(ans.split()))


def test_graph_defaults():
    A = pgv.AGraph(rankdir="LR", pack="true")
    ans = """strict graph { graph [pack=true, rankdir=LR ]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))


def test_node_defaults():
    A = pgv.AGraph()
    A.node_attr["label"] = "test"
    assert_true("label" in A.node_attr)
    assert_equal(A.node_attr["label"], "test")
    assert_equal(A.node_attr.keys(), ["label"])
    assert_equal(A.node_attr, {"label": "test"})
    assert_equal(list(A.node_attr.iteritems()), [("label", "test")])
    ans = """strict graph { node [label=test]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    A.node_attr["label"] = ""
    ans = """strict graph { }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    A.node_attr["label"] = "test"
    del A.node_attr["label"]
    ans = """strict graph { }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    A.graph_attr["fontname"] = "graph font"
    A.node_attr["fontname"] = "node font"
    A.edge_attr["fontname"] = "edge font"
    ans = """strict graph {
          graph [fontname="graph font"];
          node [fontname="node font"];
          edge [fontname="edge font"];
        }"""
    assert_equal(stringify(A), " ".join(ans.split()))


def test_edge_defaults():
    A = pgv.AGraph()
    A.edge_attr["label"] = "test"
    assert_true("label" in A.edge_attr)
    assert_equal(A.edge_attr["label"], "test")
    assert_equal(A.edge_attr.keys(), ["label"])
    assert_equal(A.edge_attr, {"label": "test"})
    assert_equal(list(A.edge_attr.iteritems()), [("label", "test")])

    ans = """strict graph { edge [label=test]; } """
    assert_equal(stringify(A), " ".join(ans.split()))

    A.edge_attr["label"] = ""
    ans = """strict graph { }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    A.edge_attr["label"] = "test"
    del A.edge_attr["label"]
    ans = """strict graph { }"""
    assert_equal(stringify(A), " ".join(ans.split()))
