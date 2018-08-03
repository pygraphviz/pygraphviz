from __future__ import unicode_literals
from nose.tools import *
import pygraphviz as pgv
from os import linesep

class TestGraph:
    def setUp(self):
        self.null = pgv.AGraph()
        self.K1 = pgv.AGraph()
        self.K1.add_node(1)
        self.K3 = pgv.AGraph()
        self.K3.add_edges_from([(1,2),(1,3),(2,3)])
        self.K5 = pgv.AGraph()
        self.K5.add_edges_from([(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)])
        self.P3 = pgv.AGraph()
        self.P3.add_path([1,2,3])
        self.P5 = pgv.AGraph()
        self.P5.add_path([1,2,3,4,5])


    def test_strict(self):
        A =pgv.AGraph()  # empty
        assert_true(A.is_strict())
        assert_equal(A.nodes(), [])

    def test_data(self):
        d = {'a':'b','b':'c'}
        A = pgv.AGraph(data=d) # with data
        assert_equal(sorted(A.nodes()), ['a', 'b', 'c'])
        assert_equal(sorted(A.edges()), [('a', 'b'), ('b', 'c')])


    def test_str(self):
        A = pgv.AGraph(name="test")
        assert_equal(A.string(),
"""strict graph test {
}
""".replace('\n', linesep)
)
        A = pgv.AGraph()
        assert_equal(A.string(),
"""strict graph {
}
""".replace('\n', linesep)
)

    def test_repr(self):
        A = pgv.AGraph()
        assert_equal(A.__repr__()[0:7], '<AGraph')

    def test_equal(self):
        A = pgv.AGraph()
        H = pgv. AGraph()
        assert_true(H==A)
        assert_false(H is A)

    def test_iter(self):
        assert_equal(sorted(list(self.P3.__iter__())), ['1', '2', '3'])
        assert_equal(sorted(self.P3), ['1', '2', '3'])

    def test_contains(self):
        assert_true( '1' in self.P3)
        assert_false(10 in self.P3)

    def test_len(self):
        assert_equal(len(self.P3), 3)

    def test_getitem(self):
        assert_equal(self.P3[1], ['2'])

    @raises(KeyError)
    def test_missing_getitem(self):
        a = self.P3[10]

    def test_add_remove_node(self):
        A = pgv.AGraph()
        A.add_node(1)
        assert_equal(A.nodes(), ['1'])
        A.add_node('A')
        assert_equal(sorted(A.nodes()), ['1', 'A'])
        A.add_node([1]) # nodes must be strings or have a __str__
        assert_equal(sorted(A.nodes()), ['1', 'A', '[1]'])

        A.remove_node([1])
        assert_equal(sorted(A.nodes()), ['1', 'A'])
        A.remove_node('A')
        assert_equal(A.nodes(), ['1'])
        A.remove_node(1)
        assert_equal(A.nodes(), [])
        assert_raises(KeyError, A.remove_node, 1)

    def test_add_remove_nodes_from(self):
        A = pgv.AGraph()
        A.add_nodes_from(range(3))
        assert_equal(sorted(A.nodes()), ['0', '1', '2'])
        A.remove_nodes_from(range(3))
        assert_equal(A.nodes(), [])
        assert_raises(KeyError, A.remove_nodes_from, range(3))


    def test_nodes(self):
        assert_equal(sorted(self.P3.nodes()),['1', '2', '3'])
        assert_equal(sorted(self.P3.nodes_iter()),['1', '2', '3'])
        assert_equal(sorted(self.P3.iternodes()),['1', '2', '3'])

    def test_order(self):
        assert_equal(self.P3.number_of_nodes(), 3)
        assert_equal(self.P3.order(), 3)

    def test_has_node(self):
        assert_true(self.P3.has_node(1))
        assert_true(self.P3.has_node('1'))
        assert_false(self.P3.has_node('10'))

    def test_get_node(self):
        assert_equal(self.P3.get_node(1), '1')
        one = self.P3.get_node(1)
        nh = one.get_handle()
        node = pgv.Node(self.P3,1)
        assert_equal(node.get_handle(), nh)
        assert_equal(node, '1')
        assert_raises(KeyError, pgv.Node, self.P3, 10)


    def test_add_edge(self):
        A = pgv.AGraph()
        A.add_edge(1,2)
        assert_equal(sorted(A.edges()), [('1', '2')])
        e = (2,3)
        A.add_edge(e)
        assert_equal(sorted([tuple(sorted(e)) for e in A.edges()]),
                     [('1', '2'), ('2', '3')])

    def test_add_remove_edges_from(self):
        A = pgv.AGraph()
        A.add_edges_from([(1,2),(2,3)])
        assert_equal(sorted([tuple(sorted(e)) for e in A.edges()]),
                     [('1', '2'), ('2', '3')])

        A.remove_edge(1,2)
        assert_equal(sorted(A.edges()), [('2', '3')])
        e = (2,3)
        A.remove_edge(e)
        assert_equal(A.edges(), [])
        assert_raises(KeyError, A.remove_edge, 1,2)

    def test_remove_edges_from(self):
        A = pgv.AGraph()
        A.add_edges_from([(1,2),(2,3)])
        assert_equal(sorted([tuple(sorted(e)) for e in A.edges()]),
                     [('1', '2'), ('2', '3')])
        A.remove_edges_from([(1,2),(2,3)])
        assert_equal(A.edges(), [])

    def test_edges(self):
        A = pgv.AGraph()
        A.add_edges_from([(1,2),(2,3)])
        assert_equal(sorted([tuple(sorted(e)) for e in A.edges()]),
                     [('1', '2'), ('2', '3')])
        assert_equal(sorted([tuple(sorted(e)) for e in A.edges_iter()]),
                     [('1', '2'), ('2', '3')])
        assert_equal(sorted([tuple(sorted(e)) for e in A.iteredges()]),
                     [('1', '2'), ('2', '3')])

    def test_has_edge(self):
        assert_true(self.P3.has_edge(1,2))
        assert_true(self.P3.has_edge('1','2'))
        assert_false(self.P3.has_edge('1','10'))
        assert_equal(self.P3.get_edge(1,2), ('1', '2'))
        eone = self.P3.get_edge(1,2)
        eh = eone.handle
        edge = pgv.Edge(self.P3,1,2)
        assert_equal(edge.handle, eh)
        assert_equal(edge, ('1', '2'))
        A = self.P3.copy()
        A.add_node(10)
        assert_raises(KeyError, pgv.Edge, A, 1, 10)



    def test_neighbors(self):
        A = pgv.AGraph()
        A.add_edges_from([(1,2),(2,3)])
        assert_equal(sorted(A.neighbors(2)), ['1', '3'])
        assert_equal(sorted(A.neighbors_iter(2)), ['1', '3'])
        assert_equal(sorted(A.iterneighbors(2)), ['1', '3'])


    def test_degree(self):
        A = pgv.AGraph()
        A.add_edges_from([(1,2),(2,3)])
        assert_equal(sorted(A.degree()), [1, 1, 2])
        assert_equal(sorted(A.degree_iter()), [('1', 1), ('2', 2), ('3', 1)])
        assert_equal(sorted(A.iterdegree()), [('1', 1), ('2', 2), ('3', 1)])
        assert_equal(sorted(A.iterdegree(A.nodes())),
                     [('1', 1), ('2', 2), ('3', 1)])
        assert_equal(sorted(A.iterdegree(A)), [('1', 1), ('2', 2), ('3', 1)])
        assert_equal(A.degree(1), 1)
        assert_equal(A.degree(2), 2)


    def test_clear(self):
        A = pgv.AGraph()
        A.add_edges_from([(1,2),(2,3)])
        A.clear()
        assert_equal(A.nodes(), [])
        assert_equal(A.edges(), [])

    def test_copy(self):
        A = self.P3.copy()
        assert_equal(A.nodes(), ['1', '2', '3'])
        assert_equal(A.edges(), [('1', '2'), ('2', '3')])
        assert_equal(A, self.P3)
        assert_false(A is self.P3)
        assert_true(self.P3 is self.P3)

    def test_add_path(self):
        A = pgv.AGraph()
        A.add_path([1,2,3])
        assert_equal(A, self.P3)

    def test_add_cycle(self):
        A = pgv.AGraph()
        A.add_cycle([1,2,3])
        assert_equal(A.nodes(), ['1', '2', '3'])
        assert_equal(sorted([tuple(sorted(e)) for e in A.iteredges()]),
                     [('1', '2'), ('1', '3'), ('2', '3')])


    def test_graph_strict(self):
        A = pgv.AGraph()
        A.add_node(1)
        A.add_node(1) # silent falure
        assert_equal(A.nodes(), ['1'])
        A.add_edge(1,2)
        A.add_edge(1,2) # silent falure
        assert_equal(A.edges(), [('1', '2')])
        A.add_edge(3,3) # self-loops OK with strict
        assert_equal(A.edges(), [('1', '2'), ('3', '3')])
        assert_equal(A.nodes(), ['1', '2', '3'])

    def test_graph_not_strict(self):
        A = pgv.AGraph(strict=False)
        assert_false(A.is_strict())
        A.add_node(1)
        A.add_node(1)  # nop
        assert_equal(A.nodes(), ['1'])
        A.add_edge(1,2)
        A.add_edge(1,2)
        assert_equal(A.edges(), [('1', '2'), ('1', '2')])
        A.add_edge(3,3)
        assert_equal(A.edges(), [('1', '2'), ('1', '2'), ('3', '3')])
        assert_equal(A.nodes(), ['1', '2', '3'])

        A.add_edge('3','3','foo')
        assert_equal(A.edges(),
        [('1', '2'), ('1', '2'), ('3', '3'), ('3', '3')])
        assert_equal(A.edges(keys=True),
        [('1', '2', None), ('1', '2', None),
         ('3', '3', None), ('3', '3', 'foo')])
        eone = A.get_edge(3,3,'foo')
        eh = eone.handle
        edge = pgv.Edge(A,3,3,'foo')
        assert_equal(edge.handle, eh)
        assert_equal(edge, ('3', '3'))
        assert_equal(eone, ('3', '3'))
        assert_equal(edge.name, 'foo')


