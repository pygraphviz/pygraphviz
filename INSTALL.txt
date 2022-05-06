*******
Install
*******

PyGraphviz requires:

- Python (version 3.8, 3.9, or 3.10)
- `Graphviz <https://www.graphviz.org/>`_ (version 2.42 or later)
- C/C++ Compiler

.. note::
   These instructions assume you have Python and a C/C++ Compiler on your computer.

.. warning::
   Do not use the default channels to install pygraphviz with ``conda``. The
   conda-forge channel should be used instead::

       conda install --channel conda-forge pygraphviz

   - |conda-forge-ubuntu-badge|
   - |conda-forge-macos-badge|
   - |conda-forge-windows-badge|


.. |conda-forge-ubuntu-badge| image:: https://github.com/pygraphviz/pygraphviz/workflows/conda-forge-ubuntu/badge.svg
.. |conda-forge-macos-badge| image:: https://github.com/pygraphviz/pygraphviz/workflows/conda-forge-macos/badge.svg
.. |conda-forge-windows-badge| image:: https://github.com/pygraphviz/pygraphviz/workflows/conda-forge-windows/badge.svg

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

We recommend installing Graphviz using the Homebrew package manager or MacPorts for macOS.

Homebrew
~~~~~~~~

.. code-block:: console

    $ brew install graphviz
    $ pip install pygraphviz

MacPorts
~~~~~~~~

.. code-block:: console

    $ port install graphviz
    $ pip install pygraphviz
    $ pip install --global-option=build_ext \
                  --global-option="-I/opt/local/include/" \
                  --global-option="-L/opt/local/lib/" \
                  pygraphviz

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
