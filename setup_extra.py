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
import os


def pkg_config():
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz
    try:
        import subprocess as S
    except ImportError:
        print """-- Missing subprocess package:
        Install subprocess from
        http://effbot.org/downloads/#subprocess
        or set the graphviz paths manually as described below."""

    library_path=None
    include_path=None
    try:
        output,err = \
                   S.Popen('pkg-config --libs-only-L libcgraph',
                           shell=True, stdin=S.PIPE, stdout=S.PIPE,
                           close_fds=True).communicate()
        if output:
            library_path=output.strip()[2:]
        output,err = \
                   S.Popen('pkg-config --cflags-only-I libcgraph',
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
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz
    try:
        import subprocess as S
    except ImportError:
        print """-- Missing subprocess package:
        Install subprocess from
        http://effbot.org/downloads/#subprocess
        or set the graphviz paths manually as described below."""
    library_path=None
    include_path=None
    try:
        output = S.Popen(['dotneato-config','--ldflags','--cflags'],
                         stdout=S.PIPE).communicate()[0]
        if output:
            include_path,library_path=output.split()
            library_path=library_path.strip()[2:]
            include_path=include_path.strip()[2:]
        else:
            output = S.Popen(['dotneato-config','--libs','--cflags'],
                         stdout=S.PIPE).communicate()[0]
            if output:
                include_path,library_path=output.split('\n',1)
                library_path=library_path.strip()[2:]
                include_path=include_path.strip()[2:]
    except:
        print "Failed to find dotneato-config"
    return include_path,library_path


