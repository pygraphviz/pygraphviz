import os
import re
import subprocess
import sys
from setuptools import setup, Extension


def _graphviz_paths_from_pkg_config():
    """Return Graphviz include and library paths reported by pkg-config."""
    try:
        include_dir = subprocess.check_output(
            ["pkg-config", "--variable=includedir", "libgvc"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        lib_dir = subprocess.check_output(
            ["pkg-config", "--variable=libdir", "libgvc"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None

    if not include_dir or not lib_dir:
        return None

    plugin_lib_dir = os.path.join(lib_dir, "graphviz")
    return [include_dir], [lib_dir, plugin_lib_dir]


if __name__ == "__main__":
    WINDOWS = sys.platform == "win32"
    MACOS = sys.platform == "darwin"

    # Extract graphviz major version from command line
    # NOTE: A GRAPHVIZ_MAJOR_VERSION macro was added in Graphviz v14.0, but is
    # not available prior - so parsing the CLI version output is the only
    # reliable way to get portable version info across all versions.
    # If, in the future, it is possible/reasonable to set Graphviz 14 as a
    # minimum supported version, then this should be replaced with the macro
    # See gh-573 for further discussion
    try:  # Better exception message if graphviz not installed
        version_str = subprocess.check_output(["dot", "-V"], stderr=subprocess.STDOUT)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "\n\nCould not find `dot` executable!\n"
            "Graphviz must be installed to build pygraphviz from source.\n\n"
        ) from e

    vm = re.match(r"dot - graphviz version \d+(\.\d+)+", version_str.decode())
    graphviz_version = vm.string[: vm.end()].split(" ")[-1]
    print(f"Detected Graphviz version {graphviz_version}")

    vmaj, vmin, vpatch = graphviz_version.split(".")
    # NOTE: int() is not strictly necessary, but used as implicit validation of
    # version string
    graphviz_major_version = int(vmaj)
    graphviz_minor_version = int(vmin)
    graphviz_patch_version = int(vpatch)
    # Pass version info into swig build
    swig_options = [
        f"-DGRAPHVIZ_VERSION_MAJOR={graphviz_major_version}",
        f"-DGRAPHVIZ_VERSION_MINOR={graphviz_minor_version}",
        f"-DGRAPHVIZ_VERSION_PATCH={graphviz_patch_version}",
    ]

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
        graphviz_paths = None if WINDOWS else _graphviz_paths_from_pkg_config()
        if graphviz_paths:
            include_dirs, library_dirs = graphviz_paths
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

    # cdt does not link to cgraph, whereas cgraph links to cdt.
    # thus, cdt needs to come first in the library list to be sure
    # that both libraries are linked in the final built .so (if cgraph
    # is first, the implicit inclusion of cdt can lead to an incomplete
    # link list, having only cdt and preventing the module from being loaded with
    # undefined symbol errors. seen under PyPy on Linux.)
    libraries = [
        "cdt",
        "cgraph",
        "gvc",
        "gvplugin_core",
        "gvplugin_dot_layout",
        "gvplugin_neato_layout",
    ]

    # Raster renderer per platform (see graphviz.i for the rationale).
    if MACOS:
        # Native Quartz renderer; needs the ApplicationServices framework.
        libraries.append("gvplugin_quartz")
        extra_kwargs.setdefault("extra_link_args", [])
        extra_kwargs["extra_link_args"] += ["-framework", "ApplicationServices"]
    else:
        # Windows + Linux: pango/cairo (centered text) plus gd for gif/jpg.
        libraries.append("gvplugin_gd")
        libraries.append("gvplugin_pango")

    extension = [
        Extension(
            name="pygraphviz._graphviz",
            sources=["pygraphviz/graphviz.i"],
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            libraries=libraries,
            define_macros=define_macros,
            swig_opts=swig_options,
            **extra_kwargs,
        )
    ]

    setup(ext_modules=extension)