class TestDiGraphOnly(TestGraph):
    def test_edge(self):
        A =pgv.AGraph(directed=True)
        A.add_edge(1,2)
        assert_true(A.has_edge(1,2))
        assert_false(A.has_edge(2,1))
        A.add_edge(2,1)
        assert_true(A.has_edge(2,1))

    def test_edges(self):
        A = pgv.AGraph(directed=True)
        A.add_edges_from(self.P3.edges())
        assert_equal(sorted([tuple(sorted(e)) for e in A.edges()]),
                    [('1', '2'), ('2', '3')])
        assert_equal(sorted([tuple(sorted(e)) for e in A.edges_iter()]),
                    [('1', '2'), ('2', '3')])
        assert_equal(sorted([tuple(sorted(e)) for e in A.out_edges()]),
                    [('1', '2'), ('2', '3')])
        assert_equal(sorted([tuple(sorted(e)) for e in A.out_edges_iter()]),
                    [('1', '2'), ('2', '3')])
        assert_equal(sorted([tuple(sorted(e)) for e in A.in_edges()]),
                    [('1', '2'), ('2', '3')])
        assert_equal(sorted([tuple(sorted(e)) for e in A.in_edges_iter()]),
                    [('1', '2'), ('2', '3')])
        assert_equal(sorted(A.edges(1)), [('1', '2')])
        assert_equal(sorted(A.edges([1, 2])), [('1', '2'), ('2', '3')])
        assert_equal(sorted(A.edges_iter(1)), [('1', '2')])
        assert_equal(sorted(A.out_edges(1)), [('1', '2')])
        assert_equal(sorted(A.out_edges([1, 2])), [('1', '2'), ('2', '3')])
        assert_equal(sorted(A.out_edges_iter(1)), [('1', '2')])
        assert_equal(sorted(A.in_edges(2)), [('1', '2')])
        assert_equal(sorted(A.in_edges([1, 2])), [('1', '2')])
        assert_equal(sorted(A.in_edges_iter(2)), [('1', '2')])
        assert_equal(A.predecessors(1), [])
        assert_equal(list(A.predecessors_iter(1)),[])
        assert_equal(A.predecessors(2), ['1'])
        assert_equal(list(A.predecessors_iter(2)), ['1'])
        assert_equal(A.successors(1), ['2'])
        assert_equal(list(A.successors_iter(1)), ['2'])
        assert_equal(A.successors(2), ['3'])
        assert_equal(list(A.successors_iter(2)), ['3'])
        assert_equal (sorted(A.out_degree()), [0, 1, 1])
        assert_equal(sorted(A.out_degree(with_labels=True).values()),
                     [0, 1, 1])
        assert_equal(sorted(A.out_degree_iter()),
                     [('1', 1), ('2', 1), ('3', 0)])
        assert_equal(sorted(A.in_degree()), [0, 1, 1])
        assert_equal(sorted(A.in_degree(with_labels=True).values()),
                     [0, 1, 1])
        assert_equal(sorted(A.in_degree_iter()),
                     [('1', 0), ('2', 1), ('3', 1)])

        assert_equal(A.in_degree(1), 0)
        assert_equal(A.out_degree(1), 1)
        assert_equal(A.in_degree(2), 1)
        assert_equal(A.out_degree(2), 1)

        # Have to use expandtabs(1) not 0 because of PyPy bug
        # https://bitbucket.org/pypy/pypy/issues/2113/calling-strexpandtabs-0-crashes-with-a
        assert_equal(A.string().expandtabs(1),
"""strict digraph {
 1 -> 2;
 2 -> 3;
}
""".replace('\n', linesep)
)

        assert_equal(A.reverse().string().expandtabs(1),
"""strict digraph {
 2 -> 1;
 3 -> 2;
}
""".replace('\n', linesep)
)

    def test_name(self):
        A = pgv.AGraph(name='test')
        assert_equal(A.name, 'test')
        B = A.reverse()
        assert_equal(B.name, 'test')
