*******
Install
*******

PyGraphviz requires:

- Python (version 3.7, 3.8, or 3.9)
- `GraphViz <https://www.graphviz.org/>`_ (version 2.42 or later)


.. note::
   We assume you have Python on your computer.   

Recommended
===========

We recommend installing Python packages using `pip and virtual environments
<https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_.

Linux
-----

We recommend installing Graphviz using your Linux system's package manager.
Below are examples for some popular distribtions.

Ubuntu and Debian
~~~~~~~~~~~~~~~~~

.. code-block:: console

    $ sudo apt-get install graphviz graphviz-dev
    $ pip install pygraphviz 

Fedora and Red Hat
~~~~~~~~~~~~~~~~~~

You may need to replace ``dnf`` with ``yum`` in the example below.

.. code-block:: console

    $ sudo dnf install install graphviz graphviz-devel
    $ pip install pygraphviz

macOS
-----

We recommend installing Graphviz using the Homebrew package manager for macOS.

Homebrew
~~~~~~~~

.. code-block:: console

    $ brew install graphviz
    $ pip install pygraphviz

Advanced
========

The two main difficulties are
(1) informing pip where Graphviz is installed and
(2) installing Graphviz.


Providing path to Graphviz
--------------------------

You need to know where the binary files, includes files, and library files for Graphviz
are located on your file system.
Here are some examples of how you tell pip where these files are.

MacPorts
~~~~~~~~

.. code-block:: console

    $ port install graphviz-devel
    $ pip install --global-option=build_ext \
                  --global-option="-I/opt/local/include/" \
                  --global-option="-L/opt/local/lib/" \
                  pygraphviz

.. _windows-install:

Installing Graphviz on Windows
------------------------------

Installing Graphviz and PyGraphviz on Windows is not easy.
Fortunately, the situation is being worked on and there will be more
information here soon.

.. include:: reference/faq.rst
