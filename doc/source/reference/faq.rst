FAQ
===

   :Q: **I followed the installation instructions but when I do:**

       >>> import pygraphviz 

       **I get an error like:**

       ``ImportError: libagraph.so.1: cannot open shared object file: No
       such file or directory``

       **What is wrong?**

   :A: Some Unix systems don't include the Graphviz library in the
       default search path for the run-time linker.  The path is often
       something like ``/usr/lib/graphviz`` or ``/sw/lib/graphviz`` etc. and
       it needs to be added to your search path.
       On \*nix systems, the preferred way to do this is by setting the
       appropriate flags when building/installing ``pygraphviz``.
       For example, if the Graphviz libraries are installed in
       ``/opt/lib/mygviz/`` on your system:

       .. code-block:: bash

          pip install --global-option=build_ext \
                      --global-option="-L/opt/lib/mygviz/" \
                      --global-option="-R/opt/lib/mygviz/" \
                      pygraphviz

       In this example, the ``-L`` and ``-R`` flags tell the linker where to
       look for the required Graphviz libraries at build time and run time,
       respectively.

   :Q: **How do I compile pygraphviz under Windows?**

   :A: See :ref:`windows-install` for the latest on how to
       install Graphviz and pygraphviz on Windows.

   :Q: **Why don't you distribute a pygraphviz Windows installer?**

   :A: We would very much like to make binary wheels available for ``pygraphviz``,
       but there are several complications.
       ``pygraphviz`` is a wrapper around Graphviz, which means that Graphviz
       must be installed, and Graphviz header files, libraries *and* command
       line executables must all be accessible for the wrapper.
       The recommended use of the `Graphviz CLI`_ poses challenges for wheel
       packaging.

       .. seealso:: 
          This `GitHub issue <https://github.com/pygraphviz/pygraphviz/issues/167>`__
          for further discussion on wheels and packaging.

.. _Graphviz CLI: https://gitlab.com/graphviz/graphviz/-/issues/1808#note_403608643
