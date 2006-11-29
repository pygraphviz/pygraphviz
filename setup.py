#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for pygraphviz.
"""
#    Copyright (C) 2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

from glob import glob
import os
import sys
if os.path.exists('MANIFEST'): os.remove('MANIFEST')
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
    print "Warning: dotneato-config not in path."
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


execfile(os.path.join('pygraphviz','release.py'))

packages = ["pygraphviz","pygraphviz.tests"]
docdirbase  = 'share/doc/pygraphviz-%s' % version
data = [(docdirbase, glob("doc/*.txt")),
        (docdirbase, glob("doc/*.py")),
        (os.path.join(docdirbase, 'examples'),glob("doc/examples/*.py")),
        (os.path.join(docdirbase, 'examples'),glob("doc/examples/*.dat")),
        ]
extension = [Extension("pygraphviz._graphviz",
                      ["pygraphviz/graphviz_wrap.c"],
                      include_dirs=[includes],
                      library_dirs=[libs],
                      libraries=["agraph","cdt"],
                      )]
package_data = {'': ['*.txt'],}

if __name__ == "__main__":

    setup(
      name             = name,
      version          = version,
      author           = authors['Hagberg'][0],
      author_email     = authors['Hagberg'][1],
      description      = description,
      keywords         = keywords,
      long_description = long_description,
      license          = license,
      platforms        = platforms,
      url              = url,      
      download_url     = download_url,
      packages         = packages,
      data_files       = data,
      classifiers      = classifiers,
      ext_modules      = extension,
      package_data     = package_data,
      )

