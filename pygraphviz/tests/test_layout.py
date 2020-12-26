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


def test_layout_prog_arg():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    assert [n.attr["pos"] is None for n in A.nodes()] == [True] * 4
    A.layout(prog="dot")
    assert [n.attr["pos"] is not None for n in A.nodes()] == [True] * 4
    dot_pos = [n.attr["pos"] for n in A.nodes()]

    A.layout(prog="dot")
    result = [n.attr["pos"] for n in A.nodes()]
    assert result == dot_pos

    A.layout(prog="twopi")
    result = [n.attr["pos"] for n in A.nodes()]
    assert result != dot_pos

    A.layout(prog="neato")
    result = [n.attr["pos"] for n in A.nodes()]
    assert result != dot_pos

    A.layout(prog="circo")
    result = [n.attr["pos"] for n in A.nodes()]
    assert result != dot_pos

    A.layout(prog="fdp")
    result = [n.attr["pos"] for n in A.nodes()]
    assert result != dot_pos


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
