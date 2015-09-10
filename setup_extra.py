#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup helpers for PyGraphviz.
"""
#    Copyright (C) 2006-2015 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

from __future__ import print_function
from __future__ import absolute_import
import subprocess as S
import sys
import os


def _b2str(buffer):
    result = u''
    if sys.version_info >= (3, 0):
        encoding = sys.getfilesystemencoding()
        if not encoding:
            # can be run without stdout
            if sys.stdout and sys.stdout.encoding:
                # encoding is not None only staring Python 3.2
                encoding = sys.stdout.encoding
            else:
                # fall back to default encoding ( normally it should not happen)
                encoding = 'utf8'
        if buffer:
            result = buffer.decode(encoding)
        return result
    else:
        # in Python 2 conversion is implicit
        return buffer


def _dpkg_config():
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz
    include_dirs=None
    library_dirs=None
    
    try:
        output = S.check_output(['dpkg', '-S', 'graphviz'])
        output = _b2str(output)
        lines = output.split('\n')
        for line in lines:
            if not include_dirs and line.endswith('.h'):
                include_dirs = os.path.dirname(line.split(':')[1].strip())
                include_dirs = include_dirs.strip() or None
            if not library_dirs and line.endswith('.so'):
                library_dirs = os.path.dirname(line.split(':')[1].strip())
                library_dirs = library_dirs.strip() or None
            if include_dirs and library_dirs:
                break
    except OSError:
        print("Failed to find dpkg")
    return include_dirs, library_dirs


def _pkg_config():
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz
    include_path=None
    library_path=None
    try:
        output = S.check_output(['pkg-config', '--libs-only-L', 'libcgraph'])
        output = _b2str(output)
        if output:
            library_path = output.strip()[2:]
            library_path = library_path.strip() or None
        output = S.check_output(['pkg-config', '--cflags-only-I', 'libcgraph'])
        output = _b2str(output)
        if output:
            include_path = output.strip()[2:]
            include_path = include_path.strip() or None
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
            library_path = library_path.strip()[2:].strip() or None
            include_path = include_path.strip()[2:].strip() or None
    except OSError:
        print("Failed to find dotneato-config")
        # fall through and test the other syntax
    if not include_path or not library_path:
        try:
            output = S.check_output(['dotneato-config', '--libs', '--cflags'])
            output = _b2str(output)
            if output:
                include_path, library_path = output.split('\n',1)
                library_path = library_path or library_path.strip()[2:].strip() or None
                include_path = include_path or include_path.strip()[2:].strip() or None
        except OSError:
            print("Failed to find dotneato-config")

    return include_path, library_path

def _try_configure(include_dirs, library_dirs, try_function):
    i, l = try_function()
    i = include_dirs or i
    l = library_dirs or l
    return i, l


def get_graphviz_dirs():
    """
    First try to read include_dirs from
    :return: tuple of lists ([include_dirs], [library_dirs])
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
        if library_dirs is None or include_dirs is None:
            print("Trying dpkg")
            include_dirs, library_dirs = _try_configure(include_dirs, library_dirs, _dpkg_config)

        if library_dirs is None or include_dirs is None:
            print("Trying pkg-config")
            include_dirs, library_dirs = _try_configure(include_dirs, library_dirs, _pkg_config)

        if library_dirs is None or include_dirs is None:
            print("Trying dotneato-config")
            include_dirs, library_dirs = _try_configure(include_dirs, library_dirs, _dotneato_config)

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
        provide path to graphviz include and library. For example:

        pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"

        The current setting of library_dirs and include_dirs is:""")
            print("library_dirs=%s"%library_dirs)
            print("include_dirs=%s"%include_dirs)
            print()
            raise OSError("Error locating graphviz.")

    print("include_dirs=%s" % include_dirs)
    print("library_dirs=%s" % library_dirs)


    return include_dirs, library_dirs

