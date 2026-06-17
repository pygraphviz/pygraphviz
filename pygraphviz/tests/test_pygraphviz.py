import pytest

import pygraphviz as pgv


def test_graphviz_version():
    """Test to ensure package exports the __graphviz_version__ attribute, which
    holds the version info for the packaged graphviz version."""
    # Smoke test - the following lines will fail if e.g. __graphviz_version__
    # is not present or the version string takes an unexpected form
    graphviz_version = pgv.__graphviz_version__
    vmaj, vmin, vpatch = graphviz_version.split(".")
    assert int(vmaj) >= 2
