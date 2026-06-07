import os
import re
import subprocess
import sys
from setuptools import setup, Extension

if __name__ == "__main__":
    WINDOWS = sys.platform == "win32"
    MACOS = sys.platform == "darwin"

    # FIXME: This should be handled with the cibuildwheel windows path specification
    # but for whatever reason it's not being picked up correctly. This is a hack
    # to make this work with the specific installation locations used within the
    # cibuildwheel environment.
    if WINDOWS:
        os.environ["PATH"] += ";C:\\graphviz\\bin"
    # Extract graphviz major version from command line
    # NOTE: A GRAPHVIZ_MAJOR_VERSION macro was added in Graphviz v14.0, but is
    # not availble prior - so parsing the CLI version output is the only
    # reliable way to get portable version info across all versions.
    # If, in the future, it is possible/reasonable to set Graphviz 14 as a
    # minimum supported version, then this should be replaced with the macro
    # See gh-573 for further discussion
    try:  # Better exception message if graphviz not installed
        version_str = subprocess.check_output(["dot", "-V"], stderr=subprocess.STDOUT)
    except FileNotFoundError:
        raise FileNotFoundError(
            "\n\nCould not find `dot` executable!\n"
            "Graphviz must be installed to build pygraphviz from source.\n\n"
        )

    vm = re.match(r"dot - graphviz version (\d+)", version_str.decode())
    graphviz_major_version = int(vm.string[: vm.end()].split(" ")[-1])
    print(f"Detected Graphviz version {graphviz_major_version}")
    # Pass version info into swig build
    swig_options = [f"-DGRAPHVIZ_VERSION_MAJOR={graphviz_major_version}"]

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

    if MACOS:
        # macOS uses the native Quartz (CoreText/CoreGraphics) renderer for
        # anti-aliased raster output (png/pdf/jpg/gif/...). It supersedes gd,
        # which is therefore not built on macOS (--with-libgd=no), letting the
        # wheel build drop libpng/freetype/libgd entirely. The plugin's
        # library struct is registered as a builtin in graphviz.i;
        # ApplicationServices supplies the CoreGraphics/CoreText symbols.
        libraries.append("gvplugin_quartz")
        extra_kwargs.setdefault("extra_link_args", [])
        extra_kwargs["extra_link_args"] += ["-framework", "ApplicationServices"]
    elif WINDOWS:
        # Windows uses the native GDI+ renderer (png/jpg/gif/bmp/tiff/emf),
        # the Windows analog of Quartz on macOS, in place of gd. The official
        # graphviz installer ships gvplugin_gdiplus.dll and its import lib
        # gvplugin_gdiplus.lib; GDI+ uses Windows system fonts (no fontconfig).
        # The plugin's library struct is registered as a builtin in graphviz.i.
        libraries.append("gvplugin_gdiplus")
    else:
        # Linux: pango/cairo for anti-aliased text in png/svg/pdf/ps, kept
        # alongside gd because cairo/pango have no gif/jpg device (gd also
        # supplies the legacy gd/gd2/wbmp formats). Both plugin structs are
        # registered as builtins in graphviz.i; pango pulls in cairo/pango/
        # fontconfig/freetype at link time, which auditwheel bundles.
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
