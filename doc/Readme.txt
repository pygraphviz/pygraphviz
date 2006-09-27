----------
Pygraphviz
----------

pygraphviz
----------

   Pygraphviz is a Python interface to the Graphviz graph layout and
   visualization package.

   With Pygraphviz you can create, edit, read, write, and draw graphs using
   Python to access the Graphviz graph data structure and layout algorithms.

   Upcoming release:

   pygraphviz-0.32 is the second rewrite of the original project
   and has improved attribute handling and drawing function.
   It is not backward compatible with earlier versions.  Breaking 
   backward compatibility was necessary to correct the attribute handling
   for graphs, nodes, and edges.

   Pygraphviz is distributed with a BSD license.


Quick Example
-------------

   Just write in Python::

    >>> from pygraphviz import *
    >>> G=AGraph()
    >>> G.add_node('a')
    >>> G.add_edge('b','c')
    >>> G
    strict graph {
            a;
            b -- c;
    }


   More documentation

     - Tutorial  http://networkx.lanl.gov/pygraphviz/Tutorial
     - Reference Manual  http://networkx.lanl.gov/reference/pygraphviz/


Requirements
-------------

   To use pygraphviz you need

      - Python version 2.3 or later http://www.python.org/
      - Graphviz http://graphviz.org/

Downloading
-----------

   You can download pygraphviz from  http://sourceforge.net/project/showfiles.php?group_id=122233

   You can browse the source at https://networkx.lanl.gov/browser/pygraphviz/trunk

   To access the repository using subversion, you will need a subversion client (e.g. svn for Linux). Then check out the code using

    svn co https://networkx.lanl.gov/svn/pygraphviz/trunk pygraphviz


Quick Install
-------------

   Tested on Linux and OSX.  In principle will work on any platform
   with a C compiler and the Graphviz libraries.  

   Download the source, unpack, and run "python setup.py install". 

   Also may be installed using EasyInstall http://peak.telecommunity.com/DevCenter/EasyInstall

   easy_install pygraphviz	


History
-------

   The original concept was developed and implemented by
   Manos Renieris at Brown University: 
   http://www.cs.brown.edu/~er/software/


Development
-----------

   pygraphviz is currently maintained by Aric Hagberg and Dan Schult

   More information can be found at https://networkx.lanl.gov/pygraphviz/

   For bug reports and feature requests fill out a ticket at
   https://networkx.lanl.gov/newticket/

