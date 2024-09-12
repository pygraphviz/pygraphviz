import pygraphviz as pgv

stringify = pgv.testing.stringify


def test_default_attributes():
    A = pgv.AGraph()
    A.graph_attr["label"] = "test"
    A.graph_attr["spam"] = "eggs"
    assert "label" in A.graph_attr
    assert A.graph_attr["label"] == "test"
    assert A.graph_attr.keys() == ["label", "spam"]
    graph_attrs = [("label", "test"), ("spam", "eggs")]
    assert sorted(A.graph_attr.iteritems()) == graph_attrs
    ans = """strict graph { graph [label=test, spam=eggs]; }"""
    assert stringify(A) == " ".join(ans.split())

    A.graph_attr["label"] = ""
    A.graph_attr["spam"] = ""
    ans = """strict graph { }"""
    assert stringify(A) == " ".join(ans.split())

    A.graph_attr["label"] = "test"
    del A.graph_attr["label"]
    ans = """strict graph { }"""
    assert stringify(A) == " ".join(ans.split())


def test_graph_defaults():
    A = pgv.AGraph(rankdir="LR", pack="true")
    ans = """strict graph { graph [pack=true, rankdir=LR]; }"""
    assert stringify(A) == " ".join(ans.split())


def test_node_defaults():
    A = pgv.AGraph()
    A.node_attr["label"] = "test"
    assert "label" in A.node_attr
    assert A.node_attr["label"] == "test"
    assert A.node_attr.keys() == ["label"]
    assert A.node_attr == {"label": "test"}
    assert list(A.node_attr.iteritems()) == [("label", "test")]
    ans = """strict graph { node [label=test]; }"""
    assert stringify(A) == " ".join(ans.split())

    A.node_attr["label"] = ""
    ans = """strict graph { }"""
    assert stringify(A) == " ".join(ans.split())

    A.node_attr["label"] = "test"
    del A.node_attr["label"]
    ans = """strict graph { }"""
    assert stringify(A) == " ".join(ans.split())

    A.graph_attr["fontname"] = "graph font"
    A.node_attr["fontname"] = "node font"
    A.edge_attr["fontname"] = "edge font"
    ans = """strict graph {
          graph [fontname="graph font"];
          node [fontname="node font"];
          edge [fontname="edge font"];
        }"""
    assert stringify(A) == " ".join(ans.split())


def test_edge_defaults():
    A = pgv.AGraph()
    A.edge_attr["label"] = "test"
    assert "label" in A.edge_attr
    assert A.edge_attr["label"] == "test"
    assert A.edge_attr.keys() == ["label"]
    assert A.edge_attr == {"label": "test"}
    assert list(A.edge_attr.iteritems()) == [("label", "test")]

    ans = """strict graph { edge [label=test]; } """
    assert stringify(A) == " ".join(ans.split())

    A.edge_attr["label"] = ""
    ans = """strict graph { }"""
    assert stringify(A) == " ".join(ans.split())

    A.edge_attr["label"] = "test"
    del A.edge_attr["label"]
    ans = """strict graph { }"""
    assert stringify(A) == " ".join(ans.split())
