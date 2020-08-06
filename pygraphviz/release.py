"""Release data for PyGraphviz."""

#    Copyright (C) 2006-2018 by
#    Aric Hagberg <aric.hagberg@gmail.com>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.
#    All rights reserved, see LICENSE for details.


import os
import re


def write_versionfile():
    """Creates a file containing version information."""
    base = os.path.split(__file__)[0]
    versionfile = os.path.join(base, "version.py")
    if revision is None and os.path.isfile(versionfile):
        # Unable to get revision info, so probably not in an SVN directory
        # If a version.py already exists, let's not overwrite it.
        # Useful mostly for nightly tarballs.
        return
    fh = open(versionfile, "w")
    text = '''"""
Version information for PyGraphviz, created during installation.

Do not add this file to the repository.

"""

__version__ = '%(version)s'
__revision__ = %(revision)s
__date__ = '%(date)s'

'''
    if revision is not None:
        rev = f"'{revision}'"
    else:
        rev = revision
    subs = {"version": version, "revision": rev, "date": date}
    fh.write(text % subs)
    fh.close()


def get_svn_revision():
    rev = None
    base = os.path.split(__file__)[0]
    entries_path = os.path.join(base, ".svn", "entries")
    if os.path.isfile(entries_path):
        entries = open(entries_path).read()
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match(r"(\d+)", entries):
            rev_match = re.search(r"\d+\s+dir\s+(\d+)", entries)
            if rev_match:
                rev = rev_match.groups()[0]
    if rev:
        return rev
    else:
        return None


name = "pygraphviz"
version = "1.6"

# Declare current release as a development release.
# Change to False before tagging a release; then change back.
dev = False

revision = None
if dev:
    version += ".dev"
    revision = get_svn_revision()
    if revision is not None:
        version += "%s" % revision

description = "Python interface to Graphviz"
long_description = """\
PyGraphviz is a Python interface to the Graphviz graph layout and visualization package. With PyGraphviz you can create, edit, read, write, and draw graphs using Python to access the Graphviz graph data structure and layout algorithms. PyGraphviz provides a similar programming interface to NetworkX (http://networkx.github.io). 
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
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
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

if __name__ == "__main__":
    # Write versionfile for nightly snapshots.
    write_versionfile()
