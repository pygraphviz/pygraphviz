import os
import sys
from setuptools import setup, Extension

if __name__ == "__main__":
    WINDOWS = sys.platform == "win32"

    define_macros = [("SWIG_PYTHON_STRICT_BYTE_CHAR", None)]
    if WINDOWS:
        define_macros.append(("GVDLL", None))

    # Check for custom graphviz prefix (used by cibuildwheel builds)
    graphviz_prefix = os.environ.get("GRAPHVIZ_PREFIX", "")

    if graphviz_prefix:
        # Wheel build: graphviz is at a known prefix
        include_dirs = [os.path.join(graphviz_prefix, "include")]
        lib_dir = os.path.join(graphviz_prefix, "lib")
        if WINDOWS:
            plugin_lib_dir = lib_dir
        else:
            plugin_lib_dir = os.path.join(graphviz_prefix, "lib", "graphviz")
        library_dirs = [lib_dir, plugin_lib_dir]
        # Repair tools (auditwheel/delocate/delvewheel) handle rpath for wheels
        extra_kwargs = {}
    else:
        # Development install: search system paths
        include_dirs = []
        # List of search paths for where graphviz libs may be installed.
        # The graphviz library subdir contains the plugin libraries (e.g.
        # gvplugin_*). The main graphviz libs (cgraph etc.) are in the
        # parent dir
        library_dirs = [
            "/usr/lib/x86_64-linux-gnu",  # Ubuntu x86_64
            "/usr/lib/x86_64-linux-gnu/graphviz",
            "/opt/homebrew/lib",  # Macos, homebrew aarch64
            "/opt/homebrew/lib/graphviz",
            "/usr/lib64",  # Fedora
            "/usr/lib64/graphviz",
            "/usr/local/lib",  # source install / macos homebrew x86_64
            "/usr/local/lib/graphviz",
            "/opt/local/lib",
            "/opt/local/lib/graphviz",
        ]
        # runtime_library_dirs must not be defined with windows else setup will fail
        extra_kwargs = {} if WINDOWS else {"runtime_library_dirs": library_dirs}

    extension = [
        Extension(
            name="pygraphviz._graphviz",
            sources=["pygraphviz/graphviz_wrap.c"],
            include_dirs=include_dirs,
            library_dirs=library_dirs,
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
                "gvplugin_core",
                "gvplugin_dot_layout",
                "gvplugin_neato_layout",
            ],
            define_macros=define_macros,
            **extra_kwargs,
        )
    ]

    setup(ext_modules=extension)
