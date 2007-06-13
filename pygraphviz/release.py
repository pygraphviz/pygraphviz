# -*- coding: utf-8 -*-
"""Release data for pygraphviz."""

#    Copyright (C) 2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.


name = 'pygraphviz'
version = '0.35_svn'
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

