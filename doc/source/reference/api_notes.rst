API Notes
=========

pygraphviz-1.2
--------------
  No API changes

pygraphviz-1.1
--------------
  Pygraphviz-1.1 adds unicode (graphviz charset) support.
  The default Node type is now unicode.
  See examples/utf8.py for an example of how to use non-ASCII characters.

  The __str__ and  __repr__ methods have been rewritten and a __unicode__
  method added.

  If G is a pygraphviz.AGraph object then

  - str(G) produces a dot-format string representation 
    (some characters might not be represented correctly)
  - unicode(G) produces a dot-format unicode representation
  - repr(G) produces a string of the unicode representation.
  - print G produces a formatted dot language output
  

pygraphivz-0.32
---------------
  pygraphviz-0.32 is a rewrite of pygraphviz-0.2x  with some significant
  changes in the API and Graphviz wrapper.  It is not compatible with
  with earlier versions.

  The goal of pygraphviz is to provide a (mostly) Pythonic interface
  to the Graphviz Agraph data-structure, layout, and drawing algorithms.

  The API is now similar to the NetworkX API.  Studying the
  documentation and Tutorial for NetworkX will teach you most of what
  you need to know for pygraphviz.  For a short introduction on pygraphviz
  see the pygraphviz Tutorial.

  There are some important differences between the PyGraphviz
  and NetworkX API.  With PyGraphviz

   - All nodes must be of string or unicode type. 
     An attempt will be made to convert other types to a string.

   - Nodes and edges are custom Python objects.  Nodes are like
     unicode/string objects and edges are like tuple objects.  (In NetworkX
     nodes can be anything and edges are two- or three-tuples.)

   - Graphs, edges, and nodes may have attributes such as color,
     size, shape, attached to them.  If the attributes are known
     Graphviz attributes they will be used for drawing and layout.

   - The layout() and draw() methods allow positioning of nodes
     and rendering in all of the supported Graphviz output formats.

   - The string() method produces a string with the graph represented
     in Graphviz dot format.  See also from_string().
   
   - The subgraph() method is the Graphviz representation of
     subgraphs: a tree of graphs under the original
     (root) graph. The are primarily used for clustering of nodes when
     drawing with dot.

  Pygraphviz supports most of the Graphviz API.

