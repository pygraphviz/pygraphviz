import pytest
import unittest
import pygraphviz as pgv

stringify = pgv.testing.stringify


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.null = pgv.AGraph()
        self.K1 = pgv.AGraph()
        self.K1.add_node(1)
        self.K3 = pgv.AGraph()
        self.K3.add_edges_from([(1, 2), (1, 3), (2, 3)])
        self.K5 = pgv.AGraph()
        self.K5.add_edges_from(
            [
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5),
                (2, 3),
                (2, 4),
                (2, 5),
                (3, 4),
                (3, 5),
                (4, 5),
            ]
        )
        self.P3 = pgv.AGraph()
        self.P3.add_path([1, 2, 3])
        self.P5 = pgv.AGraph()
        self.P5.add_path([1, 2, 3, 4, 5])

    def test_strict(self):
        A = pgv.AGraph()  # empty
        assert A.is_strict()
        assert A.nodes() == []

    def test_data(self):
        d = {"a": "b", "b": "c"}
        A = pgv.AGraph(data=d)  # with data
        assert sorted(A.nodes()) == ["a", "b", "c"]
        assert sorted(A.edges()) == [("a", "b"), ("b", "c")]

    def test_str(self):
        A = pgv.AGraph(name="test")
        assert stringify(A) == "strict graph test { }"
        A = pgv.AGraph()
        assert stringify(A) == "strict graph { }"

    def test_repr(self):
        A = pgv.AGraph()
        assert repr(A).startswith("<AGraph <Swig Object of type 'Agraph_t")
        # If graph has a name, it should show up in the repr
        A = pgv.AGraph(name="foo")
        assert "foo" in repr(A)

    def test_equal(self):
        A = pgv.AGraph()
        H = pgv.AGraph()
        assert H == A
        assert H is not A

        assert self.P3 == self.P3

        A = pgv.AGraph()
        A.add_path([1, 2, 3])
        assert A.nodes() == self.P3.nodes()
        assert A.edges() == self.P3.edges()
        assert stringify(A) == stringify(self.P3)
        assert A == self.P3

    def test_not_equal(self):
        A = pgv.AGraph()
        A.add_path([1, 2, 3])
        B = self.P3
        assert A == B

        A.add_node(4)
        assert A != B
        A.remove_node(4)
        assert A == B
        A.add_edge(3, 1)
        assert A != B
        A.remove_edge(3, 1)
        assert A == B

        A.add_node(4, hi=9)
        assert A != B
        A.remove_node(4)
        assert A != B  # attribute 'hi' exists for every node.
        B.node_attr["hi"] = ""
        assert A == B
        A.add_edge(3, 1, hi=9)
        assert A != B
        A.remove_edge(3, 1)
        assert A != B
        B.edge_attr["hi"] = ""
        assert A == B

        # Note: adding node attr gives every node that attribute but empty.
        # Default values are only assigned to nodes added after default is set.
        A.node_attr["low"] = 3
        assert A != B
        B.node_attr["low"] = 3
        assert A == B
        B.node_attr["low"] = 4
        assert A == B

        A.edge_attr["low"] = 3
        assert A != B
        B.edge_attr["low"] = 3
        assert A == B
        B.edge_attr["low"] = 4
        assert A == B

        # graph_attr are not default values -- they are attribute values.
        A.graph_attr.update({"low": 5})
        assert A == B
        # print(sorted(A.nodes()), sorted(B.nodes()))
        # print(sorted(A.edges()), sorted(B.edges()))
        # print(tuple(dict(n.attr) for n in sorted(A.nodes())))
        # print(tuple(dict(n.attr) for n in sorted(B.nodes())))
        # print(tuple(dict(e.attr) for e in sorted(A.edges())))
        # print(tuple(dict(e.attr) for e in sorted(B.edges())))
        # print(dict(A.node_attr), dict(B.node_attr))
        # print(dict(A.edge_attr), dict(B.edge_attr))
        # print(dict(A.graph_attr), dict(B.graph_attr))

    def test_hash(self):
        A = pgv.AGraph()
        A.add_path([1, 2, 3])
        assert hash(A) == hash(self.P3)
        B = A.copy()
        assert hash(A) == hash(B)
        B.add_node(4)
        assert hash(A) != hash(B)

    def test_iter(self):
        assert sorted(self.P3.__iter__()) == ["1", "2", "3"]
        assert sorted(self.P3) == ["1", "2", "3"]

    def test_contains(self):
        assert "1" in self.P3
        assert 10 not in self.P3

    def test_len(self):
        assert len(self.P3) == 3

    def test_getitem(self):
        assert self.P3[1] == ["2"]

    def test_missing_getitem(self):
        with pytest.raises(KeyError):
            a = self.P3[10]

    def test_add_remove_node(self):
        A = pgv.AGraph()
        A.add_node(1)
        assert A.nodes() == ["1"]
        A.add_node("A")
        assert sorted(A.nodes()) == ["1", "A"]
        A.add_node([1])  # nodes must be strings or have a __str__
        assert sorted(A.nodes()) == ["1", "A", "[1]"]

        A.remove_node([1])
        assert sorted(A.nodes()) == ["1", "A"]
        A.remove_node("A")
        assert A.nodes() == ["1"]
        A.remove_node(1)
        assert A.nodes() == []
        with pytest.raises(KeyError):
            A.remove_node(1)

    def test_add_remove_nodes_from(self):
        A = pgv.AGraph()
        A.add_nodes_from(range(3))
        assert sorted(A.nodes()) == ["0", "1", "2"]
        A.remove_nodes_from(range(3))
        assert A.nodes() == []
        with pytest.raises(KeyError):
            A.remove_nodes_from(range(3))

    def test_nodes(self):
        assert sorted(self.P3.nodes()) == ["1", "2", "3"]
        assert sorted(self.P3.nodes_iter()) == ["1", "2", "3"]
        assert sorted(self.P3.iternodes()) == ["1", "2", "3"]

    def test_order(self):
        assert self.P3.number_of_nodes() == 3
        assert self.P3.order() == 3

    def test_has_node(self):
        assert self.P3.has_node(1)
        assert self.P3.has_node("1")
        assert not self.P3.has_node("10")

    def test_get_node(self):
        assert self.P3.get_node(1) == "1"
        one = self.P3.get_node(1)
        nh = one.get_handle()
        node = pgv.Node(self.P3, 1)
        assert node.get_handle() == nh
        assert node == "1"
        with pytest.raises(KeyError):
            pgv.Node(self.P3, 10)

    def test_add_edge(self):
        A = pgv.AGraph()
        A.add_edge(1, 2)
        assert sorted(A.edges()) == [("1", "2")]
        e = (2, 3)
        A.add_edge(e)
        edges = [("1", "2"), ("2", "3")]
        assert sorted(tuple(sorted(e)) for e in A.edges()) == edges

    def test_add_remove_edges_from(self):
        A = pgv.AGraph()
        A.add_edges_from([(1, 2), (2, 3)])
        edges = [("1", "2"), ("2", "3")]
        assert sorted(tuple(sorted(e)) for e in A.edges()) == edges

        A.remove_edge(1, 2)
        assert sorted(A.edges()) == [("2", "3")]
        e = (2, 3)
        A.remove_edge(e)
        assert A.edges() == []
        with pytest.raises(KeyError):
            A.remove_edge(1, 2)

    def test_remove_edges_from(self):
        A = pgv.AGraph()
        A.add_edges_from([(1, 2), (2, 3)])
        edges = [("1", "2"), ("2", "3")]
        assert sorted(tuple(sorted(e)) for e in A.edges()) == edges
        A.remove_edges_from([(1, 2), (2, 3)])
        assert A.edges() == []

    def test_edges(self):
        A = pgv.AGraph()
        A.add_edges_from([(1, 2), (2, 3)])
        edges = [("1", "2"), ("2", "3")]
        assert sorted(tuple(sorted(e)) for e in A.edges()) == edges
        assert sorted(tuple(sorted(e)) for e in A.edges_iter()) == edges
        assert sorted(tuple(sorted(e)) for e in A.iteredges()) == edges

    def test_has_edge(self):
        assert self.P3.has_edge(1, 2)
        assert self.P3.has_edge("1", "2")
        assert not self.P3.has_edge("1", "10")
        assert self.P3.get_edge(1, 2) == ("1", "2")
        eone = self.P3.get_edge(1, 2)
        eh = eone.handle
        edge = pgv.Edge(self.P3, 1, 2)
        assert edge.handle == eh
        assert edge == ("1", "2")
        A = self.P3.copy()
        A.add_node(10)
        with pytest.raises(KeyError):
            pgv.Edge(A, 1, 10)

    def test_neighbors(self):
        A = pgv.AGraph()
        A.add_edges_from([(1, 2), (2, 3)])
        assert sorted(A.neighbors(2)) == ["1", "3"]
        assert sorted(A.neighbors_iter(2)) == ["1", "3"]
        assert sorted(A.iterneighbors(2)) == ["1", "3"]

    def test_degree(self):
        A = pgv.AGraph()
        A.add_edges_from([(1, 2), (2, 3)])
        assert sorted(A.degree()) == [1, 1, 2]
        assert sorted(A.degree_iter()) == [("1", 1), ("2", 2), ("3", 1)]
        assert sorted(A.iterdegree()) == [("1", 1), ("2", 2), ("3", 1)]
        assert sorted(A.iterdegree(A.nodes())) == [("1", 1), ("2", 2), ("3", 1)]
        assert sorted(A.iterdegree(A)) == [("1", 1), ("2", 2), ("3", 1)]
        assert A.degree(1) == 1
        assert A.degree(2) == 2

    def test_clear(self):
        A = pgv.AGraph()
        A.add_edges_from([(1, 2), (2, 3)])
        A.clear()
        assert A.nodes() == []
        assert A.edges() == []

    def test_copy(self):
        A = self.P3.copy()
        assert A.nodes() == ["1", "2", "3"]
        assert A.edges() == [("1", "2"), ("2", "3")]
        assert A is not self.P3
        assert self.P3 is self.P3
        assert stringify(A) == stringify(self.P3)
        assert A == self.P3

        # see Github Issue #354: G.copy() doesn't return a faithful copy
        DG = pgv.AGraph(directed=True)
        DG.add_edge(1, 2)
        DG_copy = DG.copy()
        assert DG_copy.is_directed()
        G = pgv.AGraph()
        G.add_edge(1, 2)
        G_copy = G.copy()
        assert not G_copy.is_directed()

        # Similarly with the strict and name attrs when copying: see gh-426
        A = pgv.AGraph(strict=False, directed=True, name="foobar")
        AC = A.copy()
        assert AC.strict == A.strict
        assert AC.name == A.name

    def test_multigraph_copy_with_keys(self):
        A = pgv.AGraph(strict=False)
        # Add parallel edges
        A.add_edge(1, 2, key="1_2-1")
        A.add_edge(1, 2, key="1_2-2")
        # Add single edge
        A.add_edge(3, 4, key="3_4-1")

        AC = A.copy()

        # Sanity - verify keys exist in original graph
        assert all(key is not None for key in A.edges(keys=True))
        # Verify all edges in copied graph have edges
        assert all(key is not None for key in AC.edges(keys=True))
        # Verify edges, including keys, are identical to original graph
        assert set(A.edges(keys=True)) == set(AC.edges(keys=True))

    def test_add_path(self):
        A = pgv.AGraph()
        A.add_path([1, 2, 3])
        assert A == self.P3

    def test_add_cycle(self):
        A = pgv.AGraph()
        A.add_cycle([1, 2, 3])
        assert A.nodes() == ["1", "2", "3"]
        edges = [("1", "2"), ("1", "3"), ("2", "3")]
        assert sorted(tuple(sorted(e)) for e in A.iteredges()) == edges

    def test_graph_strict(self):
        A = pgv.AGraph()
        A.add_node(1)
        A.add_node(1)  # silent falure
        assert A.nodes() == ["1"]
        A.add_edge(1, 2)
        A.add_edge(1, 2)  # silent falure
        assert A.edges() == [("1", "2")]
        A.add_edge(3, 3)  # self-loops OK with strict
        assert A.edges() == [("1", "2"), ("3", "3")]
        assert A.nodes() == ["1", "2", "3"]

    def test_graph_not_strict(self):
        A = pgv.AGraph(strict=False)
        assert not A.is_strict()
        A.add_node(1)
        A.add_node(1)  # nop
        assert A.nodes() == ["1"]
        A.add_edge(1, 2)
        A.add_edge(1, 2)
        assert A.edges() == [("1", "2"), ("1", "2")]
        A.add_edge(3, 3)
        assert A.edges() == [("1", "2"), ("1", "2"), ("3", "3")]
        assert A.nodes() == ["1", "2", "3"]

        A.add_edge("3", "3", "foo")
        assert A.edges() == [("1", "2"), ("1", "2"), ("3", "3"), ("3", "3")]
        ans = [("1", "2", None), ("1", "2", None), ("3", "3", None), ("3", "3", "foo")]
        assert A.edges(keys=True) == ans
        eone = A.get_edge(3, 3, "foo")
        eh = eone.handle
        edge = pgv.Edge(A, 3, 3, "foo")
        assert edge.handle == eh
        assert edge == ("3", "3")
        assert eone == ("3", "3")
        assert edge.name == "foo"


