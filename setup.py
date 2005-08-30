#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for pygraphviz.

"""
import os
import sys

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

import distutils
from distutils.command import build
from distutils.core import setup, Extension

if sys.argv[-1] == 'setup.py':
    print "To install, run 'python setup.py install'"
    print

# get library and include prefix
# TODO: the following might not be too portable
fp=os.popen('dotneato-config --prefix ','r')
lib_prefix=fp.readline()[:-1]
if fp.close():   # returns exit status
    print "Warning: dotneato-config not in path!"
    print "   If you are using a non-unix system, "
    print "   you will probably need to manually change"
    print "   the include_dirs and library_dirs in setup.py"
    print "   to point to the correct locations of your graphviz installation."
    lib_prefix="/usr"

# set includes and libs by hand if this isn't right for your platform
includes=lib_prefix+os.sep+'include'+os.sep+'graphviz'
libs=lib_prefix+os.sep+'lib'+os.sep+'graphviz'

# sanity check
try:
    agraphpath=includes+os.sep+'agraph.h'
    fh=open(agraphpath,'r')    
except:
    print "agraph.h include file not found at %s"%agraphpath
    print "incomplete graphviz installation (graphviz-dev missing?)"
    raise

long_description = """\
pygraphviz is a Python wrapper for the graphviz Agraph data structure.
See http://graphviz.org/
"""

class my_build(build.build):
    """ Just change the order of build_py and build_ext """
    sub_commands = [('build_clib',    build.build.has_c_libraries),
                    ('build_ext',     build.build.has_ext_modules),
                    ('build_scripts', build.build.has_scripts),
                    ('build_py',      build.build.has_pure_modules),
                   ]

setup(name = "pygraphviz",
      version = "0.1",
      author="Aric Hagberg, Dan Schult, Manos Renieris",
      author_email="hagberg@lanl.gov",
      license="GPL",
      description="A python interface to graphviz",
      long_description=long_description,
      url="http://networkx.sourceforge.net/",
      cmdclass={'build':my_build},
      ext_modules = [
      Extension("pygraphviz._graphviz",
                ["graphviz.i"],
                include_dirs=[includes],
                library_dirs=[libs],
                libraries=["agraph","cdt"],
                )
      ],
      package_dir = {"pygraphviz" : ""},
      packages = ["pygraphviz"],

      )
