FAQ
---

   :Q: I followed the installation instructions but when I do

       >>> import pygraphviz 

       I get an error like
       ImportError: libagraph.so.1: cannot open shared object file: No
       such file or directory

       What is wrong?

   :A: Some Unix systems don't include the Graphviz library in the
       default search path for the run-time linker.  The path is often
       something like /usr/lib/graphviz or /sw/lib/graphviz etc. and
       it needs to be added to your search path.  You can

       1. set the LD_LIBRARY_PATH environment variable
          e.g. export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib/graphviz

       2. configure your system with the additional path.
          e.g. for Linux add a line to /etc/ld.so.conf and
	  run ldconfig


   :Q: How do I compile pygraphviz under Windows?  And why
       don't you distribute a pygraphviz Windows installer?

   :A: We don't have Windows development machines but would like to
       have pygraphviz work on all platforms.  If you have success
       with Windows or would be willing to help test and distribute a
       Windows installer please drop us a note. 
       
       See also tickets: https://networkx.lanl.gov/trac/ticket/117
        https://networkx.lanl.gov/trac/ticket/491
