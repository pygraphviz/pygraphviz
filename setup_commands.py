#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup commands for PyGraphviz.
"""
#    Copyright (C) 2006-2014 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.
#    All rights reserved, see LICENSE for details.
#
#   Derived from http://www.niteoweb.com/blog/setuptools-run-custom-code-during-install
#   Author: Maksym Markov <maksym.markov@gmail.com>

from setuptools.command.develop import develop
from setuptools.command.install import install

from setup_extra import get_graphviz_dirs

def add_extensions(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that it prints a friendly greeting.
    """
    orig_init = command_subclass.__init__
    orig_initialize_options = command_subclass.initialize_options
    orig_run = command_subclass.run
    command_subclass.user_options.extend([('include-path=', None, 'path to graphviz include files.'),
                                          ('library-path=', None, 'path to graphviz library files.')])

    def __init__(self, *args, **kws):
        orig_init(self, *args, **kws)

    def modified_initialize_options(self):
        self.include_path = None
        self.library_path = None
        orig_initialize_options(self)

    def modified_run(self):
        # Add extension here
        # if there is no library_path and include_path passed form command line then try identify them
        if (not self.include_path) or (not self.library_path):
            self.include_path, self.library_path = get_graphviz_dirs()
        if self.distribution and self.distribution.ext_modules:
            for m in self.distribution.ext_modules:
                if m.name == 'pygraphviz._graphviz':
                    if self.include_path:
                        m.include_dirs.append(self.include_path)
                    if self.library_path:
                        m.library_dirs.append(self.library_path)
        orig_run(self)

    command_subclass.__init__ = __init__
    command_subclass.initialize_options = modified_initialize_options
    command_subclass.run = modified_run

    return command_subclass


@add_extensions
class AddExtensionDevelopCommand(develop):
    pass

@add_extensions
class AddExtensionInstallCommand(install):
    pass
