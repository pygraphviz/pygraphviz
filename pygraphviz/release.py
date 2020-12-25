"""Release data for PyGraphviz."""

import os
import re


def write_versionfile():
    """Creates a file containing version information."""
    base = os.path.split(__file__)[0]
    versionfile = os.path.join(base, "version.py")
    if os.path.isfile(versionfile):
        # If a version.py already exists, let's not overwrite it.
        return
    fh = open(versionfile, "w")
    text = '''"""
Version information for PyGraphviz, created during installation.

Do not add this file to the repository.

"""

__version__ = '%(version)s'
__date__ = '%(date)s'

'''
    subs = {"version": version, "date": date}
    fh.write(text % subs)
    fh.close()


name = "pygraphviz"
version = "1.7"

# Declare current release as a development release.
# Change to False before tagging a release; then change back.
dev = True

description = "Python interface to Graphviz"
long_description = """\
PyGraphviz is a Python interface to the Graphviz graph layout and visualization package. With PyGraphviz you can create, edit, read, write, and draw graphs using Python to access the Graphviz graph data structure and layout algorithms. PyGraphviz provides a similar programming interface to NetworkX (https://networkx.org). 
"""
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

# Get date dynamically
import time

date = time.asctime()
del time
