import pygraphviz as pgv


def test_del():
    A = pgv.AGraph()
    A.add_node(1, foo="bar")
    # For some reasons after porting to Python 3 clear often cause infinite loop
    A.delete_node("1")
    assert len(A) == 0


def test_clear_node_with_attributes():
    A = pgv.AGraph()
    A.add_node(1, foo="bar")
    # For some reasons after porting to Python 3 clear often cause infinite loop
    A.clear()
    assert len(A) == 0
    assert A.nodes() == []
    assert A.node_attr.keys() in ([], ["label"])


def test_clear_graph_attributes():
    A = pgv.AGraph()
    A.add_node(1, foo="bar")
    A.graph_attr.update(landscape="true", ranksep="0.1")
    # For some reasons after porting to Python 3 clear often cause infinite loop
    A.clear()
    assert len(A) == 0
    assert A.nodes() == []
    assert A.node_attr.keys() in ([], ["label"])
    assert A.graph_attr.keys() == []
