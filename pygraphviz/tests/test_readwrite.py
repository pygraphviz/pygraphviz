import pygraphviz as pgv


def test_readwrite(tmp_path):
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    path = tmp_path / "rw_win32_testfile"
    with path.open("w") as fh:
        assert not fh.closed
    # Make sure it can be opened for writing again on Win32
    assert fh.closed
    # Pass a string to trigger the code paths that close the newly created file handle
    A.write(path)
    B = pgv.AGraph(path)
    assert A == B
    assert B == A
    assert B is not A


def test_readwrite_pathobj(tmp_path):
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    path = tmp_path / "rw_win32_testfile"
    with path.open("w") as fh:
        assert not fh.closed
    # Make sure it can be opened for writing again on Win32
    assert fh.closed
    # Pass a string to trigger the code paths that close the newly created file handle
    A.write(path)
    B = pgv.AGraph(path)
    assert A == B
    assert B == A
    assert B is not A


def test_sequential_reads_windows():
    for _ in range(512):
        pgv.AGraph("digraph {1 -> 2}")
