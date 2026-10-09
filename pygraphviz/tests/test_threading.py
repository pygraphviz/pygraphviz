import sys
import sysconfig
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

import pygraphviz as pgv


@pytest.mark.skipif(
    not sysconfig.get_config_var("Py_GIL_DISABLED"),
    reason="requires free-threaded Python",
)
def test_gil_not_reenabled():
    # Importing pygraphviz must not re-enable the GIL (see graphviz.i)
    assert not sys._is_gil_enabled()


def _build_and_render(i):
    A = pgv.AGraph(directed=True, name=f"G{i}")
    A.add_path(list(range(20)))
    A.add_edge(19, 0, color="red", label=f"edge {i}")
    A.node_attr["shape"] = "box"
    A.get_node(5).attr["label"] = "<<b>html</b>>"
    sub = A.add_subgraph([1, 2, 3], name="cluster_sub")
    sub.graph_attr["label"] = "sub"
    A.delete_node(10)
    # round-trip through Graphviz's parser
    B = pgv.AGraph(string=A.to_string())
    B.layout(prog="dot")
    return (
        B.number_of_nodes(),
        B.number_of_edges(),
        B.draw(format="svg", prog="dot"),
        B.draw(format="plain", prog="neato"),
    )


def test_concurrent_use():
    # Graphviz uses process-wide state, so concurrent calls must be serialized
    # (by the GIL, or by pygraphviz's lock on free-threaded Python)
    n_threads = 8
    n_iter = 5
    expected = [_build_and_render(i) for i in range(n_iter)]
    barrier = threading.Barrier(n_threads)

    def work():
        barrier.wait()
        return [_build_and_render(i) for i in range(n_iter)]

    with ThreadPoolExecutor(n_threads) as executor:
        futures = [executor.submit(work) for _ in range(n_threads)]
        for future in futures:
            assert future.result() == expected
