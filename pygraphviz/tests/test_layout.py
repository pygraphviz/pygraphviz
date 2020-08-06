import pygraphviz as pgv


def test_layout():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    A.layout()
    assert ["pos" in n.attr for n in A.nodes()] == [True, True, True, True]
