**********
Installing
**********

Quick Install
=============

Get PyGraphviz from the Python Package Index at
http://pypi.python.org/pypi/pygraphviz

or install it with::

   easy_install pygraphviz

and an attempt will be made to find and install an appropriate version
that matches your operating system and Python version. 

More download options are at http://networkx.lanl.gov/download.html

Installing from Source
======================

You can install from source by downloading a source archive file
(tar.gz or zip) or by checking out the source files from the
Subversion repository.

Source Archive File
-------------------

  1. Download the source (tar.gz or zip file).

  2. Unpack and change directory to pygraphviz-"version" 

  3. Run "python setup.py install" to build and install 

  4. (optional) Run "python setup_egg.py nosetests" to execute the tests


SVN Repository
--------------

  1. Check out the PyGraphviz trunk::

       svn co https://networkx.lanl.gov/svn/pygraphviz/trunk pygraphviz

  2. Change directory to "pygraphviz"   

  3.  Run "python setup.py install" to build and install 

  4. (optional) Run "python setup_egg.py nosetests" to execute the tests


If you don't have permission to install software on your
system, you can install into another directory using
the --prefix or --home flags to setup.py.

For example

::  

    python setup.py install --prefix=/home/username/python
    or
    python setup.py install --home=~

If you didn't install in the standard Python site-packages directory
you will need to set your PYTHONPATH variable to the alternate location.
See http://docs.python.org/inst/search-path.html for further details.


Requirements
============

GraphViz
--------

To use PyGraphviz you need GraphViz version 2.16 or later.
Some versions have known bugs that have been fixed; get the latest
release available for best results.

 - Official site: http://www.graphviz.org


Python
------

To use PyGraphviz you need Python version 2.4 or later http://www.python.org/

The easiest way to get Python and most optional packages is to install
the Enthought Python distribution
http://www.enthought.com/products/epd.php

Other options are

Windows
~~~~~~~
 - Official Python site version:  http://www.python.org/download/

 - ActiveState version:  http://activestate.com/Products/ActivePython/

OSX
~~~

OSX 10.5 ships with Python version 2.5.  If you
have an older version we encourage you to download
a newer release. Pre-built Python packages are available from 

 - Official Python site version  http://www.python.org/download/

 - Pythonmac  http://www.pythonmac.org/packages/ 

 - ActiveState http://activestate.com/Products/ActivePython/


If you are using Fink or MacPorts, Python is available through both
of those package systems.

Linux
~~~~~
Python is included in all major Linux distributions

