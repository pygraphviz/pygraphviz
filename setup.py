#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for pygraphviz.

"""
from glob import glob
import os
import sys

from distutils.core import setup, Extension

if sys.argv[-1] == 'setup.py':
    print "To install, run 'python setup.py install'"
    print

# get library and include prefix, the following might not be too portable
fp=os.popen('dotneato-config --prefix ','r')
prefix=fp.readline()[:-1]

# If setting the prefix failed you should attempt to set the prefix here
# by ucommenting one of these lines or providing your own :
# prefix="/usr" # unix, Linux
# prefix="/usr/local" # unix, alternate
# prefix="/sw"  # OSX, fink
# prefix="/opt/local"  # OSX, darwin-ports? 

if not prefix:  
    print "Warning: dotneato-config not in path!"
    print "   If you are using a non-unix system, "
    print "   you will probably need to manually change"
    print "   the include_dirs and library_dirs in setup.py"
    print "   to point to the correct locations of your graphviz installation."
    prefix="/usr" # make a guess anyway

# set includes and libs by hand here if you have a very nonstandard
# installation of graphviz
includes=prefix+os.sep+'include'+os.sep+'graphviz'
libs=prefix+os.sep+'lib'+os.sep+'graphviz'

# sanity check
try:
    agraphpath=includes+os.sep+'agraph.h'
    fh=open(agraphpath,'r')    
except:
    print "agraph.h include file not found at %s"%agraphpath
    print "incomplete graphviz installation (graphviz-dev missing?)"
    raise

long_description = """\
A Python wrapper for the Graphviz Agraph data structure.

pygraphviz can be used to create and draw networks and graphs with Graphviz.

"""

version="0.23-svn"
docdirbase  = 'share/doc/pygraphviz-%s' % version
data = [(docdirbase, glob("doc/*.txt")),
        (os.path.join(docdirbase, 'examples'),glob("doc/examples/*.py")),
        (os.path.join(docdirbase, 'examples'),glob("doc/examples/*.dat")),
        (os.path.join(docdirbase, 'data'),glob("doc/data/*ls")),
        ]

setup(name = "pygraphviz",
      version = version,
      packages = ["pygraphviz","pygraphviz.tests"],
      ext_modules = [
      Extension("pygraphviz._graphviz",
                ["pygraphviz/graphviz_wrap.c"],
                include_dirs=[includes],
                library_dirs=[libs],
                libraries=["agraph","cdt"],
                )
      ],
      data_files = data,
      package_data = {
        '': ['*.txt'],
        },
      test_suite = "pygraphviz.tests.test.test_suite",
      author="Aric Hagberg, Dan Schult, Manos Renieris",
      author_email="hagberg@lanl.gov",
      license="BSD",
      description="Python interface to Graphviz",
      long_description=long_description,
      url="http://networkx.lanl.gov/pygraphviz/",
      download_url="http://sourceforge.net/project/showfiles.php?group_id=122233&package_id=161979",

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
      )

