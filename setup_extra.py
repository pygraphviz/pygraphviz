#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup helpers for PyGraphviz.
"""
#    Copyright (C) 2006-2010 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

from __future__ import print_function
from __future__ import absolute_import
import subprocess as S
import sys


def _b2str(buffer):
    result = u''
    if sys.version_info >= (3, 0):
        encoding = sys.getfilesystemencoding()
        if not encoding:
            # can be run without stdout
            if sys.stdout and sys.stdout.encoding:
                # encoding is nont None only staring Python 3.2
                encoding = sys.stdout.encoding
            else:
                # fall back to default encoding ( normally it should not happen)
                encoding = 'utf8'
        if buffer:
            result = buffer.decode(encoding)
        return result
    else:
        return buffer


def _pkg_config():
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz
    library_path=None
    include_path=None
    try:
        output = S.check_output(['pkg-config', '--libs-only-L', 'libcgraph'])
        output = _b2str(output)
        if output:
            library_path=output.strip()[2:]
        output = S.check_output(['pkg-config', '--cflags-only-I', 'libcgraph'])
        output = _b2str(output)
        if output:
            include_path=output.strip()[2:]
    except OSError:
        print("Failed to find pkg-config")
    return include_path, library_path

def _dotneato_config():
    # find graphviz configuration with dotneato-config
    # works with older versions of graphviz
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz
    library_path=None
    include_path=None
    try:
        output = S.check_output(['dotneato-config', '--ldflags', '--cflags'])
        output = _b2str(output)
        if output:
            include_path, library_path = output.split()
            library_path = library_path.strip()[2:]
            include_path = include_path.strip()[2:]
    except OSError:
        print("Failed to find dotneato-config")
        # fall through and test the other syntax
    if not include_path and not library_path:
        try:
            output = S.check_output(['dotneato-config', '--libs', '--cflags'])
            output = _b2str(output)
            if output:
                include_path, library_path = output.split('\n',1)
                library_path = library_path.strip()[2:]
                include_path = include_path.strip()[2:]
        except OSError:
            print("Failed to find dotneato-config")

    return include_path, library_path

def get_graphviz_dirs():
    """
    First try to read include_dirs from
    :return: tuple of lists ([include_dirs], [library_dirs], [define_macros])
    """

    # If the setup script couldn't find your graphviz installation you can
    # specify it here by uncommenting these lines or providing your own:
    # You must set both 'library_dirs' and 'include_dirs'

    # Linux, generic UNIX
    #library_dirs='/usr/lib/graphviz'
    #include_dirs='/usr/include/graphviz'

    # OSX, Linux, alternate location
    #library_dirs='/usr/local/lib/graphviz'
    #include_dirs='/usr/local/include/graphviz'

    # OSX (Fink)
    #library_dirs='/sw/lib/graphviz'
    #include_dirs='/sw/include/graphviz'

    # OSX (MacPorts)
    #library_dirs='/opt/local/lib/graphviz'
    #include_dirs='/opt/local/include/graphviz'

    # Windows
    # Unknown - use command line -I and -L switches to set
    include_dirs = None
    library_dirs = None

    if sys.platform != "win32":
        # Attempt to find Graphviz installation
        if library_dirs is None and include_dirs is None:
            print("Trying pkg-config")
            include_dirs, library_dirs = _pkg_config()

        if library_dirs is None and include_dirs is None:
            print("Trying dotneato-config")
            include_dirs, library_dirs = _dotneato_config()

        if library_dirs is None or include_dirs is None:
            print()
            print("""Your Graphviz installation could not be found.

        1) You don't have Graphviz installed:
           Install Graphviz (http://graphviz.org)

        2) Your Graphviz package might incomplete.
           Install the binary development subpackage (e.g. libgraphviz-dev or similar.)

        3) You are using Windows
           There are no PyGraphviz binary packages for Windows but you might be
           able to build it from this source.  See
           http://networkx.lanl.gov/pygraphviz/reference/faq.html

        If you think your installation is correct you will need to manually
        change the include_dirs and library_dirs variables in setup.py to
        point to the correct locations of your graphviz installation.

        The current setting of library_dirs and include_dirs is:""")
            print("library_dirs=%s"%library_dirs)
            print("include_dirs=%s"%include_dirs)
            print()
            raise OSError("Error locating graphviz.")

    print("include_dirs=%s" % include_dirs)
    print("library_dirs=%s" % library_dirs)


    return include_dirs, library_dirs

