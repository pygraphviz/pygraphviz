.. _contents:

Python interface to Graphviz
============================

.. only:: html

    :Release: |version|
    :Date: |today|

PyGraphviz is a Python interface to the Graphviz graph layout and
visualization package.
With PyGraphviz you can create, edit, read, write, and draw graphs using
Python to access the Graphviz graph data structure and layout algorithms.
PyGraphviz provides a similar programming interface to NetworkX
(https://networkx.org).

Example
-------

.. code:: pycon

    >>> import pygraphviz as pgv
    >>> G = pgv.AGraph()
    >>> G.add_node("a")
    >>> G.add_edge("b", "c")
    >>> print(G)
    strict graph "" {
            a;
            b -- c;
    }

License
-------

.. include:: ../../LICENSE


.. toctree::
   :maxdepth: 1
   :hidden:

   install
   tutorial
   auto_examples/index
   reference/index
   developer/index
   release/index
