PyGraphviz
==========

.. image:: https://github.com/pygraphviz/pygraphviz/workflows/test/badge.svg?branch=master
  :target: https://github.com/pygraphviz/pygraphviz/actions?query=workflow%3Atest+branch%3Amaster

.. image:: https://codecov.io/gh/pygraphviz/pygraphviz/branch/master/graph/badge.svg
   :target: https://app.codecov.io/gh/pygraphviz/pygraphviz/branch/master


PyGraphviz is a Python interface to the Graphviz graph layout and
visualization package.
With PyGraphviz you can create, edit, read, write, and draw graphs using
Python to access the Graphviz graph data structure and layout algorithms.
PyGraphviz provides a similar programming interface to NetworkX
(https://networkx.org). 

- **Website (including documentation):** https://pygraphviz.github.io
- **Mailing list:** https://groups.google.com/forum/#!forum/pygraphviz-discuss
- **Source:** https://github.com/pygraphviz/pygraphviz
- **Bug reports:** https://github.com/pygraphviz/pygraphviz/issues

Simple example
--------------

.. code:: python

    >>> import pygraphviz as pgv
    >>> G = pgv.AGraph()
    >>> G.add_node("a")
    >>> G.add_edge("b", "c")
    >>> print(G)
    strict graph "" {
            a;
            b -- c;
    }

Install
-------

PyGraphviz requires Graphviz.
Please see `INSTALL.rst` for details.

License
-------

Released under the 3-Clause BSD license (see ``LICENSE``)::

  Copyright (C) 2006-2021 PyGraphviz Developers
  Aric Hagberg <aric.hagberg@gmail.gov>
  Dan Schult <dschult@colgate.edu>
  Manos Renieris
