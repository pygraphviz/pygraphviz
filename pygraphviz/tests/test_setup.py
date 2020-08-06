import sys
from unittest.mock import patch

# inside distributed version, there is no setup_extra files already
sys.path.insert(0, "../..")
try:
    setup_extra = __import__("setup_extra")
except ImportError:
    setup_extra = None


def _get_values():
    return None, "library"


def _get_dpkg_output():
    r = """libgvc: /usr/local/include/graphviz/gvc.h
                     gphviz: /usr/local/lib/graphviz/graphviz.so"""
    s = bytes(r, encoding="utf8")
    return s


def test_try():
    if setup_extra:
        i, l = None, None
        i, l = setup_extra._try_configure(i, l, _get_values)
        assert i is None
        assert l == "library"


@patch("subprocess.check_output")
def test_dpkg_config(subprocess_mock):
    if setup_extra:
        subprocess_mock.return_value = _get_dpkg_output()
        i, l = setup_extra._dpkg_config()
        assert i == "/usr/local/include/graphviz"
        assert l == "/usr/local/lib/graphviz"


def test_b2str():
    if setup_extra:
        r = bytes("abc", encoding="utf8")
        s = setup_extra._b2str(r)
        assert s == "abc"
