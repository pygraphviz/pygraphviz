import pytest
import sys

import pygraphviz as pgv

# FIXME: Windows 'CMake' installer does not install neato, gvpr, fdp and others
# https://gitlab.com/graphviz/graphviz/-/issues/1753
@pytest.mark.xfail(sys.platform == "win32", reason="does not run on windows")
def test_layout():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    A.layout()
    assert ["pos" in n.attr for n in A.nodes()] == [True, True, True, True]