class TestDiGraphOnly(TestGraph):
    def test_edge(self):
        A = pgv.AGraph(directed=True)
        A.add_edge(1, 2)
        assert A.has_edge(1, 2)
        assert not A.has_edge(2, 1)
        A.add_edge(2, 1)
        assert A.has_edge(2, 1)

    def test_edges(self):
        A = pgv.AGraph(directed=True)
        A.add_edges_from(self.P3.edges())
        edges = [("1", "2"), ("2", "3")]
        assert sorted(tuple(sorted(e)) for e in A.edges()) == edges
        assert sorted(tuple(sorted(e)) for e in A.edges_iter()) == edges
        assert sorted(tuple(sorted(e)) for e in A.out_edges()) == edges
        assert sorted(tuple(sorted(e)) for e in A.out_edges_iter()) == edges
        assert sorted(tuple(sorted(e)) for e in A.in_edges()) == edges
        assert sorted(tuple(sorted(e)) for e in A.in_edges_iter()) == edges
        assert sorted(A.edges(1)) == [("1", "2")]
        assert sorted(A.edges([1, 2])) == [("1", "2"), ("2", "3")]
        assert sorted(A.edges_iter(1)) == [("1", "2")]
        assert sorted(A.out_edges(1)) == [("1", "2")]
        assert sorted(A.out_edges([1, 2])) == [("1", "2"), ("2", "3")]
        assert sorted(A.out_edges_iter(1)) == [("1", "2")]
        assert sorted(A.in_edges(2)) == [("1", "2")]
        assert sorted(A.in_edges([1, 2])) == [("1", "2")]
        assert sorted(A.in_edges_iter(2)) == [("1", "2")]
        assert A.predecessors(1) == []
        assert list(A.predecessors_iter(1)) == []
        assert A.predecessors(2) == ["1"]
        assert list(A.predecessors_iter(2)) == ["1"]
        assert A.successors(1) == ["2"]
        assert list(A.successors_iter(1)) == ["2"]
        assert A.successors(2) == ["3"]
        assert list(A.successors_iter(2)) == ["3"]
        assert sorted(A.out_degree()) == [0, 1, 1]
        assert sorted(A.out_degree(with_labels=True).values()) == [0, 1, 1]
        assert sorted(A.out_degree_iter()) == [("1", 1), ("2", 1), ("3", 0)]
        assert sorted(A.in_degree()) == [0, 1, 1]
        assert sorted(A.in_degree(with_labels=True).values()) == [0, 1, 1]
        assert sorted(A.in_degree_iter()) == [("1", 0), ("2", 1), ("3", 1)]

        assert A.in_degree(1) == 0
        assert A.out_degree(1) == 1
        assert A.in_degree(2) == 1
        assert A.out_degree(2) == 1

        ans = """strict digraph { 1 -> 2; 2 -> 3; }"""
        assert stringify(A) == ans

        ans = """strict digraph { 2 -> 1; 3 -> 2; }"""
        assert stringify(A.reverse()) == ans

    def test_name(self):
        A = pgv.AGraph(name="test")
        assert A.name == "test"
        B = A.reverse()
        assert B.name == "test"


