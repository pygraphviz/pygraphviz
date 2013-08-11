import unittest
import pygraphviz as pgv

class GraphTester(unittest.TestCase):
    def test_edges(self):
        a = pgv.AGraph()
        a.add_edge('a', 'b')
        a.add_edge('a', 'c')
        a.add_edge('a', 'd')
        a.add_edge('a', 'e')
        a.add_edge('a', 'a')
        a.add_edge('f', 'a')
        a.add_edge('g', 'a')
        a.add_edge('g', 'b')
        a.add_edge('c', 'g')
        a.add_edge('a', 'a')
        a.add_edge('d', 'a')

        self.assertItemsEqual(a.edges('a'), [ ('a', 'b'), ('a', 'c'),
            ('a', 'd'), ('a', 'e'), ('f', 'a'), ('g', 'a'), ('a', 'a'), ])
        self.assertItemsEqual(a.edges('g'), [('g', 'a'), ('g', 'b'), ('c', 'g')])
        self.assertItemsEqual(a.edges('c'), [('c', 'g'), ('a', 'c')])
        self.assertItemsEqual(a.edges(['g', 'c']),
                [('g', 'a'), ('g', 'b'), ('c', 'g'), ('a', 'c')])
        self.assertItemsEqual(a.edges(['b', 'e']),
                [('a', 'b'), ('a', 'e'), ('g', 'b')])
        self.assertItemsEqual(a.edges(), [ ('a', 'b'), ('a', 'c'), ('a', 'd'),
        ('a', 'e'), ('f', 'a'), ('g', 'a'), ('g', 'b'), ('c', 'g'), ('a', 'a')])

    def test_edges_non_strict(self):
        a = pgv.AGraph(strict=False)
        a.add_edge('a', 'b')
        a.add_edge('a', 'c')
        a.add_edge('a', 'd')
        a.add_edge('a', 'e')
        a.add_edge('f', 'a')
        a.add_edge('g', 'a')
        a.add_edge('g', 'b')
        a.add_edge('c', 'g')
        a.add_edge('a', 'a')
        a.add_edge('a', 'a')
        a.add_edge('d', 'a')

        self.assertItemsEqual(a.edges('a'), [ ('a', 'b'), ('a', 'c'),
            ('a', 'd'), ('a', 'e'), ('f', 'a'), ('g', 'a'), ('a', 'a'), ('a', 'a'),
            ('d', 'a')])
        self.assertItemsEqual(a.edges('g'), [('g', 'a'), ('g', 'b'), ('c', 'g')])
        self.assertItemsEqual(a.edges('c'), [('c', 'g'), ('a', 'c')])
        self.assertItemsEqual(a.edges(['g', 'c']),
                [('g', 'a'), ('g', 'b'), ('c', 'g'), ('a', 'c')])
        self.assertItemsEqual(a.edges(['b', 'e']),
                [('a', 'b'), ('a', 'e'), ('g', 'b')])
        self.assertItemsEqual(a.edges(), [ ('a', 'b'), ('a', 'c'), ('a', 'd'),
        ('a', 'e'), ('f', 'a'), ('g', 'a'), ('g', 'b'), ('c', 'g'), ('a', 'a'),
        ('a', 'a'), ('d', 'a')])
if __name__ == '__main__':
    unittest.main()
