..  -*- coding: utf-8 -*-

News
====

pygraphviz-1.12
---------------

Release date: TBD

  - Drop Python 3.8 (SPEC 0)

pygraphviz-1.11
---------------

Release date: 1 June 2023

  - Update to SWIG 4.1.1
  - Require Graphviz 2.46+
  - Fix passthrough of graph attributes when copying
  - Update install instructions

pygraphviz-1.10
---------------

Release date: 19 August 2022

  - Add Python 3.11 support
  - Fix gvRenderData bytes output
  - Fix FILE* resource leak in agread() wrapper
  - Close all references to fname before calling unlink(fname)

pygraphviz-1.9
--------------

Release date: 9 February 2022

  - Drop Python 3.7 support
  - Add Python 3.10 support
  - Add osage and patchwork to progs list
  - Add IPython rich display hook to AGraph class
  - Add contributor guide
  - Fixed directed nature of AGraph.copy()
  - Minor documentation and code fixes

pygraphviz-1.8
--------------

Release date: 20 January 2022

This release was pulled because the install was broken with pip 22 and python 3.7.

pygraphviz-1.7
--------------

Release date: 1 February 2021

  - Drop Python 3.6 support
  - Add Python 3.9 support
  - Require Graphviz 2.42+, (Graphviz 2.46+ recommended)
  - Improve installation process and documentation
  - Switch from nose to pytest
  - Remove old Python 2 code
  - AGraph.eq includes attribute comparison (PR #246)

pygraphviz-1.6
--------------

Release date: 05 September 2020

  - Add Python 3.8 support
  - Drop Python 2.7 support
  - Update to SWIG 4.0.1

pygraphviz-1.5
--------------

Release date: 10 September 2018

  - Python 3.7 support

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

  Pygraphviz-1.1 adds unicode (graphviz charset) support.
  The default Node type is now unicode.
  See examples/utf8.py for an example of how to use non-ASCII characters.

  The __str__ and  __repr__ methods have been rewritten and a __unicode__
  method added.

  If G is a pygraphviz.AGraph object then

  - str(G) produces a dot-format string representation
    (some characters might not be represented correctly)
  - unicode(G) produces a dot-format unicode representation
  - repr(G) produces a string of the unicode representation.
  - print G produces a formatted dot language output

pygraphviz-1.0.0
-----------------
Release date: 30 July 2010

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

pygraphviz-0.37
---------------
Release date: 17 August 2008

  - Handle default attributes for subgraphs
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

  - Rebuilt SWIG wrappers - works correctly now on 64 bit machines/python2.5
  - Implement Graphviz subgraph functionality
  - Better error reporting when attempting to set attributes, avoid
    segfault when using None
  - pkg-config handling now works in more configurations (hopefully all)


pygraphviz-0.34
---------------
Release date: 11 April 2007

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

   This version now inter-operates with many of the NetworkX
   algorithms and graph generators.

   pygraphviz-0.32 is a rewrite of pygraphviz-0.2x  with some significant
   changes in the API and Graphviz wrapper.  It is not compatible with
   with earlier versions.

   The goal of pygraphviz is to provide a (mostly) Pythonic interface
   to the Graphviz Agraph data-structure, layout, and drawing algorithms.

   The API is now similar to the NetworkX API.  Studying the
   documentation and Tutorial for NetworkX will teach you most of what
   you need to know for pygraphviz.  For a short introduction on pygraphviz
   see the pygraphviz Tutorial.

   There are some important differences between the PyGraphviz
   and NetworkX API.  With PyGraphviz

    - All nodes must be of string or unicode type.
      An attempt will be made to convert other types to a string.

    - Nodes and edges are custom Python objects.  Nodes are like
      unicode/string objects and edges are like tuple objects.  (In NetworkX
      nodes can be anything and edges are two- or three-tuples.)

    - Graphs, edges, and nodes may have attributes such as color,
      size, shape, attached to them.  If the attributes are known
      Graphviz attributes they will be used for drawing and layout.

    - The layout() and draw() methods allow positioning of nodes
      and rendering in all of the supported Graphviz output formats.

    - The string() method produces a string with the graph represented
      in Graphviz dot format.  See also from_string().

    - The subgraph() method is the Graphviz representation of
      subgraphs: a tree of graphs under the original
      (root) graph. The are primarily used for clustering of nodes when
      drawing with dot.

   Pygraphviz supports most of the Graphviz API.