@pytest.mark.parametrize(
    "d",
    (
        {0: {1: {}}, 1: {0: {}, 2: {}}, 2: {1: {}}},  # Dict-of-dicts
        {0: [1], 1: [0, 2], 2: [1]},  # Dict-of-lists
    ),
)
def test_agraph_constructor_dict_input(d):
    """Test AGraph constructor with thing = dod or dol."""
    # d is a dod or dol representation of a path graph with 3 nodes
    A = pgv.AGraph(d)
    assert sorted(A.nodes()) == ["0", "1", "2"]
    assert sorted(A.edges()) == [("0", "1"), ("1", "2")]


def test_agraph_constructor_handle_input():
    """Test AGraph constructor with thing= a Swig pointer - graph handle."""
    base = pgv.AGraph({0: [1], 1: [0, 2], 2: [1]})
    child = pgv.AGraph(base.handle)
    assert base == child
    # AGraphs created from handle reference original graph
    base.remove_node(2)
    assert sorted(child.nodes()) == ["0", "1"]


def test_agraph_constructor_bad_input():
    """AGraph constructor does not support edge lists."""
    with pytest.raises(TypeError, match="Unrecognized input"):
        pgv.AGraph([(0, 1), (1, 2)])


def test_agraph_constructor_string_non_standard_encoding():
    """AGraph constructor with a string specifying non-utf8-encoding."""
    # A path graph string in .dot format with charset specified
    dotstring = 'strict graph "" {\n\tcharset="latin1";\n\t0 -- 1;\n\t1 -- 2;\n}\n'
    A = pgv.AGraph(string=dotstring)
    assert A.encoding == "latin1"
    assert sorted(A.edges()) == [("0", "1"), ("1", "2")]


