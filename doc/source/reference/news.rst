..  -*- coding: utf-8 -*-

News
==== 
pygraphviz-1.3.1
----------------
Release date: 6 September 2015

 - Update manifest to include missing files



pygraphviz-1.3
--------------
Release date: 5 September 2015

 - Python 3 support
 - Encoding bugfixes

https://github.com/pygraphviz/pygraphviz/issues?q=milestone%3Apygraphivz-1.3+is%3Aclosed


pygraphviz-1.2
-----------------
Release date: 3 August 2013

 - Quote Graphviz program names to work with space (Windows fix)
 - Keep name in reverse()

pygraphviz-1.1
-----------------
Release date: 9 February 2011

 - Added unicode support for handling non-ASCII characters
 - Better handling of user data on initialization of AGraph() object
   to guess input type (AGraph object, file, dict-of-dicts, file)
 - Add sfdp to layout options

See https://networkx.lanl.gov/trac/query?group=status&milestone=pygraphviz-1.1

pygraphviz-1.0.0
-----------------
Release date: 30 July 2010

See: https://networkx.lanl.gov/trac/timeline

 - Added to_string() and from_string methods
 - Interface to graphviz "acyclic" and "tred"
 - Better handling of user data on initialization of AGraph() object
   to guess input type (AGraph object, file, dict-of-dicts, file)
 - Add handling of default attributes for subgraphs
 - Improved error handling when using non-string data
 - Fix bug in default attribute handling
 - Make sure file handles are closed correctly


pygraphviz-0.99.1
-----------------
Release date: 7 December 2008

See: https://networkx.lanl.gov/trac/timeline

 - Use Graphviz libcgraph instead of deprecated libagraph
 - More closely match API to NetworkX 
 - edges() now produces two-tuples or three tuples if edges(keys=True)
 - Edge and Node objects now have .name and .handle properties
 - Warn without throwing exceptions for Graphviz errors
 - Graph now has .strict and .directed properties
 - Cleared up fontsize warnings in examples 


pygraphviz-0.99
---------------
Release date: 18 November 2008

See: https://networkx.lanl.gov/trac/timeline

 - New documentation at http://networkx.lanl.gov/pygraphviz/
 - Developer's site at https://networkx.lanl.gov/trac/wiki/PyGraphviz

pygraphviz-0.37
---------------
Release date: 17 August 2008

See: https://networkx.lanl.gov/trac/timeline

 - Handle default attributes for subgraphs, examples at
   https://networkx.lanl.gov/trac/browser/pygraphviz/trunk/doc/examples/attributes.py
   https://networkx.lanl.gov/trac/browser/pygraphviz/trunk/doc/examples/subgraph.py
 - Buggy attribute assignment fixed by Graphviz team (use Graphviz>2.17.20080127)
 - Encode all stings as UTF-8 as default
 - Fix AGraph.clear() memory leak and attempt to address slow deletion 
   of nodes and edges 
 - Allow pdf output and support all available output types on a given platform
 - Fix number_of_edges() to use gv.agnedges to correctly report edges for
   graphs with self loops

pygraphviz-0.36
---------------
Release date: 13 January 2008

See: https://networkx.lanl.gov/trac/timeline

 - Automatic handling of types on init of AGraph(data): data can be
   a filename, string in dot format, dictionary-of-dictionaries,
   or a SWIG AGraph pointer.
 - Add interface to Graphviz programs acyclic and tred
 - Refactor process handling to allow easier access to Graphviz layout
   and graph processing programs
 - to_string() and from_string() methods 
 - Handle multiple anonymous edges correctly
 - Attribute handling on add_node, add_edge and init of AGraph.
   So you can e.g. A=AGraph(ranksep='0.1'); A.add_node('a',color='red')
   A.add_edge('a','b',color='blue')


pygraphviz-0.35
---------------
Release date: 22 July 2007

See: https://networkx.lanl.gov/trac/timeline

 - Rebuilt SWIG wrappers - works correctly now on 64 bit machines/python2.5
 - Implement Graphviz subgraph functionality
 - Better error reporting when attempting to set attributes, avoid 
   segfault when using None 
 - pkg-config handling now works in more configurations (hopefully all) 
 

pygraphviz-0.34
---------------
Release date: 11 April 2007

See: https://networkx.lanl.gov/trac/timeline

 - run "python setup_egg.py test" for tests if you have setuptools
 - added tests for layout code
 - use pkg-config for finding graphviz (dotneato-config still works
   for older graphviz versions)
 - use threads and temporary files for multiplatform nonblocking IO
 - django example

pygraphviz-0.33
---------------
  - Workaround for "nop" bug in graphviz-2.8, improved packaging,
    updated swig wrapper, better error handling.

pygraphviz-0.32
---------------

   The release pygraphviz-0.32 is the second rewrite of the original project.
   It has improved attribute handling and drawing capabilities.
   It is not backward compatible with earlier versions.
   Earlier versions will always be available at the download site.

   This version now inter-operates with many of the NetworkX
   algorithms and graph generators.  See 
   https://networkx.lanl.gov/trac/browser/networkx/trunk/doc/examples/pygraphviz_simple.py
