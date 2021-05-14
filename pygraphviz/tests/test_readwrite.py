import pygraphviz as pgv
import os
import tempfile
import pathlib


def test_readwrite():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    the_file = tempfile.NamedTemporaryFile(delete=False)
    fname = the_file.name
    # Make sure it can be opened for writing again on Win32
    the_file.close()
    # Pass a string to trigger the code paths that close the newly created file handle
    A.write(fname)
    B = pgv.AGraph(fname)
    assert A == B
    assert B == A
    assert B is not A
    os.unlink(fname)


def test_readwrite_pathobj():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    the_file = tempfile.NamedTemporaryFile(delete=False)
    fname = pathlib.Path(the_file.name)
    # Make sure it can be opened for writing again on Win32
    the_file.close()
    # Pass a string to trigger the code paths that close the newly created file handle
    A.write(fname)
    B = pgv.AGraph(fname)
    assert A == B
    assert B == A
    assert B is not A
    os.unlink(fname)


def test_sequential_reads_windows():
    for _ in range(512):
        pgv.AGraph("digraph {1 -> 2}")