def test_agraph_equality_node_attrs():
    """Graphs are not equal if node attributes differ."""
    nodes = [0, 1]
    # Create graphs with the same nodes
    A, B = pgv.AGraph(), pgv.AGraph()
    A.add_nodes_from(nodes)
    B.add_nodes_from(nodes)
    # Set default attributes for all nodes in each graph
    A.node_attr["color"] = "red"
    B.node_attr["color"] = "red"
    assert A.get_node(1).attr["color"] == "red"
    assert A == B
    # Change attribute of a single node in B
    B.get_node(1).attr["color"] = "blue"
    # Graphs are no longer considered equal
    assert A != B
    # See #284  A and C should be different
    C = pgv.AGraph()
    A.add_nodes_from(nodes)
    assert A != C


def test_agraph_equality_edge_attrs():
    """Graphs are not equal if edge attributes differ."""
    A, B = pgv.AGraph(), pgv.AGraph()
    A.add_edge(0, 1, weight=1.0)
    B.add_edge(0, 1, weight=1.0)
    assert A == B
    # Change edge attribute
    B.get_edge(0, 1).attr["weight"] = 2.0
    assert A != B
    # See #284  A and C should be different
    C = pgv.AGraph()
    A.add_edge(0, 1)
    assert A != C


def test_agraph_has_edge_single_input_parsing():
    """If len(args) is 1, args[0] is assumed to be a tuple."""
    A = pgv.AGraph({0: [1], 1: [0, 2], 2: [1]})
    assert A.has_edge((0, 1))
    assert not A.has_edge((0, 3))


def test_repr_on_incomplete_initialization():
    """Smoke test to ensure no segfaults from accessing uninitialized attributes
    in __repr__ when object initialization fails. See gh-519."""
    with pytest.raises(TypeError, match="Unrecognized input"):
        A = pgv.AGraph(object())
