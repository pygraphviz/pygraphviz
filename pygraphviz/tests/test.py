#!/usr/bin/env python

import sys
import doctest
import unittest
import glob
import os

def test_suite():
    test_files=['graph.txt','layout_draw.txt','attributes.txt','unicode.txt']
    try: # has setuptools
        from pkg_resources import resource_filename
        tests=[resource_filename(__name__, t) for t in test_files]
    except: # no setuptools
        import pygraphviz
        base=os.path.dirname(pygraphviz.__file__)
        tests=glob.glob(base+"/tests/"+"*.txt") 

    suite = unittest.TestSuite()
    for t in tests:
        s = doctest.DocFileSuite(t,module_relative=False)
        suite.addTest(s)
    return suite


def run():
    if sys.version_info[:2] < (2, 4):
        print "Python version 2.4 or later required for tests (%d.%d detected)." %  sys.version_info[:2]
        sys.exit(-1)
    runner = unittest.TextTestRunner()
    runner.run(test_suite())


if __name__ == "__main__":
    if sys.version_info[:2] < (2, 4):
        print "Python version 2.4 or later required for tests (%d.%d detected)." %  sys.version_info[:2]
        sys.exit(-1)
    try:
        import pygraphviz
    except:
        print "Can't import pygraphviz module, not in path"
        print sys.path
        raise
    
    run()

