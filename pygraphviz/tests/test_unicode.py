import pygraphviz as pgv


def test_name_unicode():
    A = pgv.AGraph(name="unicode")
    assert A.name == "unicode"


def test_node_encoding():
    A = pgv.AGraph(encoding="UTF-8")
    hello = "Здравствуйте!"
    A.add_node(hello)
    n = A.get_node(hello)
    assert n.name == hello

    n.attr["goodbye"] = "До свидания"
    assert n.attr["goodbye"] == "До свидания"


def test_edge_encoding():
    A = pgv.AGraph(encoding="UTF-8")
    hello = "שלום"
    A.add_edge(hello, hello, key=1)  # self loop
    e = A.get_edge(hello, hello)
    assert e.name == "1"
    assert e == (hello, hello)

    e.attr["hello"] = hello
    assert e.attr["hello"] == hello


def test_from_string():
    # test unicode in from_string()
    t = "测试"
    G = pgv.AGraph()
    G.add_node(t)
    ug = str(G)
    sg = str(G)
    G1 = pgv.AGraph(ug)
    G2 = pgv.AGraph(sg)
    assert str(G1) == str(G2)
