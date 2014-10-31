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
import os
import sys
import subprocess as S

def pkg_config():
    # attempt to find graphviz installation with pkg-config
    # should work with modern versions of graphviz

    library_path=None
    include_path=None
    try:
        output = S.check_output(['pkg-config', '--libs-only-L', 'libcgraph'])
        library_path = output.strip()[2:]

        output = S.check_output(['pkg-config', '--cflags-only-I',
            'libcgraph'])
        include_path = output.strip()[2:]
    except S.CalledProcessError:
        print("Failed to find pkg-config")

    return include_path, library_path

def dotneato_config():
    # find graphviz configuration with dotneato-config
    # works with older versions of graphviz

    library_path = None
    include_path = None
    try:
        output = S.check_output(['dotneato-config', '--ldflags', '--cflags'])
        include_path, library_path = output.split()
        library_path = library_path.strip()[2:]
        include_path = include_path.strip()[2:]
    except S.CalledProcessError:
        print("Failed to find dotneato-config")
        # fall through and test the other syntax
    else:
        return include_path, library_path

    try:
        output = S.check_output(['dotneato-config', '--libs', '--cflags'])
        include_path, library_path = output.split('\n', 1)
        library_path = library_path.strip()[2:]
        include_path = include_path.strip()[2:]
    except:
        print("Failed to find dotneato-config")

    # nothing else to try, just return
    return include_path, library_path

