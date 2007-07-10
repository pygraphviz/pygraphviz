#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for pygraphviz.
"""
#    Copyright (C) 2006,2007 by 
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

library_path=None
include_path=None


# If the setup script couldn't find your graphviz installation you can
# specify it here by uncommenting these lines or providing your own:
# You must set both 'library_path' and 'include_path'

# UNIX, Linux
#library_path='/usr/lib/graphviz'
#include_path='/usr/include/graphviz'

# UNIX, Linux alternate
#library_path='/usr/local/lib/graphviz'
#include_path='/usr/local/include/graphviz'

# Mac OS X (Fink)
#library_path='/sw/lib/graphviz'
#include_path='/sw/include/graphviz'

# Mac OS X (MacPorts)
#library_path='/opt/local/lib/graphviz'
#include_path='/opt/local/include/graphviz'


def pkg_config():
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz
    library_path=None
    include_path=None
    try:
        output,err = \
                   S.Popen('pkg-config --libs-only-L libagraph',
                           shell=True, stdin=S.PIPE, stdout=S.PIPE,
                           close_fds=True).communicate()
        if output:
            library_path=output.strip()[2:]
        output,err = \
                   S.Popen('pkg-config --cflags-only-I libagraph',
                           shell=True, stdin=S.PIPE, stdout=S.PIPE,
                           close_fds=True).communicate()
        if output:
            include_path=output.strip()[2:]
    except:
        print "Failed to find pkg-config"
    return include_path,library_path

def dotneato_config():
    # find graphviz configuration with dotneato-config
    # works with older versions of graphviz
    library_path=None
    include_path=None
    try:
        output = S.Popen(['dotneato-config','--ldflags','--cflags'],
                         stdout=S.PIPE).communicate()[0]
        if output:
            include_path,library_path=output.split()
            library_path=library_path.strip()[2:]
            include_path=include_path.strip()[2:]
    except:
        print "Failed to find dotneato-config"
    return include_path,library_path



if library_path is None and include_path is None:
    try:
        import subprocess as S
    except ImportError:
        print """-- Missing subprocess package:
        Install subprocess from
        http://effbot.org/downloads/#subprocess
        or set the graphviz paths manually as described below."""

if library_path is None and include_path is None:
    print "Trying pkg-config"
    include_path,library_path=pkg_config()

if library_path is None and include_path is None:
    print "Trying dotneato-config"
    include_path,library_path=dotneato_config()

if library_path is None or include_path is None:
    print 
    print  """Your graphviz installation could not be found.

Either the graphviz package is missing on incomplete (graphviz-dev missing?).  

If you think your installation is correct you will need to manually
change the include_path and library_path variables in setup.py to
point to the correct locations of your graphviz installation.

The current setting of library_path and include_path is:"""
    print "library_path=%s"%library_path
    print "include_path=%s"%include_path
    print
    raise OSError,"Error locating graphviz."

print "library_path=%s"%library_path
print "include_path=%s"%include_path

if len(library_path)>0:
    library_dirs=[library_path]
else:
    library_dirs=None

if len(include_path)>0:
    include_dirs=[include_path]
else:
    include_dirs=None

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
                      include_dirs=include_dirs,
                      library_dirs=library_dirs,
                      runtime_library_dirs=library_dirs,
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

