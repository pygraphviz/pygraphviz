import sys
import os
import re
from setuptools import setup, Extension

def get_graphviz_version():
    """
    Reads GRAPHVIZ_VERSION_MAJOR from the header file.
    Assumes the header is available at a known path during setup.
    """
    # NOTE: You may need to adjust this path based on your environment
    # or rely on the build system to have already installed it.
    header_path = '/usr/include/graphviz/graphviz_version.h'

    if not os.path.exists(header_path):
        # Fallback/default if header file cannot be read during setup.
        # This should match your expected target version.
        raise RuntimeError(f"Graphviz header file not found at {header_path}.")

    with open(header_path, 'r') as f:
        content = f.read()
        match = re.search(r'#define\s+GRAPHVIZ_VERSION_MAJOR\s+(\d+)', content)
        if match:
            return int(match.group(1))
        else:
            match = re.search(r'#define\s+PACKAGE_VERSION\s+"([0-9.]+)"', content)
            if match:
                maj_ver = match.group(1).split('.')[0]
                return int(maj_ver)

    raise RuntimeError(f"GRAPHVIZ_VERSION_MAJOR macro not found in the header file!")

if __name__ == "__main__":
    WINDOWS = sys.platform == "win32"

    # Get the target version number
    gv_major_version = get_graphviz_version()

    define_macros = []
    swig_options = []

    if WINDOWS:
        define_macros.append(("GVDLL", None))

    swig_options.append("-DGRAPHVIZ_VERSION_MAJOR={}".format(str(gv_major_version)))
    print(f"Defining GRAPHVIZ_VERSION_MAJOR as: {gv_major_version}")

    # List of search paths for where graphviz libs may be installed.
    # The graphviz library subdir contains the plugin libraries (e.g.
    # gvplugin_*). The main graphviz libs (cgraph etc.) are in the
    # parent dir
    library_search_paths = [
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
    extra_kwargs = {} if WINDOWS else {"runtime_library_dirs": library_search_paths}

    extension = [
        Extension(
            name="pygraphviz._graphviz",
            sources=["pygraphviz/graphviz.i"],
            include_dirs=[],
            library_dirs=library_search_paths,
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
            swig_opts=swig_options,
            **extra_kwargs,
        )
    ]

    setup(ext_modules=extension)
