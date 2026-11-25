import pytest

import pygraphviz as pgv


@pytest.mark.parametrize("name", ["", "%", "%1", "%node", "ordinary", "caf\u00e9"])
@pytest.mark.parametrize("directed", [False, True])
def test_node_names(name, directed):
    graph = pgv.AGraph(directed=directed)
    graph.add_node(name, color="red")
    graph.add_edge(name, "other")

    node = graph.get_node(name)
    assert str(node) == name
    assert node.name == name
    assert node.attr["color"] == "red"
    assert set(graph.nodes()) == {name, "other"}
    assert tuple(graph.edges()[0]) == (name, "other")
    assert graph.edges()[0].name is None

    graph.remove_node(name)
    assert not graph.has_node(name)
    assert list(graph.nodes()) == ["other"]


@pytest.mark.parametrize("name", ["", "ordinary", "caf\u00e9"])
@pytest.mark.parametrize("directed", [False, True])
def test_node_names_roundtrip(name, directed):
    graph = pgv.AGraph(directed=directed)
    graph.add_node(name, color="red")
    graph.add_edge(name, "other")

    restored = pgv.AGraph(string=graph.string())
    assert restored.get_node(name).name == name
    assert restored.get_node(name).attr["color"] == "red"
    assert tuple(restored.edges()[0]) == (name, "other")
    restored.remove_node(name)
    assert not restored.has_node(name)
    assert list(restored.nodes()) == ["other"]
