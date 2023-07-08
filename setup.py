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
            library_dirs=[],
            # cdt does not link to cgraph, whereas cgraph links to cdt.
            # thus, cdt needs to come first in the library list to be sure
            # that both libraries are linked in the final built .so (if cgraph
            # is first, the implicit inclusion of cdt can lead to an incomplete
            # link list, having only cdt and preventing the module from being loaded with
            # undefined symbol errors. seen under PyPy on Linux.)
            libraries=["cdt", "cgraph", "gvc"],
            define_macros=define_macros,
        )
    ]

    setup(ext_modules=extension)
