import sys
sys.path.insert(0,'../..')
import setup_extra
from nose.tools import *
from unittest.mock import patch


def _get_values():
    return None, 'library'


def _get_dpkg_output():
    s = bytes("""libgvc: /usr/local/include/graphviz/gvc.h
                 gphviz: /usr/local/lib/graphviz/graphviz.so""", encoding='utf8')
    return s


def test_try():
    i, l = None, None
    i, l = setup_extra._try_configure(i, l, _get_values)
    assert_equals(i, None)
    assert_equals(l, 'library')


@patch('subprocess.check_output')
def test_dpkg_config(subprocess_mock):
    subprocess_mock.return_value = _get_dpkg_output()
    i, l = setup_extra._dpkg_config()
    assert_equal(i, '/usr/local/include/graphviz')
    assert_equal(l, '/usr/local/lib/graphviz')



def test_b2str():
    s = setup_extra._b2str(bytes('abc', encoding='utf8'))
    assert_equal(s, u'abc')