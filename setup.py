#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for PyGraphviz
"""
#    Copyright (C) 2006-2009 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

from glob import glob
import os
import sys
if os.path.exists('MANIFEST'): os.remove('MANIFEST')
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
from setup_extra import pkg_config, dotneato_config, write_versionfile

if sys.argv[-1] == 'setup.py':
    print "To install, run 'python setup.py install'"
    print

if sys.version_info[:2] < (2, 4):
    print "PyGraphviz requires Python version 2.4 or later (%d.%d detected)." % \
          sys.version_info[:2]
    sys.exit(-1)

library_path=None
include_path=None

# If the setup script couldn't find your graphviz installation you can
# specify it here by uncommenting these lines or providing your own:
# You must set both 'library_path' and 'include_path'

# Linux, generic UNIX
#library_path='/usr/lib/graphviz'
#include_path='/usr/include/graphviz'

# OSX, Linux, alternate location
#library_path='/usr/local/lib/graphviz'
#include_path='/usr/local/include/graphviz'

# OSX (Fink)
#library_path='/sw/lib/graphviz'
#include_path='/sw/include/graphviz'

# OSX (MacPorts)
#library_path='/opt/local/lib/graphviz'
#include_path='/opt/local/include/graphviz'

# Attempt to find Graphviz installation
if library_path is None and include_path is None:
    print "Trying pkg-config"
    include_path,library_path=pkg_config()

if library_path is None and include_path is None:
    print "Trying dotneato-config"
    include_path,library_path=dotneato_config()

if library_path is None or include_path is None:
    print 
    print  """Your graphviz installation could not be found.

Either the graphviz package is missing on incomplete
(binary packages graphviz-dev or graphviz-devel missing?).  

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
write_versionfile(version,revision,date)


packages = ["pygraphviz","pygraphviz.tests"]
docdirbase  = 'share/doc/pygraphviz-%s' % version
data = [(docdirbase, glob("*.txt")),
        (os.path.join(docdirbase, 'examples'),glob("examples/*.py")),
        (os.path.join(docdirbase, 'examples'),glob("examples/*.dat")),
        (os.path.join(docdirbase, 'examples'),glob("examples/*.dat.gz")),
        ]
extension = [Extension("pygraphviz._graphviz",
                      ["pygraphviz/graphviz_wrap.c"],
                      include_dirs=include_dirs,
                      library_dirs=library_dirs,
                      runtime_library_dirs=library_dirs,
                      libraries=["cgraph","cdt"],
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

