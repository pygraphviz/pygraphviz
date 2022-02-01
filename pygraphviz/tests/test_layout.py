import pytest
import sys

import pygraphviz as pgv


def test_layout():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    assert [n.attr["pos"] is None for n in A.nodes()] == [True] * 4
    A.layout()
    assert [n.attr["pos"] is not None for n in A.nodes()] == [True] * 4


def test_layout_defaults():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    # print("Pos before",[n.attr["pos"] for n in A.nodes()])
    assert [n.attr["pos"] is None for n in A.nodes()] == [True] * 4
    A.layout()
    assert [n.attr["pos"] is not None for n in A.nodes()] == [True] * 4
    # print("Pos after",[n.attr["pos"] for n in A.nodes()])


@pytest.mark.parametrize(
    "prog",
    ("neato", "dot", "twopi", "circo", "fdp", "osage", "patchwork", "sfdp"),
)
def test_layout_prog_arg(prog):
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])

    # No node position before layout
    assert all(n.attr["pos"] is None for n in A.nodes())

    # All nodes should have a position after layout
    A.layout(prog=prog)
    assert all(n.attr["pos"] is not None for n in A.nodes())

    # Node positions should be different for each of the layouts
    pos = [n.attr["pos"] for n in A.nodes()]
    A.layout(prog="dot")  # Use dot layout as reference
    dot_pos = [n.attr["pos"] for n in A.nodes()]
    assert pos == dot_pos if prog == "dot" else pos != dot_pos


def test_bad_prog_arg_raises():
    A = pgv.AGraph()
    A.add_path([1, 2, 3, 4])
    with pytest.raises(ValueError, match="Program.*is not one of"):
        A.layout(prog="not-a-valid-layout")


class TestExperimentalGraphvizLibInterface:
    def test_layout(self):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        assert [n.attr["pos"] is None for n in A.nodes()] == [True] * 4
        A._layout()
        assert [n.attr["pos"] is not None for n in A.nodes()] == [True] * 4

    def test_layout_defaults(self):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        # print("Pos before",[n.attr["pos"] for n in A.nodes()])
        assert [n.attr["pos"] is None for n in A.nodes()] == [True] * 4
        A._layout()
        assert [n.attr["pos"] is not None for n in A.nodes()] == [True] * 4
        # print("Pos after",[n.attr["pos"] for n in A.nodes()])

    def test_layout_prog_arg(self):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        assert [n.attr["pos"] is None for n in A.nodes()] == [True] * 4
        A._layout(prog=b"dot")
        assert [n.attr["pos"] is not None for n in A.nodes()] == [True] * 4
        dot_pos = [n.attr["pos"] for n in A.nodes()]

        A._layout(prog="dot")
        result = [n.attr["pos"] for n in A.nodes()]
        assert result == dot_pos

        A._layout(prog="twopi")
        result = [n.attr["pos"] for n in A.nodes()]
        assert result != dot_pos

        A._layout(prog="neato")
        result = [n.attr["pos"] for n in A.nodes()]
        assert result != dot_pos

        A._layout(prog="circo")
        result = [n.attr["pos"] for n in A.nodes()]
        assert result != dot_pos

        A._layout(prog="fdp")
        result = [n.attr["pos"] for n in A.nodes()]
        assert result != dot_pos

        A._layout(prog="nop")
        result = [n.attr["pos"] for n in A.nodes()]
        assert result != dot_pos
