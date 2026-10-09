import os

import pytest
import pygraphviz as pgv

graphviz_major_version = int(pgv.__graphviz_version__.split(".")[0])


@pytest.mark.skipif(graphviz_major_version < 13, reason="Graphviz version too old")
def test_multiple_reads_same_source_trailing_character(tmp_path):
    """Ensure multiple reads from the same text file with an unexpected trailing
    character don't cause agread fails. See gh-171."""
    fpath = tmp_path / "hello.gv.txt"
    # Original bug was in the read-from-file code path
    with open(fpath, "w") as fh:
        fh.write('digraph G {Hello->World}"')  # note the trailing "

    # Smoke test: sequential reads from the same file via the AGraph constructor
    # should not raise ValueError/DotError
    A = pgv.AGraph(str(fpath))
    B = pgv.AGraph(str(fpath))
    assert A.to_string() == B.to_string()


def _open_fds():
    for fd_dir in ("/proc/self/fd", "/dev/fd"):
        if os.path.isdir(fd_dir):
            return len(os.listdir(fd_dir))
    pytest.skip("cannot list open file descriptors on this platform")


def test_failed_read_does_not_leak_fd(tmp_path):
    """A failed agread must still close its dup'ed file descriptor."""
    fpath = tmp_path / "bad.gv"
    fpath.write_text("graph { a -- }")
    n_before = _open_fds()
    for _ in range(10):
        with pytest.raises(pgv.DotError):
            pgv.AGraph(str(fpath))
    assert _open_fds() == n_before


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
