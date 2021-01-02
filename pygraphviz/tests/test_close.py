import pygraphviz as pgv


def test_context_manager():
    with pgv.AGraph() as ag:
        ag0 = ag
    assert ag0.handle != None


def test_double_close():
    ag = pgv.AGraph()
    ag.close()
    assert ag.handle is None
    ag.close()
