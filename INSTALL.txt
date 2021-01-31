*******
Install
*******

PyGraphviz requires:

- Python (version 3.7, 3.8, or 3.9)
- `Graphviz <https://www.graphviz.org/>`_ (version 2.42 or later)
- C/C++ Compiler

.. note::
   These instructions assume you have Python and a C/C++ Compiler on your computer.   

.. warning::
   We recommend avoiding Anaconda and conda-forge to install Graphviz and PyGraphviz.

Recommended
===========

We recommend installing Python packages using `pip and virtual environments
<https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_.

Linux
-----

We recommend installing Graphviz using your Linux system's package manager.
Below are examples for some popular distributions.

Ubuntu and Debian
~~~~~~~~~~~~~~~~~

.. code-block:: console

    $ sudo apt-get install graphviz graphviz-dev
    $ pip install pygraphviz 

Fedora and Red Hat
~~~~~~~~~~~~~~~~~~

You may need to replace ``dnf`` with ``yum`` in the example below.

.. code-block:: console

    $ sudo dnf install graphviz graphviz-devel
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
   1. installing Graphviz and
   2. informing pip where Graphviz is installed.

Providing path to Graphviz
--------------------------

If you've installed Graphviz and ``pip`` is unable to find Graphviz, then you need to
provide ``pip`` with the path(s) where it can find Graphviz.
To do this, you first need to figure out where the binary files, includes files, and
library files for Graphviz are located on your file system.

Once you know where you've installed Graphviz, you will need to do something like
the following.  There is an additional example using Chocolatey on Windows further
down the page.

MacPorts
~~~~~~~~

.. note:: ``port install graphviz-devel`` installs an old developer release of Graphviz.
Hopefully, the MacPorts packagers will update Graphviz to a recent release.
Once that happens, you may want to use ``port install graphviz`` instead of
``port install graphviz-devel`` below.
There is an open ticket to upgrade MacPorts to version 2.46.0 here:
https://trac.macports.org/ticket/62165

.. code-block:: console

    $ port install graphviz-devel
    $ pip install --global-option=build_ext \
                  --global-option="-I/opt/local/include/" \
                  --global-option="-L/opt/local/lib/" \
                  pygraphviz

.. _windows-install:

Windows
-------

Historically, installing Graphviz and PyGraphviz on Windows has been challenging.
Fortunately, the Graphviz developers are working to fix this and
their recent releases have much improved the situation.

For this reason, PyGraphviz 1.7 only supports Graphviz 2.46.0 or higher on Windows.
We recommend either manually installing the official binary release of Graphviz or
using `Chocolatey <https://chocolatey.org/>`_, which has been updated to Graphviz 2.46.0.

You may also need to install Visual C/C++, e.g. from here:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

Assuming you have Python and Visual C/C++ installed,
we believe the following should work on Windows 10 (64 bit) using PowerShell.

Manual download
~~~~~~~~~~~~~~~

1. Download and install 2.46.0 for Windows 10 (64-bit):
   `stable_windows_10_cmake_Release_x64_graphviz-install-2.46.0-win64.exe
   <https://gitlab.com/graphviz/graphviz/-/package_files/6164164/download>`_.
2. Install PyGraphviz via

.. code-block:: console

    PS C:\> python -m pip install --global-option=build_ext `
                  --global-option="-IC:\Program Files\Graphviz\include" `
                  --global-option="-LC:\Program Files\Graphviz\lib" `
                  pygraphviz

Chocolatey
~~~~~~~~~~

.. code-block:: console

    PS C:\> choco install graphviz
    PS C:\> python -m pip install --global-option=build_ext `
                  --global-option="-IC:\Program Files\Graphviz\include" `
                  --global-option="-LC:\Program Files\Graphviz\lib" `
                  pygraphviz

.. include:: reference/faq.rst
