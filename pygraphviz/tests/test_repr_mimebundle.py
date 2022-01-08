import pygraphviz as pgv
import pytest


def test_repr_output():
    A = pgv.AGraph()
    A.add_path([1, 2, 3, 4])
    assert repr(A).startswith("<AGraph <Swig Object of type 'Agraph_t")
    A.layout()
    assert A._svg_repr().startswith("<?xml version=")


def test_mimetype_select():
    A = pgv.AGraph()
    A.add_path([1, 2, 3, 4])
    assert "text/plain" in A._repr_mimebundle_().keys()
    assert not "image/svg+xml" in A._repr_mimebundle_().keys()
    A.layout()
    assert "image/svg+xml" in A._repr_mimebundle_().keys()


def test_svg_repr_error():
    with pytest.raises(AttributeError):
        A = pgv.AGraph()
        A._svg_repr()
