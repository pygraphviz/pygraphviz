# -*- coding: utf-8 -*-
"""Release data for pygraphviz."""

#    Copyright (C) 2006-2008 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.


import os
import re


def get_svn_revision():
    rev = None
    path ="."
    entries_path = '%s/.svn/entries' % path
    if os.path.exists(entries_path):
        entries = open(entries_path, 'r').read()
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match('(\d+)', entries):
            rev_match = re.search('\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
    if rev:
        return 'dev%s' % rev
    return None

name = 'pygraphviz'
version = '1.0'
revision = get_svn_revision()
if revision is not None:
    version+=".%s"%revision

description = "Python interface to Graphviz"
long_description = """\
A Python wrapper for the Graphviz Agraph data structure.

pygraphviz can be used to create and draw networks and graphs with Graphviz.

"""
license = 'BSD'

authors = {'Hagberg' : ('Aric Hagberg','hagberg@lanl.gov'),
           'Schult' : ('Dan Schult','dschult@colgate.edu'),
           'Renieris' : ('Manos Renieris','')
           }
url = 'http://networkx.lanl.gov/pygraphviz'
download_url="http://networkx.lanl.gov/wiki/download"
platforms = ['Linux','Mac OSX','Windows XP/2000/NT']
keywords = ['Networks', 'Graph Visualization', 'network', 'graph', 'graph drawing']
classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        ]

# Get date dynamically
import time
date = time.asctime()
del time

