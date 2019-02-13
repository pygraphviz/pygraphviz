#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for PyGraphviz
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from glob import glob

import os
import sys
from os.path import join
from os.path import relpath

def ensure_versionfile(repodir):
    """ Write the version information. """
    #TODO rework this import hack with import graphviz.release or import
    # graphviz.version ( doesn't work now because of code in the __init__)
    sys.path.insert(0, repodir)
    sys._in_pygraphviz_setup = True
    from pygraphviz import release
    release.write_versionfile()
    sys.path.pop(0)
    return release

repodir = os.path.dirname(__file__)

packages = ["pygraphviz", "pygraphviz.tests"]

def relglob(pattern):
    return [relpath(p, repodir) for p in glob(join(repodir, pattern))]


release = ensure_versionfile(repodir)
docdirbase = 'share/doc/pygraphviz-%s' % release.version
data = [
    (docdirbase, relglob("*.txt")),
    (join(docdirbase, 'examples'), relglob("examples/*.py")),
    (join(docdirbase, 'examples'), relglob("examples/*.dat")),
    (join(docdirbase, 'examples'), relglob("examples/*.dat.gz")),
]
package_data = {'pygraphviz': ['*.txt'], }

if __name__ == "__main__":
    print('data')
    print(data)

    # skbuild replaces 'from setuptools import setup'
    # extension and build_ext are no longer necessary, CMake handles it.
    from skbuild import setup

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(
        name=release.name,
        version=release.version,
        author=release.authors['Hagberg'][0],
        author_email=release.authors['Hagberg'][1],
        description=release.description,
        keywords=release.keywords,
        long_description=release.long_description,
        license=release.license,
        platforms=release.platforms,
        url=release.url,
        download_url=release.download_url,
        classifiers=release.classifiers,
        packages=packages,
        data_files=data,
        package_data=package_data,
        include_package_data=True,
        test_suite='nose.collector',
        tests_require=['nose>=1.3.7', 'doctest-ignore-unicode>=0.1.2', 'mock>=2.0.0'],
    )
