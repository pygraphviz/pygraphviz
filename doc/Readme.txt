----------
Pygraphviz
----------

Pygraphviz
----------

   Pygraphviz is a Python interface to the Graphviz graph layout and
   visualization package.

   With Pygraphviz you can create, edit, read, write, and draw graphs using
   Python to access the Graphviz internal graph data structure and 
   layout algorithms.

   Pygraphviz is distributed with a BSD license.

   News:

   The release pygraphviz-0.32 is the second rewrite of the original project.
   It has improved attribute handling and drawing capabilities.
   It is not backward compatible with earlier versions.
   Earlier versions will always be available at the download site.


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
     - Examples  http://networkx.lanl.gov/pygraphviz/Examples


Requirements
-------------

   To use Pygraphviz you need

      - Python version 2.3 or later http://www.python.org/
      - Graphviz http://graphviz.org/ 
        Tested with version 2.8 or later, but may work with earlier versions.
	Linux users might need to install the graphviz-dev package.
      - A C compiler

Downloading
-----------

   You can download pygraphviz from  http://sourceforge.net/project/showfiles.php?group_id=122233

   You can browse the source at https://networkx.lanl.gov/browser/pygraphviz/trunk

   To access the repository using subversion, you will need a subversion client (e.g. svn for Linux). Then check out the code using

    svn co https://networkx.lanl.gov/svn/pygraphviz/trunk pygraphviz


Quick Install
-------------

   Pygraphviz is developed and tested on Linux and OSX.  
   In principle it will work on any platform that has Python,
   a C compiler, and the Graphviz libraries.  

   Installing from source:

      - Download the source (tar.gz or zip file)
      - Unpack and change directory to pygraphviz-x.xx
      - Run "python setup.py install" to build and install
      - (optional) cd pygraphviz/tests and run "python setup_egg.py test" to execute the tests
      
    
   Installing a Python egg from source:

      - Download the source (tar.gz or zip file)
      - Unpack and change directory to pygraphviz-x.xx
      - Run "python setup_egg.py install" to build and install
      - (optional) run "python setup_egg.py test" to execute the tests


History
-------

   The original concept was developed and implemented by
   Manos Renieris at Brown University: 
   http://www.cs.brown.edu/~er/software/


Development
-----------

   Pygraphviz is currently maintained by Aric Hagberg and Dan Schult

   More information can be found at https://networkx.lanl.gov/pygraphviz/

   For bug reports and feature requests fill out a ticket at
   https://networkx.lanl.gov/newticket/

