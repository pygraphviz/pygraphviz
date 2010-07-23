#!/usr/bin/env python
"""
An alternate setup.py script for setuptools.

If you have setuptools and run this as 

>>> python setup_egg.py bdist_egg

you will get a python egg.

Use

>>> python setup_egg.py test

to run the tests.


"""
# local import, might need modification for 2.6/3.0
from setup import *

# must occur after local import to override distutils.core.setup
from setuptools import setup, Extension


extension = [Extension("pygraphviz._graphviz",
                      ["pygraphviz/graphviz_wrap.c"],
                      include_dirs=include_dirs,
                      library_dirs=library_dirs,
                      runtime_library_dirs=library_dirs,
                      libraries=["cgraph","cdt"])]

if __name__ == "__main__":

    setup(
        name             = release.name,
        version          = release.version,
        author           = release.authors['Hagberg'][0],
        author_email     = release.authors['Hagberg'][1],
        description      = release.description,
        keywords         = release.keywords,
        long_description = release.long_description,
        license          = release.license,
        platforms        = release.platforms,
        url              = release.url,      
        download_url     = release.download_url,
        classifiers      = release.classifiers,
        packages         = packages,
        data_files       = data,
        ext_modules      = extension,
        package_data     = package_data,
        install_requires=['setuptools'],
        include_package_data = True,
        test_suite       = "pygraphviz.tests.test.test_suite", 
        )

