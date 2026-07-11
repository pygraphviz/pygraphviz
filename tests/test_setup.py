import runpy
import subprocess
from pathlib import Path

import pytest


SETUP_GLOBALS = runpy.run_path(Path(__file__).parents[1] / "setup.py")
graphviz_paths_from_pkg_config = SETUP_GLOBALS["_graphviz_paths_from_pkg_config"]


def test_graphviz_paths_from_pkg_config(monkeypatch):
    values = {
        "--variable=includedir": "/opt/graphviz/include\n",
        "--variable=libdir": "/opt/graphviz/lib\n",
    }

    def check_output(command, **kwargs):
        assert command[0] == "pkg-config"
        assert command[2] == "libgvc"
        return values[command[1]]

    monkeypatch.setattr(subprocess, "check_output", check_output)

    assert graphviz_paths_from_pkg_config() == (
        ["/opt/graphviz/include"],
        ["/opt/graphviz/lib", "/opt/graphviz/lib/graphviz"],
    )


@pytest.mark.parametrize(
    "error",
    [FileNotFoundError(), subprocess.CalledProcessError(1, ["pkg-config"])],
)
def test_graphviz_paths_from_pkg_config_falls_back(monkeypatch, error):
    def check_output(*args, **kwargs):
        raise error

    monkeypatch.setattr(subprocess, "check_output", check_output)

    assert graphviz_paths_from_pkg_config() is None
