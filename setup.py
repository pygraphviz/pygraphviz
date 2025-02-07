import sys
from setuptools import setup, Extension
import platform
import os

def get_homebrew_graphviz():
    paths = {
        'include_dirs': [],
        'library_dirs': []
    }
    # This could be different
    if platform.machine() == 'arm64':
        brew_prefix = '/opt/homebrew'
    else:
        brew_prefix = '/usr/local'

    # Add graphviz-specific paths
    graphviz_include = os.path.join(brew_prefix, 'include', 'graphviz')
    graphviz_lib = os.path.join(brew_prefix, 'lib')
    plugin_lib = os.path.join(graphviz_lib, 'graphviz')
    paths['include_dirs'].append(graphviz_include)
    paths['library_dirs'].append(graphviz_lib)
    paths['library_dirs'].append(plugin_lib)
    return paths


if __name__ == "__main__":
    define_macros = [("SWIG_PYTHON_STRICT_BYTE_CHAR", None)]
    if sys.platform == "win32":
        define_macros.append(("GVDLL", None))
        kwargs_ext = {
                'include_dirs': ['C:\Program Files\Graphviz\include'],
                'library_dirs': ['C:\Program Files\Graphviz\lib']}
    elif platform.system() == 'Darwin':
        kwargs_ext = get_homebrew_graphviz()
    else:
        kwargs_ext = {}
    extension = [
        Extension(
            name="pygraphviz._graphviz",
            sources=["pygraphviz/graphviz_wrap.c"],
            # cdt does not link to cgraph, whereas cgraph links to cdt.
            # thus, cdt needs to come first in the library list to be sure
            # that both libraries are linked in the final built .so (if cgraph
            # is first, the implicit inclusion of cdt can lead to an incomplete
            # link list, having only cdt and preventing the module from being loaded with
            # undefined symbol errors. seen under PyPy on Linux.)
            libraries=[
                "cdt",
                "cgraph",
                "gvc",
                #"gvpr",
                "gvplugin_core",
                "gvplugin_dot_layout",
                "gvplugin_neato_layout",
                # "gvplugin_visio",
            ],
            define_macros=define_macros,
            **kwargs_ext,
        )
    ]

    setup(ext_modules=extension)

