import pytest

import pygraphviz as pgv


@pytest.mark.parametrize("directed", [False, True])
@pytest.mark.parametrize("strict", [False, True])
def test_copy_keeps_nested_clusters_and_independent_lifetime(directed, strict):
    declaration = ("strict " if strict else "") + ("digraph" if directed else "graph")
    operator = "->" if directed else "--"
    source = pgv.AGraph(
        string=f"""{declaration} source {{
        graph [rankdir=LR];
        node [shape=box];
        subgraph cluster_outer {{
            graph [label=Outer];
            node [color=blue];
            edge [style=dashed];
            a {operator} b [key=inside, color=red];
            subgraph cluster_inner {{ graph [label=Inner]; c [label=C]; }}
        }}
        b {operator} outside [key=outside];
        subgraph cluster_empty {{ graph [label=Empty]; }}
    }}"""
    )
    cluster = source.get_subgraph("cluster_outer")
    assert cluster.graph_attr["label"] == "Outer"
    assert cluster.node_attr["color"] == "blue"

    copied = source.copy()
    outer_copy = copied.get_subgraph("cluster_outer")
    assert outer_copy is not None
    assert outer_copy.graph_attr["label"] == "Outer"
    assert outer_copy.node_attr["color"] == "blue"
    assert set(outer_copy.nodes()) == {"a", "b", "c"}
    assert set(outer_copy.edges(keys=True)) == {("a", "b", "inside")}
    assert outer_copy.get_subgraph("cluster_inner").get_node("c").attr["label"] == "C"
    assert copied.get_subgraph("cluster_empty") is not None
    assert copied.get_subgraph("cluster_empty").nodes() == []
    assert copied.graph_attr["rankdir"] == "LR"
    assert copied.directed == source.directed
    assert copied.strict == source.strict

    outer_copy.add_edge("new_a", "new_b")
    assert outer_copy.get_node("new_a").attr["color"] == "blue"
    assert outer_copy.get_edge("new_a", "new_b").attr["style"] == "dashed"
    assert "new_a" not in source
    outer_copy.graph_attr["label"] = "Copied outer"
    assert cluster.graph_attr["label"] == "Outer"
    source.close()
    assert b"Copied outer" in copied.draw(format="svg", prog="dot")
    copied.close()


def test_copy_does_not_induce_extra_subgraph_edges():
    source = pgv.AGraph()
    source.add_edge("a", "b")
    child = source.add_subgraph(name="members_only")
    child.add_nodes_from(["a", "b"])
    assert child.edges() == []
    copied = source.copy()
    assert copied.has_edge("a", "b")
    assert copied.get_subgraph("members_only").edges() == []
    copied.close()
    assert source.has_edge("a", "b")
    source.close()


@pytest.mark.parametrize("directed", [False, True])
def test_copy_keeps_anonymous_parallel_edge_membership(directed):
    source = pgv.AGraph(strict=False, directed=directed)
    first = source.add_subgraph(name="first")
    first.add_edge("a", "b", color="red")
    second = source.add_subgraph(name="second")
    second.add_edge("a", "b", color="blue")
    copied = source.copy()
    assert sorted(edge.attr["color"] for edge in copied.edges()) == ["blue", "red"]
    assert [edge.attr["color"] for edge in copied.get_subgraph("first").edges()] == [
        "red"
    ]
    assert [edge.attr["color"] for edge in copied.get_subgraph("second").edges()] == [
        "blue"
    ]
    copied.close()
    source.close()


def test_copy_subgraph_becomes_independent_root():
    source = pgv.AGraph()
    child = source.add_subgraph(name="cluster_child")
    child.add_node("a")
    child.add_subgraph(name="cluster_nested").add_node("b")
    source.add_node("outside")
    copied = child.copy()
    source.close()
    assert set(copied.nodes()) == {"a", "b"}
    assert copied.get_subgraph("cluster_nested").has_node("b")
    assert b"<svg" in copied.draw(format="svg", prog="dot")
    copied.close()


def test_copy_preserves_non_default_charset_in_nested_graphs():
    source = pgv.AGraph(
        string="""graph {
        charset="ISO-8859-1";
        subgraph "cluster_münchen" {
            graph [label="München"];
            "café" [label="café"];
        }
    }"""
    )
    assert source.get_node("café").attr["label"] == "café"
    copied = source.copy()
    source.close()
    assert copied.encoding == "ISO-8859-1"
    assert copied.get_subgraph("cluster_münchen").graph_attr["label"] == "München"
    assert copied.get_node("café").attr["label"] == "café"
    assert "café" in copied.to_string()
    copied.close()
