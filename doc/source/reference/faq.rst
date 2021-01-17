FAQ
---

   :Q: I followed the installation instructions but when I do

       >>> import pygraphviz 

       I get an error like:

       ``ImportError: libagraph.so.1: cannot open shared object file: No
       such file or directory``

       What is wrong?

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

   :Q: How do I compile pygraphviz under Windows?  And why
       don't you distribute a pygraphviz Windows installer?

   :A: We don't have Windows development machines but would like to
       have pygraphviz work on all platforms.  If you have success
       with Windows or would be willing to help test and distribute a
       Windows installer please drop us a note. 
       
       See also issues at: https://github.com/pygraphviz/pygraphviz/search?q=Windows&type=Issues
