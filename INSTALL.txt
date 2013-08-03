**********
Installing
**********

Quick Install
=============

Get PyGraphviz from the Python Package Index at
http://pypi.python.org/pypi/pygraphviz

or install it with::

   pip install pygraphviz

and an attempt will be made to find and install an appropriate version
that matches your operating system and Python version.

You can install the development version (at github.com) with::

  pip install git://github.com/pygraphviz/pygraphviz.git#egg=pygraphviz


Get PyGraphviz from the Python Package Index at
http://pypi.python.org/pypi/pygraphviz

or install it with::

   easy_install pygraphviz

and an attempt will be made to find and install an appropriate version
that matches your operating system and Python version. 


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


Github
------

  1. Clone the pygraphviz repostitory

       git clone https://github.com/pygraphviz/pygraphviz.git

  (see https://github.com/pygraphviz/pygraphviz/ for other options)

  2. Change directory to "pygraphviz"

  3.  Run "python setup.py install" to build and install

  4. (optional) Run "python setup_egg.py nosetests" to execute the tests


If you don't have permission to install software on your
system, you can install into another directory using
the --user, --prefix, or --home flags to setup.py.

For example

::

    python setup.py install --prefix=/home/username/python
    or
    python setup.py install --home=~
    or
    python setup.py install --user

If you didn't install in the standard Python site-packages directory
you will need to set your PYTHONPATH variable to the alternate location.
Seehttp://docs.python.org/2/install/index.html#search-path for further details.


Requirements
============

Python
------

To use PyGraphviz you need Python version 2.6.x or 2.7.x.
PyGraphviz does not work with Python 3

The easiest way to get Python and most optional packages is to install
the Enthought Python distribution "Canopy"
https://www.enthought.com/products/canopy/

There are several other distributions that contain the key packages you need for scientific computing.  See the following link for a list: http://scipy.org/install.html


Requirements
============

GraphViz
--------

To use PyGraphviz you need GraphViz version 2.16 or later.
Some versions have known bugs that have been fixed; get the latest
release available for best results.

 - Official site: http://www.graphviz.org

