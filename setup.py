from glob import glob
import os
import sys
from setuptools import setup, Extension

if sys.version_info[:2] < (3, 7):
    error = (
        "PyGraphviz requires Python version 3.7 or later (%d.%d detected)."
        % sys.version_info[:2]
    )
    sys.stderr.write(error + "\n")
    sys.exit(-1)


name = "pygraphviz"
description = "Python interface to Graphviz"

with open("README.rst", "r") as fh:
    long_description = fh.read()

license = "BSD"
authors = {
    "Hagberg": ("Aric Hagberg", "aric.hagberg@gmail.com"),
    "Schult": ("Dan Schult", "dschult@colgate.edu"),
    "Renieris": ("Manos Renieris", ""),
}
url = "http://pygraphviz.github.io"
download_url = "https://pypi.python.org/pypi/pygraphviz"
platforms = ["Linux", "Mac OSX", "Microsoft :: Windows"]
keywords = ["Networks", "Graph Visualization", "network", "graph", "graph drawing"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: C",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Visualization",
]

with open("pygraphviz/__init__.py") as fid:
    for line in fid:
        if line.startswith("__version__"):
            version = line.strip().split()[-1][1:-1]
            break

packages = ["pygraphviz", "pygraphviz.tests"]
docdirbase = f"share/doc/pygraphviz-{version}"
data = [
    (docdirbase, glob("*.txt")),
    (os.path.join(docdirbase, "examples"), glob("examples/*.py")),
    (os.path.join(docdirbase, "examples"), glob("examples/*.dat")),
    (os.path.join(docdirbase, "examples"), glob("examples/*.dat.gz")),
]
package_data = {
    "": ["*.txt"],
}

if __name__ == "__main__":
    define_macros = []
    if sys.platform == "win32":
        define_macros = define_macros.append(("GVDLL", None))

    extension = [
        Extension(
            "pygraphviz._graphviz",
            ["pygraphviz/graphviz_wrap.c"],
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

    setup(
        name=name,
        version=version,
        author=authors["Hagberg"][0],
        author_email=authors["Hagberg"][1],
        description=description,
        keywords=keywords,
        long_description=long_description,
        license=license,
        platforms=platforms,
        url=url,
        download_url=download_url,
        classifiers=classifiers,
        packages=packages,
        data_files=data,
        ext_modules=extension,
        package_data=package_data,
        include_package_data=True,
        python_requires=">=3.7",
        tests_require=["pytest"],
    )
