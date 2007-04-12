Pygraphviz
----------

   Pygraphviz is a Python interface to the Graphviz graph layout and
   visualization package.

   With Pygraphviz you can create, edit, read, write, and draw graphs using
   Python to access the Graphviz graph data structure and layout algorithms.

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
     - Examples  http://networkx.lanl.gov/pygraphviz/Examples


Requirements
-------------

   To use Pygraphviz you need

      - Python version 2.3 or later http://www.python.org/
      - Graphviz http://graphviz.org/ 

Downloading
-----------

   You can download pygraphviz from  http://sourceforge.net/project/showfiles.php?group_id=122233

   You can browse the source at https://networkx.lanl.gov/browser/pygraphviz/trunk

   To access the repository using subversion, you will need a subversion client (e.g. svn for Linux). Then check out the code using

    svn co https://networkx.lanl.gov/svn/pygraphviz/trunk pygraphviz


Building pygraphviz
-------------------

   To build pygraphviz you need:	

      - Python version 2.3 or later http://www.python.org/

        Linux users will need the python-dev package installed.

      - Graphviz http://graphviz.org/ 

        Tested with version 2.8 or later, but may work with earlier versions.
	Linux users might need to install the graphviz-dev package.

      - A C compiler


   Pygraphviz is developed and tested on Linux and OSX.  
   In principle it will work on any platform that has Python,
   a C compiler, and the Graphviz libraries.  

   Installing from source:

      - Download the source (tar.gz or zip file)
      - Unpack and change directory to pygraphviz-x.xx
      - Run "python setup.py install" to build and install
      
   See the FAQ http://networkx.lanl.gov/pygraphviz/FAQ.html
   for a note about building pygraphviz with Windows.

Testing
-------

   Import the module and run the tests 

   >>> import pygraphviz
   >>> pygraphviz.test()


History
-------

   The original concept was developed and implemented by
   Manos Renieris at Brown University: 
   http://www.cs.brown.edu/~er/software/


Related Pacakges
----------------

   - Python bindings distributed with Graphviz (graphviz-python):  http://www.graphviz.org/Download_linux.php

   - Pydot: http://dkbza.org/pydot.html

   - mfGraph: http://www.geocities.com/foetsch/mfgraph/index.htm

   - Yapgvb: http://yapgvb.sourceforge.net/


Development
-----------

   Pygraphviz is currently maintained by 
   Aric Hagberg  (http://math.lanl.gov/~hagberg/)
   and Dan Schult

   More information can be found at https://networkx.lanl.gov/pygraphviz/

   For bug reports and feature requests fill out a ticket at
   https://networkx.lanl.gov/newticket/

   Because of ongoing spam problems you will need to register first at
   https://networkx.lanl.gov/register