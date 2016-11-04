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
from setuptools import setup, Extension
import sys

from setup_commands import AddExtensionDevelopCommand, AddExtensionInstallCommand
from setup_extra import get_graphviz_dirs


if os.path.exists('MANIFEST'): os.remove('MANIFEST')

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 6):
    print("PyGraphviz requires Python version 2.6 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

# Write the version information.
#TODO rework this import hack with import graphviz.release or import graphviz.version ( doesn't work now because of code in the __init__)
sys.path.insert(0, 'pygraphviz')
import release
release.write_versionfile()
sys.path.pop(0)

packages = ["pygraphviz", "pygraphviz.tests"]
docdirbase = 'share/doc/pygraphviz-%s' % release.version
data = [
    (docdirbase, glob("*.txt")),
    (os.path.join(docdirbase, 'examples'), glob("examples/*.py")),
    (os.path.join(docdirbase, 'examples'), glob("examples/*.dat")),
    (os.path.join(docdirbase, 'examples'), glob("examples/*.dat.gz")),
]
package_data = {'': ['*.txt'], }

if __name__ == "__main__":
    define_macros = []
    if sys.platform == "win32":
        define_macros = define_macros.append(('GVDLL', None))

    extension = [
        Extension(
            "pygraphviz._graphviz",
            ["pygraphviz/graphviz_wrap.c"],
            include_dirs=[],
            library_dirs=[],
            # cdt does not link to cgraph, whereas cgraph links to cdt.
            # thus, cdt needs to come first in the library list to be sure
            # that both libraries are linked in the final built .so (if cgraph
            # is first, the implicit inclusion of cdt can lead to an incomplete
            # link list, having only cdt and preventing the module from being loaded with
            # undefined symbol errors. seen under PyPy on Linux.)
            libraries=["cdt", "cgraph"],
            define_macros=define_macros
        )
    ]

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
        ext_modules=extension,
        cmdclass={
            'install': AddExtensionInstallCommand,
            'develop': AddExtensionDevelopCommand,
            },
        package_data=package_data,
        include_package_data = True,
        test_suite='nose.collector',
        tests_require=['nose>=0.10.1', 'doctest-ignore-unicode>=0.1.0', 'mock>=1.3'],
    )
