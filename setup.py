import sys
from setuptools import setup, Extension

if __name__ == "__main__":
    define_macros = [("SWIG_PYTHON_STRICT_BYTE_CHAR", None)]
    if sys.platform == "win32":
        define_macros.append(("GVDLL", None))

    extension = [
        Extension(
            name="pygraphviz._graphviz",
            sources=["pygraphviz/graphviz_wrap.c"],
            include_dirs=[],
            library_dirs=["/usr/lib64", "/usr/lib64/graphviz", "/usr/local/lib/graphviz"],
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
                "gvpr",
                "gvplugin_core",
                "gvplugin_dot_layout",
                "gvplugin_neato_layout",
            ],
            runtime_library_dirs=["/usr/lib64", "/usr/lib64/graphviz", "/usr/local/lib/graphviz"],
            define_macros=define_macros,
        )
    ]

    setup(ext_modules=extension)
