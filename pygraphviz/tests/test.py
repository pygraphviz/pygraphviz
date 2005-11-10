#!/usr/bin/env python

import sys
import doctest
import unittest

def test_suite():
    from pkg_resources import resource_filename
    suite = unittest.TestSuite()
    doctst = resource_filename(__name__, 'pygraphviz_test.txt')
    s = doctest.DocFileSuite(doctst,module_relative=False)
    suite.addTest(s)
    return suite

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
    
    runner = unittest.TextTestRunner()
    runner.run(test_suite())
