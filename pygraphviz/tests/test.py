#!/usr/bin/env python

import sys
import doctest
import unittest

if sys.version_info[:2] < (2, 4):
    print "Python version 2.4 or later required for tests (%d.%d detected)." %  sys.version_info[:2]
    sys.exit(-1)
try:
    import pygraphviz
except:
    print "Can't import pygraphviz module, not in path"
    print sys.path
    raise
    
suite = unittest.TestSuite()
s = doctest.DocFileSuite('pygraphviz_test.txt',module_relative=False)
suite.addTest(s)
runner = unittest.TextTestRunner()
runner.run(suite)
