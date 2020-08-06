import pygraphviz as pgv
import pytest


def test_drawing_error():
    with pytest.raises(AttributeError):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        d = A.draw()


# this is not a very good way to test...
# def test_drawing():
#    A = pgv.AGraph(name='test graph')
#    A.add_path([1,2,3,4])
#    d = A.draw(prog='neato')
#    assert len(d.splitlines()) == 19
# FIXME
# smoke test
# >>> (fd,fname)=tempfile.mkstemp()
# >>> A.draw(fname,format='ps',prog='neato')
# >>> A.draw(fname,prog='neato')


def test_name_error():
    with pytest.raises(ValueError):
        A = pgv.AGraph(name="test graph")
        A.draw("foo", prog="foo")
