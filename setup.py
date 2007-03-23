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


libs=None
includes=None

# If the setup script couldn't find your graphviz installation you can
# specify it here by ucommenting these lines or providing your own:
# You must set both 'libs' and 'includes'

#libs='/packages/lib/graphviz'
#includes='/packages/include/graphviz'

# UNIX,Linux
#libs='/usr/lib/graphviz'
#includes='/usr/include/graphviz'

# UNIX,Linux alternate
#libs='/usr/local/lib/graphviz'
#includes='/usr/local/include/graphviz'

# OSX,fink
#libs='/sw/lib/graphviz'
#includes='/sw/include/graphviz'

# OSX,darwin-ports?
#libs='/opt/local/graphviz'
#includes='/opt/local/include/graphviz'

if libs is None:
    try:
        import subprocess as S
        output,err = \
        S.Popen('pkg-config --libs-only-L --cflags-only-I libagraph',
                shell=True, stdin=S.PIPE, stdout=S.PIPE,
                close_fds=True).communicate()
        if output:
            includes,libs=output.split()
            libs=libs.strip()[2:]
            includes=includes.strip()[2:]
    except ImportError:
        print """-- Missing subprocess package:
        Install subprocess from
        http://effbot.org/downloads/#subprocess
        or set the graphviz paths manually as described below."""
    if libs is None or libs=='':
        print "-- Failed to find pkg-config for libagraph"
        print "   Trying dotneato-config"
        try:
            output = S.Popen(['dotneato-config','--ldflags','--cflags'],
                             stdout=S.PIPE).communicate()[0]
            if output:
                includes,libs=output.split()
                libs=libs.strip()[2:]
                includes=includes.strip()[2:]
        except:
            print "-- Failed to find dotneato-config"


if libs is None or libs=='':
    libs="/usr/lib/graphviz" # make a guess anyway
    includes="/usr/includes/graphviz" # make a guess anyway

# sanity check
try:
    agraphpath=includes+os.sep+'agraph.h'
    fh=open(agraphpath,'r')    
except:
    print "-- Error: agraph.h include file not found at %s"%agraphpath
    print "   Incomplete graphviz installation (graphviz-dev missing?)"
    print
    print  """Your graphviz installation couldn't be found.
If you think your installation is correct you will 
need to manually change the includes and libs variables in setup.py
to point to the correct locations of your graphviz installation.

The current settings of libs and includes is:"""
    print "libs=%s"%libs
    print "includes=%s"%includes
    print
    raise "Error locating graphviz."


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

