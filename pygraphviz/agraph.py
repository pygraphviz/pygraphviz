"""
A Python interface to Graphviz.

"""
#    Copyright (C) 2006-2011 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.
#    All rights reserved, see LICENSE for details.

import re
import shlex
import subprocess
import sys
import threading
import warnings
from collections.abc import MutableMapping

from . import graphviz as gv

_DEFAULT_ENCODING = "UTF-8"
_PY2 = sys.version_info[0] == 2
_TEXT_TYPE = unicode if _PY2 else str
_STRING_TYPES = (basestring,) if _PY2 else (str,)


def is_string_like(obj):
    return isinstance(obj, _STRING_TYPES)


class PipeReader(threading.Thread):
    """Read and write pipes using threads.
    """

    def __init__(self, result, pipe):
        threading.Thread.__init__(self)
        self.result = result
        self.pipe = pipe

    def run(self):
        try:
            while True:
                chunk = self.pipe.read()
                if not chunk:
                    break
                self.result.append(chunk)
        finally:
            self.pipe.close()


class _Action:
    find, create = 0, 1


class DotError(ValueError):
    """Dot data parsing error"""


class AGraph:
    """Class for Graphviz agraph type.

    Example use

    >>> from pygraphviz import *
    >>> G=AGraph()
    >>> G=AGraph(directed=True)
    >>> G=AGraph("file.dot")   # doctest: +SKIP

    Graphviz graph keyword parameters are processed so you may add
    them like

    >>> G=AGraph(landscape='true',ranksep='0.1')

    or alternatively

    >>> G=AGraph()
    >>> G.graph_attr.update(landscape='true',ranksep='0.1')

    and

    >>> G.node_attr.update(color='red')
    >>> G.edge_attr.update(len='2.0',color='blue')

    See http://www.graphviz.org/doc/info/attrs.html
    for a list of attributes.

    Keyword parameters:

    thing is a generic input type (filename, string, handle to pointer,
    dictionary of dictionaries).  An attempt is made to automaticaly
    detect the type so you may write for example:

    >>> d={'1': {'2': None}, '2': {'1': None, '3': None}, '3': {'2': None}}
    >>> A=AGraph(d)
    >>> s=A.to_string()
    >>> B=AGraph(s)
    >>> h=B.handle
    >>> C=AGraph(h)

    Parameters::

      name:    Name for the graph

      strict: True|False (True for simple graphs)

      directed: True|False

      data: Dictionary of dictionaries or dictionary of lists
      representing nodes or edges to load into initial graph

      string:  String containing a dot format graph

      handle:  Swig pointer to an agraph_t data structure

    """

    def __init__(
        self,
        thing=None,
        filename=None,
        data=None,
        string=None,
        handle=None,
        name="",
        strict=True,
        directed=False,
        **attr,
    ):
        self.handle = None  # assign first in case the __init__ bombs
        self._owns_handle = True
        # initialization can take no arguments (gives empty graph) or
        # a file name
        # a string of graphviz dot language
        # a swig pointer (handle) to a graph
        # a dict of dicts (or dict of lists) data structure

        self.has_layout = False  # avoid creating members outside of init

        # backward compability
        filename = attr.pop("file", filename)
        #  guess input type if specified as first (nonkeyword) argument
        if thing is not None:
            # can't specify first argument and also file,data,string,handle
            filename = None
            data = None
            string = None
            handle = None
            if isinstance(thing, dict):
                data = thing  # a dictionary of dictionaries (or lists)
            elif hasattr(thing, "own"):  # a Swig pointer - graph handle
                handle = thing
            elif is_string_like(thing):
                pattern = re.compile(r"(strict)?\s*(graph|digraph).*{.*}\s*", re.DOTALL)
                if pattern.match(thing):
                    string = thing  # this is a dot format graph in a string
                else:
                    filename = thing  # assume this is a file name
            elif hasattr(thing, "open"):
                filename = thing  # assume this is a file name (in a path obj)
            else:
                raise TypeError("Unrecognized input %s" % thing)

        if handle is not None:
            # if handle was specified, reference it
            self.handle = handle
            self._owns_handle = False
        elif filename is not None:
            # load new graph from file (creates self.handle)
            self.read(filename)
        elif string is not None:
            # load new graph from string (creates self.handle)
            # get the charset from the string to properly encode it for
            # writing to the temporary file in from_string()
            match = re.search(r'charset\s*=\s*"([^"]+)"', string)
            if match is not None:
                self.encoding = match.group(1)
            else:
                self.encoding = _DEFAULT_ENCODING
            self.from_string(string)
        else:
            # no handle, need to
            self.handle = None

        if self.handle is not None:
            # the handle was specified or created
            # get the encoding from the "charset" graph attribute
            item = gv.agget(self.handle, b"charset")
            if item is not None:
                self.encoding = (
                    item if type(item) is not bytes else item.decode("utf-8")
                )
            else:
                self.encoding = _DEFAULT_ENCODING
        else:
            # no handle was specified or created
            # get encoding from the "charset" kwarg
            self.encoding = attr.get("charset", _DEFAULT_ENCODING)
            try:
                if name is None:
                    name = ""
                    # instantiate a new, empty graph
                self.handle = gv.agraphnew(name.encode(self.encoding), strict, directed)
            except TypeError:
                raise TypeError("Graph name must be a string: %s" % name)

            # encoding is already set but if it was specified explicitly
            # as an attr, then set it explicitly for the graph
            if "charset" in attr:
                gv.agattr_label(self.handle, 0, "charset", self.encoding)

            # if data is specified, populate the newly created graph
            if data is not None:
                # load from dict of dicts or dict of lists
                for node in data:
                    for nbr in data[node]:
                        self.add_edge(node, nbr)
                self.add_nodes_from(data.keys())

        # throw away the charset attribute, if one exists,
        # since we've already set it, and now it should not be changed
        if "charset" in attr:
            del attr["charset"]

        # assign any attributes specified through keywords
        self.graph_attr = Attribute(self.handle, 0)  # default graph attributes
        self.graph_attr.update(attr)  # apply attributes passed to init
        self.node_attr = Attribute(self.handle, 1)  # default node attributes
        self.edge_attr = Attribute(self.handle, 2)  # default edge attribtes

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        pass

    if _PY2:

        def __unicode__(self):
            return self.string()

        def __str__(self):
            return unicode(self).encode(self.encoding, "replace")

    else:

        def __str__(self):
            return self.string()

    def __repr__(self):
        name = gv.agnameof(self.handle)
        if name is None:
            return "<AGraph %s>" % self.handle
        return f"<AGraph {name} {self.handle}>"

    def __eq__(self, other):
        # two graphs are equal if they have exact same string representation
        # this is not graph isomorphism
        return self.string() == other.string()

    def __hash__(self):
        # hash the string representation for id
        return hash(self.string())

    def __iter__(self):
        # provide "for n in G"
        return self.nodes_iter()

    def __contains__(self, n):
        # provide "n in G"
        return self.has_node(n)

    def __len__(self):
        return self.number_of_nodes()

    def __getitem__(self, n):
        # "G[n]" returns nodes attached to n
        return self.neighbors(n)

    # not implemented, but could be...
    #    def __setitem__(self,u,v):
    #        self.add_edge(u,v)

    def __del__(self):
        self._close_handle()

    def get_name(self):
        name = gv.agnameof(self.handle)
        if name is not None:
            name = name.decode(self.encoding)
        return name

    name = property(get_name)

    def add_node(self, n, **attr):
        """Add a single node n.

        If n is not a string, conversion to a string will be attempted.
        String conversion will work if n has valid string representation
        (try str(n) if you are unsure).

        >>> G=AGraph()
        >>> G.add_node('a')
        >>> G.nodes()  # doctest: +IGNORE_UNICODE
        [u'a']
        >>> G.add_node(1) # will be converted to a string
        >>> G.nodes()  # doctest: +IGNORE_UNICODE
        [u'a', u'1']

        Attributes can be added to nodes on creation or updated after creation
        (attribute values must be strings)

        >>> G.add_node(2,color='red')

        See http://www.graphviz.org/doc/info/attrs.html
        for a list of attributes.

        Anonymous Graphviz nodes are currently not implemented.
        """
        if not is_string_like(n):
            n = str(n)
        n = n.encode(self.encoding)
        try:
            nh = gv.agnode(self.handle, n, _Action.find)
        except KeyError:
            nh = gv.agnode(self.handle, n, _Action.create)
        node = Node(self, nh=nh)
        node.attr.update(**attr)

    def add_nodes_from(self, nbunch, **attr):
        """Add nodes from a container nbunch.

        nbunch can be any iterable container such as a list or dictionary

        >>> G=AGraph()
        >>> nlist=['a','b',1,'spam']
        >>> G.add_nodes_from(nlist)
        >>> sorted(G.nodes())  # doctest: +IGNORE_UNICODE
        [u'1', u'a', u'b', u'spam']


        Attributes can be added to nodes on creation or updated after creation

        >>> G.add_nodes_from(nlist, color='red') # set all nodes in nlist red
        """
        for n in nbunch:
            self.add_node(n, **attr)

    def remove_node(self, n):
        """Remove the single node n.

        Attempting to remove a node that isn't in the graph will produce
        an error.

        >>> G=AGraph()
        >>> G.add_node('a')
        >>> G.remove_node('a')
        """
        if not is_string_like(n):
            n = str(n)
        n = n.encode(self.encoding)
        try:
            nh = gv.agnode(self.handle, n, _Action.find)
            gv.agdelnode(self.handle, nh)
        except KeyError:
            raise KeyError("Node %s not in graph." % n.decode(self.encoding))

    delete_node = remove_node

    def remove_nodes_from(self, nbunch):
        """Remove nodes from a container nbunch.

        nbunch can be any iterable container such as a list or dictionary

        >>> G=AGraph()
        >>> nlist=['a','b',1,'spam']
        >>> G.add_nodes_from(nlist)
        >>> G.remove_nodes_from(nlist)
        """
        for n in nbunch:
            self.remove_node(n)

    delete_nodes_from = remove_nodes_from

    def nodes_iter(self):
        """Return an iterator over all the nodes in the graph.

        Note: modifying the graph structure while iterating over
        the nodes may produce unpredictable results.  Use nodes()
        as an alternative.
        """
        nh = gv.agfstnode(self.handle)
        while nh is not None:
            yield Node(self, nh=nh)
            try:
                nh = gv.agnxtnode(self.handle, nh)
            except StopIteration:
                return

    iternodes = nodes_iter

    def nodes(self):
        """Return a list of all nodes in the graph."""
        return list(self.nodes_iter())

    def number_of_nodes(self):
        """Return the number of nodes in the graph."""
        return gv.agnnodes(self.handle)

    def order(self):
        """Return the number of nodes in the graph."""
        return self.number_of_nodes()

    def has_node(self, n):
        """Return True if n is in the graph or False if not.

        >>> G=AGraph()
        >>> G.add_node('a')
        >>> G.has_node('a')
        True
        >>> 'a' in G  # same as G.has_node('a')
        True

        """
        try:
            node = Node(self, n)
            return True
        except KeyError:
            return False

    def get_node(self, n):
        """Return a node object (Node) corresponding to node n.

        >>> G=AGraph()
        >>> G.add_node('a')
        >>> node=G.get_node('a')
        >>> print(node)
        a
        """
        return Node(self, n)

    def add_edge(self, u, v=None, key=None, **attr):
        """Add a single edge between nodes u and v.

        If the nodes u and v are not in the graph they will added.

        If u and v are not strings, conversion to a string will be attempted.
        String conversion will work if u and v have valid string representation
        (try str(u) if you are unsure).

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.edges()  # doctest: +IGNORE_UNICODE
        [(u'a', u'b')]

        The optional key argument allows assignment of a key to the
        edge.  This is especially useful to distinguish between
        parallel edges in multi-edge graphs (strict=False).

        >>> G=AGraph(strict=False)
        >>> G.add_edge('a','b','first')
        >>> G.add_edge('a','b','second')
        >>> sorted(G.edges(keys=True))  # doctest: +IGNORE_UNICODE
        [(u'a', u'b', u'first'), (u'a', u'b', u'second')]

        Attributes can be added when edges are created or updated after creation

        >>> G.add_edge('a','b',color='green')

        Attributes must be valid strings.

        See http://www.graphviz.org/doc/info/attrs.html
        for a list of attributes.

        """
        if v is None:
            (u, v) = u  # no v given, assume u is an edge tuple
        try:
            uh = Node(self, u).handle
        except:
            self.add_node(u)
            uh = Node(self, u).handle
        try:
            vh = Node(self, v).handle
        except:
            self.add_node(v)
            vh = Node(self, v).handle
        if key is not None:
            if not is_string_like(key):
                key = str(key)
            key = key.encode(self.encoding)
        try:
            # new
            eh = gv.agedge(self.handle, uh, vh, key, _Action.create)
        except KeyError:
            # for strict graph, or already added
            eh = gv.agedge(self.handle, uh, vh, key, _Action.find)
        e = Edge(self, eh=eh)
        e.attr.update(**attr)

    def add_edges_from(self, ebunch, **attr):
        """Add nodes to graph from a container ebunch.

        ebunch is a container of edges such as a list or dictionary.

        >>> G=AGraph()
        >>> elist=[('a','b'),('b','c')]
        >>> G.add_edges_from(elist)

        Attributes can be added when edges are created or updated after creation

        >>> G.add_edges_from(elist, color='green')
        """
        for e in ebunch:
            self.add_edge(e, **attr)

    def get_edge(self, u, v, key=None):
        """Return an edge object (Edge) corresponding to edge (u,v).

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> edge=G.get_edge('a','b')
        >>> print(edge)  # doctest: +IGNORE_UNICODE
        (u'a', u'b')

        With optional key argument will only get edge matching (u,v,key).

        """
        return Edge(self, u, v, key)

    def remove_edge(self, u, v=None, key=None):
        """Remove edge between nodes u and v from the graph.

        With optional key argument will only remove an edge
        matching (u,v,key).

        """
        if v is None:
            (u, v) = u  # no v given, assume u is an edge tuple
        e = Edge(self, u, v, key)
        try:
            gv.agdeledge(self.handle, e.handle)
        except KeyError:
            raise KeyError(f"Edge {u}-{v} not in graph.")

    delete_edge = remove_edge

    def remove_edges_from(self, ebunch):
        """Remove edges from ebunch (a container of edges)."""
        for e in ebunch:
            self.remove_edge(e)

    delete_edges_from = remove_edges_from

    def has_edge(self, u, v=None, key=None):
        """Return True an edge u-v is in the graph or False if not.

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.has_edge('a','b')
        True

        Optional key argument will restrict match to edges (u,v,key).

        """

        if v is None:
            (u, v) = u  # no v given, assume u is an edge tuple
        try:
            Edge(self, u, v, key)
            return True
        except KeyError:
            return False

    def edges(self, nbunch=None, keys=False):
        """Return list of edges in the graph.

        If the optional nbunch (container of nodes) only edges
        adjacent to nodes in nbunch will be returned.

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.add_edge('c','d')
        >>> print(sorted(G.edges()))  # doctest: +IGNORE_UNICODE
        [(u'a', u'b'), (u'c', u'd')]
        >>> print(G.edges('a'))  # doctest: +IGNORE_UNICODE
        [(u'a', u'b')]
        """
        return list(self.edges_iter(nbunch=nbunch, keys=keys))

    def has_neighbor(self, u, v, key=None):
        """Return True if u has an edge to v or False if not.

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.has_neighbor('a','b')
        True

        Optional key argument will only find edges (u,v,key).
        """
        return self.has_edge(u, v)

    def neighbors_iter(self, n):
        """Return iterator over the nodes attached to n.

        Note: modifying the graph structure while iterating over
        node neighbors may produce unpredictable results.  Use neighbors()
        as an alternative.
        """
        n = Node(self, n)
        nh = n.handle
        eh = gv.agfstedge(self.handle, nh)
        while eh is not None:
            (s, t) = Edge(self, eh=eh)
            if s == n:
                yield Node(self, t)
            else:
                yield Node(self, s)
            try:
                eh = gv.agnxtedge(self.handle, eh, nh)
            except StopIteration:
                return

    def neighbors(self, n):
        """Return a list of the nodes attached to n."""
        return list(self.neighbors_iter(n))

    iterneighbors = neighbors_iter

    def out_edges_iter(self, nbunch=None, keys=False):
        """Return iterator over out edges in the graph.

        If the optional nbunch (container of nodes) only out edges
        adjacent to nodes in nbunch will be returned.

        Note: modifying the graph structure while iterating over
        edges may produce unpredictable results.  Use out_edges()
        as an alternative.
        """

        if nbunch is None:  # all nodes
            nh = gv.agfstnode(self.handle)
            while nh is not None:
                eh = gv.agfstout(self.handle, nh)
                while eh is not None:
                    e = Edge(self, eh=eh)
                    if keys:
                        yield (e[0], e[1], e.name)
                    else:
                        yield e
                    try:
                        eh = gv.agnxtout(self.handle, eh)
                    except StopIteration:
                        break
                try:
                    nh = gv.agnxtnode(self.handle, nh)
                except StopIteration:
                    return
        elif nbunch in self:  # if nbunch is a single node
            n = Node(self, nbunch)
            nh = n.handle
            eh = gv.agfstout(self.handle, nh)
            while eh is not None:
                e = Edge(self, eh=eh)
                if keys:
                    yield (e[0], e[1], e.name)
                else:
                    yield e
                try:
                    eh = gv.agnxtout(self.handle, eh)
                except StopIteration:
                    return
        else:  # if nbunch is a sequence of nodes
            try:
                bunch = [n for n in nbunch if n in self]
            except TypeError:
                raise TypeError("nbunch is not a node or a sequence of nodes.")
            for n in nbunch:
                try:
                    nh = Node(self, n).handle
                except KeyError:
                    continue
                eh = gv.agfstout(self.handle, nh)
                while eh is not None:
                    e = Edge(self, eh=eh)
                    if keys:
                        yield (e[0], e[1], e.name)
                    else:
                        yield e
                    try:
                        eh = gv.agnxtout(self.handle, eh)
                    except StopIteration:
                        break

    iteroutedges = out_edges_iter

    def in_edges_iter(self, nbunch=None, keys=False):
        """Return iterator over out edges in the graph.

        If the optional nbunch (container of nodes) only out edges
        adjacent to nodes in nbunch will be returned.

        Note: modifying the graph structure while iterating over
        edges may produce unpredictable results.  Use in_edges()
        as an alternative.
        """
        if nbunch is None:  # all nodes
            nh = gv.agfstnode(self.handle)
            while nh is not None:
                eh = gv.agfstin(self.handle, nh)
                while eh is not None:
                    e = Edge(self, eh=eh)
                    if keys:
                        yield (e[0], e[1], e.name)
                    else:
                        yield e
                    try:
                        eh = gv.agnxtin(self.handle, eh)
                    except StopIteration:
                        break
                try:
                    nh = gv.agnxtnode(self.handle, nh)
                except StopIteration:
                    return
        elif nbunch in self:  # if nbunch is a single node
            n = Node(self, nbunch)
            nh = n.handle
            eh = gv.agfstin(self.handle, nh)
            while eh is not None:
                e = Edge(self, eh=eh)
                if keys:
                    yield (e[0], e[1], e.name)
                else:
                    yield e
                try:
                    eh = gv.agnxtin(self.handle, eh)
                except StopIteration:
                    break
        else:  # if nbunch is a sequence of nodes
            try:
                bunch = [n for n in nbunch if n in self]
            except TypeError:
                raise TypeError("nbunch is not a node or a sequence of nodes.")
            for n in nbunch:
                try:
                    nh = Node(self, n).handle
                except KeyError:
                    continue
                eh = gv.agfstin(self.handle, nh)
                while eh is not None:
                    e = Edge(self, eh=eh)
                    if keys:
                        yield (e[0], e[1], e.name)
                    else:
                        yield e
                    try:
                        eh = gv.agnxtin(self.handle, eh)
                    except StopIteration:
                        break

    def edges_iter(self, nbunch=None, keys=False):
        """Return iterator over edges in the graph.

        If the optional nbunch (container of nodes) only edges
        adjacent to nodes in nbunch will be returned.

        Note: modifying the graph structure while iterating over
        edges may produce unpredictable results.  Use edges()
        as an alternative.
        """
        if nbunch is None:  # all nodes
            for e in self.out_edges_iter(keys=keys):
                yield e
        elif nbunch in self:  # only one node
            for e in self.out_edges_iter(nbunch, keys=keys):
                yield e
            for e in self.in_edges_iter(nbunch, keys=keys):
                if e != (nbunch, nbunch):
                    yield e
        else:  # a group of nodes
            used = set()
            for e in self.out_edges_iter(nbunch, keys=keys):
                yield e
                used.add(e)
            for e in self.in_edges_iter(nbunch, keys=keys):
                if e not in used:
                    yield e

    iterinedges = in_edges_iter

    iteredges = edges_iter

    def out_edges(self, nbunch=None, keys=False):
        """Return list of out edges in the graph.

        If the optional nbunch (container of nodes) only out edges
        adjacent to nodes in nbunch will be returned.
        """
        return list(self.out_edges_iter(nbunch=nbunch, keys=keys))

    def in_edges(self, nbunch=None, keys=False):
        """Return list of in edges in the graph.
        If the optional nbunch (container of nodes) only in edges
        adjacent to nodes in nbunch will be returned.
        """
        return list(self.in_edges_iter(nbunch=nbunch, keys=keys))

    def predecessors_iter(self, n):
        """Return iterator over predecessor nodes of n.

        Note: modifying the graph structure while iterating over
        node predecessors may produce unpredictable results.  Use
        predecessors() as an alternative.
        """
        n = Node(self, n)
        nh = n.handle
        eh = gv.agfstin(self.handle, nh)
        while eh is not None:
            (s, t) = Edge(self, eh=eh)
            if s == n:
                yield Node(self, t)
            else:
                yield Node(self, s)
            try:
                eh = gv.agnxtin(self.handle, eh)
            except StopIteration:
                return

    iterpred = predecessors_iter

    def successors_iter(self, n):
        """Return iterator over successor nodes of n.

        Note: modifying the graph structure while iterating over
        node successors may produce unpredictable results.  Use
        successors() as an alternative.
        """
        n = Node(self, n)
        nh = n.handle
        eh = gv.agfstout(self.handle, nh)
        while eh is not None:
            (s, t) = Edge(self, eh=eh)
            if s == n:
                yield Node(self, t)
            else:
                yield Node(self, s)
            try:
                eh = gv.agnxtout(self.handle, eh)
            except StopIteration:
                return

    itersucc = successors_iter

    def successors(self, n):
        """Return list of successor nodes of n."""
        return list(self.successors_iter(n))

    def predecessors(self, n):
        """Return list of predecessor nodes of n."""
        return list(self.predecessors_iter(n))

    # digraph definitions
    out_neighbors = successors
    in_neighbors = predecessors

    def degree_iter(self, nbunch=None, indeg=True, outdeg=True):
        """Return an iterator over the degree of the nodes given in
        nbunch container.

        Returns paris of (node,degree).
        """
        # prepare nbunch
        if nbunch is None:  # include all nodes via iterator
            bunch = [n for n in self.nodes_iter()]
        elif nbunch in self:  # if nbunch is a single node
            bunch = [Node(self, nbunch)]
        else:  # if nbunch is a sequence of nodes
            try:
                bunch = [Node(self, n) for n in nbunch if n in self]
            except TypeError:
                raise TypeError("nbunch is not a node or a sequence of nodes.")
        for n in bunch:
            yield (Node(self, n), gv.agdegree(self.handle, n.handle, indeg, outdeg))

    def in_degree_iter(self, nbunch=None):
        """Return an iterator over the in-degree of the nodes given in
        nbunch container.

        Returns paris of (node,degree).
        """
        return self.degree_iter(nbunch, indeg=True, outdeg=False)

    def out_degree_iter(self, nbunch=None):
        """Return an iterator over the out-degree of the nodes given in
        nbunch container.

        Returns paris of (node,degree).

        """
        return self.degree_iter(nbunch, indeg=False, outdeg=True)

    iteroutdegree = out_degree_iter
    iterindegree = in_degree_iter

    def out_degree(self, nbunch=None, with_labels=False):
        """Return the out-degree of nodes given in nbunch container.

        Using optional with_labels=True returns a dictionary
        keyed by node with value set to the degree.
        """
        if with_labels:
            return dict(self.out_degree_iter(nbunch))
        else:
            dlist = list(d for n, d in self.out_degree_iter(nbunch))
            if nbunch in self:
                return dlist[0]
            else:
                return dlist

    def in_degree(self, nbunch=None, with_labels=False):
        """Return the in-degree of nodes given in nbunch container.

        Using optional with_labels=True returns a dictionary
        keyed by node with value set to the degree.
        """

        if with_labels:
            return dict(self.in_degree_iter(nbunch))
        else:
            dlist = list(d for n, d in self.in_degree_iter(nbunch))
            if nbunch in self:
                return dlist[0]
            else:
                return dlist

    def reverse(self):
        """Return copy of directed graph with edge directions reversed."""
        if self.directed:
            # new empty DiGraph
            H = self.__class__(strict=self.strict, directed=True, name=self.name)
            H.graph_attr.update(self.graph_attr)
            H.node_attr.update(self.node_attr)
            H.edge_attr.update(self.edge_attr)
            for n in self.nodes():
                H.add_node(n)
                new_n = Node(H, n)
                new_n.attr.update(n.attr)
            for e in self.edges():
                (u, v) = e
                H.add_edge(v, u)
                uv = H.get_edge(v, u)
                uv.attr.update(e.attr)
            return H
        else:
            return self

    def degree(self, nbunch=None, with_labels=False):
        """Return the degree of nodes given in nbunch container.

        Using optional with_labels=True returns a dictionary
        keyed by node with value set to the degree.

        """
        if with_labels:
            return dict(self.degree_iter(nbunch))
        else:
            dlist = list(d for n, d in self.degree_iter(nbunch))
            if nbunch in self:
                return dlist[0]
            else:
                return dlist

    iterdegree = degree_iter

    def number_of_edges(self):
        """Return the number of edges in the graph."""
        return gv.agnedges(self.handle)

    def clear(self):
        """Remove all nodes, edges, and attributes from the graph."""
        self.remove_edges_from(self.edges())
        self.remove_nodes_from(self.nodes())
        # now "close" existing graph and create a new graph
        name = gv.agnameof(self.handle)
        strict = self.strict
        directed = self.directed
        self._close_handle()
        self.handle = gv.agraphnew(name, strict, directed)
        self._owns_handle = True
        self._update_handle_references()

    def close(self):
        self._close_handle()

    def _close_handle(self):
        # may be useful to clean up graphviz data
        # this should completely remove all of the existing graphviz data
        if self._owns_handle:
            if self.handle is not None:
                gv.agclose(self.handle)
                self.handle = None
            self._owns_handle = False
        else:
            self.handle = None

    def copy(self):
        """Return a copy of the graph."""
        from tempfile import TemporaryFile

        fh = TemporaryFile()
        # Cover TemporaryFile wart: on 'nt' we need the file member
        if hasattr(fh, "file"):
            fhandle = fh.file
        else:
            fhandle = fh

        self.write(fhandle)
        fh.seek(0)

        return self.__class__(filename=fhandle)

    def add_path(self, nlist):
        """Add the path of nodes given in nlist."""
        fromv = nlist.pop(0)
        while len(nlist) > 0:
            tov = nlist.pop(0)
            self.add_edge(fromv, tov)
            fromv = tov

    def add_cycle(self, nlist):
        """Add the cycle of nodes given in nlist."""
        self.add_path(nlist + [nlist[0]])

    def prepare_nbunch(self, nbunch=None):
        # private function to build bunch from nbunch
        if nbunch is None:  # include all nodes via iterator
            bunch = self.nodes_iter()
        elif nbunch in self:  # if nbunch is a single node
            bunch = [Node(self, nbunch)]
        else:  # if nbunch is a sequence of nodes
            try:  # capture error for nonsequence/iterator entries.
                bunch = [Node(self, n) for n in nbunch if n in self]
                # bunch=(n for n in nbunch if n in self) # need python 2.4
            except TypeError:
                raise TypeError("nbunch is not a node or a sequence of nodes.")
        return bunch

    def add_subgraph(self, nbunch=None, name=None, **attr):
        """Return subgraph induced by nodes in nbunch.
        """
        if name is not None:
            name = name.encode(self.encoding)
        try:
            handle = gv.agsubg(self.handle, name, _Action.create)
        except TypeError:
            raise TypeError(
                "Subgraph name must be a string: %s" % name.decode(self.encoding)
            )

        H = self.__class__(
            strict=self.strict, directed=self.directed, handle=handle, name=name, **attr
        )
        if nbunch is None:
            return H
        # add induced subgraph on nodes in nbunch
        bunch = self.prepare_nbunch(nbunch)
        for n in bunch:
            node = Node(self, n)
            nh = gv.agsubnode(handle, node.handle, _Action.create)
        for (u, v, k) in self.edges(keys=True):
            if u in H and v in H:
                edge = Edge(self, u, v, k)
                eh = gv.agsubedge(handle, edge.handle, _Action.create)

        return H

    def remove_subgraph(self, name):
        """Remove subgraph with given name."""
        try:
            handle = gv.agsubg(self.handle, name.encode(self.encoding), _Action.find)
        except TypeError:
            raise TypeError("Subgraph name must be a string: %s" % name)
        if handle is None:
            raise KeyError("Subgraph %s not in graph." % name)
        gv.agdelsubg(self.handle, handle)

    delete_subgraph = remove_subgraph

    subgraph = add_subgraph

    def subgraph_parent(self, nbunch=None, name=None):
        """Return parent graph of subgraph or None if graph is root graph.
        """
        handle = gv.agparent(self.handle)
        if handle is None:
            return None
        H = self.__class__(
            strict=self.strict, directed=self.directed, handle=handle, name=name
        )
        return H

    def subgraph_root(self, nbunch=None, name=None):
        """Return root graph of subgraph or None if graph is root graph.
        """
        handle = gv.agroot(self.handle)
        if handle is None:
            return None
        H = self.__class__(
            strict=self.strict, directed=self.directed, handle=handle, name=name
        )
        return H

    def get_subgraph(self, name):
        """Return existing subgraph with specified name or None if it
        doesn't exist.
        """
        try:
            handle = gv.agsubg(self.handle, name.encode(self.encoding), _Action.find)
        except TypeError:
            raise TypeError("Subgraph name must be a string: %s" % name)

        if handle is None:
            return None
        H = self.__class__(strict=self.strict, directed=self.directed, handle=handle)
        return H

    def subgraphs_iter(self):
        """Iterator over subgraphs."""
        handle = gv.agfstsubg(self.handle)
        while handle is not None:
            yield self.__class__(
                strict=self.strict, directed=self.directed, handle=handle
            )
            try:
                handle = gv.agnxtsubg(handle)
            except StopIteration:
                return

    def subgraphs(self):
        """Return a list of all subgraphs in the graph."""
        return list(self.subgraphs_iter())

    # directed, undirected tests and conversions

    def is_strict(self):
        """Return True if graph is strict or False if not.

        Strict graphs do not allow parallel edges or self loops.
        """
        if gv.agisstrict(self.handle) == 1:
            return True
        else:
            return False

    strict = property(is_strict)

    def is_directed(self):
        """Return True if graph is directed or False if not."""
        if gv.agisdirected(self.handle) == 1:
            return True
        else:
            return False

    directed = property(is_directed)

    def is_undirected(self):
        """Return True if graph is undirected or False if not."""
        if gv.agisundirected(self.handle) == 1:
            return True
        else:
            return False

    def to_undirected(self):
        """Return undirected copy of graph."""
        if not self.directed:
            return self.copy()
        else:
            U = AGraph(strict=self.strict)
            U.graph_attr.update(self.graph_attr)
            U.node_attr.update(self.node_attr)
            U.edge_attr.update(self.edge_attr)
            for n in self.nodes():
                U.add_node(n)
                new_n = Node(U, n)
                new_n.attr.update(n.attr)
            for e in self.edges():
                (u, v) = e
                U.add_edge(u, v)
                uv = U.get_edge(u, v)
                uv.attr.update(e.attr)
            return U

    def to_directed(self, **kwds):
        """Return directed copy of graph.

        Each undirected edge u-v is represented as two directed
        edges u->v and v->u.
        """
        if not self.directed:
            D = AGraph(strict=self.strict, directed=True)
            D.graph_attr.update(self.graph_attr)
            D.node_attr.update(self.node_attr)
            D.edge_attr.update(self.edge_attr)
            for n in self.nodes():
                D.add_node(n)
                new_n = Node(D, n)
                new_n.attr.update(n.attr)
            for e in self.edges():
                (u, v) = e
                D.add_edge(u, v)
                D.add_edge(v, u)
                uv = D.get_edge(u, v)
                vu = D.get_edge(v, u)
                uv.attr.update(e.attr)
                uv.attr.update(e.attr)
                vu.attr.update(e.attr)
            return D
        else:
            return self.copy()

    # io
    def read(self, path):
        """Read graph from dot format file on path.

        path can be a file name or file handle

        use::

           G.read('file.dot')

        """
        fh = self._get_fh(path)
        try:
            self._close_handle()
            try:
                self.handle = gv.agread(fh, None)
            except ValueError:
                raise DotError("Invalid Input")
            else:
                self._owns_handle = True
                self._update_handle_references()
        except OSError:
            print("IO error reading file")

    def write(self, path=None):
        """Write graph in dot format to file on path.

        path can be a file name or file handle

        use::

           G.write('file.dot')
        """
        if path is None:
            path = sys.stdout
        fh = self._get_fh(path, "w")
        try:
            gv.agwrite(self.handle, fh)
        except OSError:
            print("IO error writing file")
        finally:
            if hasattr(fh, "close") and not hasattr(path, "write"):
                fh.close()

    def string_nop(self):
        """Return a string (unicode) representation of graph in dot format."""
        # this will fail for graphviz-2.8 because of a broken nop
        # so use tempfile version below
        return self.draw(format="dot", prog="nop").decode(self.encoding)

    def to_string(self):
        """Return a string (unicode) representation of graph in dot format."""
        from tempfile import TemporaryFile

        fh = TemporaryFile()
        # Cover TemporaryFile wart: on 'nt' we need the file member
        if hasattr(fh, "file"):
            self.write(fh.file)
        else:
            self.write(fh)
        fh.seek(0)
        data = fh.read()
        fh.close()
        return data.decode(self.encoding)

    def string(self):
        """Return a string (unicode) representation of graph in dot format."""
        #        return self.to_string()
        return self.string_nop()

    def from_string(self, string):
        """Load a graph from a string in dot format.

        Overwrites any existing graph.

        To make a new graph from a string use

        >>> s='digraph {1 -> 2}'
        >>> A=AGraph()
        >>> t=A.from_string(s)
        >>> A=AGraph(string=s) # specify s is a string
        >>> A=AGraph(s)  # s assumed to be a string during initialization
        """
        # allow either unicode or encoded string
        try:
            string = string.decode(self.encoding)
        except (UnicodeEncodeError, AttributeError):
            pass
        from tempfile import TemporaryFile

        fh = TemporaryFile()
        fh.write(string.encode(self.encoding))
        fh.seek(0)
        # Cover TemporaryFile wart: on 'nt' we need the file member
        if hasattr(fh, "file"):
            self.read(fh.file)
        else:
            self.read(fh)
        fh.close()
        return self

    def _get_prog(self, prog):
        # private: get path of graphviz program
        progs = [
            "neato",
            "dot",
            "twopi",
            "circo",
            "fdp",
            "nop",
            "wc",
            "acyclic",
            "gvpr",
            "gvcolor",
            "ccomps",
            "sccmap",
            "tred",
            "sfdp",
            "unflatten",
        ]
        if prog not in progs:
            raise ValueError("Program %s is not one of: %s." % (prog, ", ".join(progs)))

        try:  # user must pick one of the graphviz programs...
            runprog = self._which(prog)
        except:
            raise ValueError("Program %s not found in path." % prog)

        return runprog

    def _run_prog(self, prog="nop", args=""):
        """Apply graphviz program to graph and return the result as a string.

        >>> A = AGraph()
        >>> s = A._run_prog() # doctest: +SKIP
        >>> s = A._run_prog(prog='acyclic') # doctest: +SKIP

        Use keyword args to add additional arguments to graphviz programs.
        """
        runprog = r'"%s"' % self._get_prog(prog)
        cmd = " ".join([runprog, args])
        dotargs = shlex.split(cmd)
        p = subprocess.Popen(
            dotargs,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=False,
        )
        (child_stdin, child_stdout, child_stderr) = (p.stdin, p.stdout, p.stderr)
        # Use threading to avoid blocking
        data = []
        errors = []
        threads = [PipeReader(data, child_stdout), PipeReader(errors, child_stderr)]
        for t in threads:
            t.start()

        self.write(child_stdin)
        child_stdin.close()

        for t in threads:
            t.join()
        p.wait()

        if not data:
            raise OSError(b"".join(errors).decode(self.encoding))

        if len(errors) > 0:
            warnings.warn(b"".join(errors).decode(self.encoding), RuntimeWarning)
        return b"".join(data)

    def unflatten(self, args=""):
        """Adjust directed graphs to improve layout aspect ratio.

        >>> A = AGraph()
        >>> A_unflattened = A.unflatten('-f -l 3')
        >>> A.unflatten('-f -l 1').layout()

        Use keyword args to add additional arguments to graphviz programs.
        """
        data = self._run_prog("unflatten", args)
        self.from_string(data)
        return self

    def layout(self, prog="neato", args=""):
        """Assign positions to nodes in graph.

        Optional prog=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
        will use specified graphviz layout method.

        >>> A=AGraph()
        >>> A.layout() # uses neato
        >>> A.layout(prog='dot')

        Use keyword args to add additional arguments to graphviz programs.

        The layout might take a long time on large graphs.

        """
        fmt = "dot"
        data = self._run_prog(prog, " ".join([args, "-T", fmt]))
        self.from_string(data)
        self.has_layout = True
        return

    def tred(self, args="", copy=False):
        """Transitive reduction of graph.  Modifies existing graph.

        To create a new graph use

        >>> A=AGraph()
        >>> B=A.tred(copy=True) # doctest: +SKIP

        See the graphviz "tred" program for details of the algorithm.
        """
        data = self._run_prog("tred", args)
        if copy:
            return self.__class__(string=data.decode(self.encoding))
        else:
            return self.from_string(data)

    def acyclic(self, args="", copy=False):
        """Reverse sufficient edges in digraph to make graph acyclic.
        Modifies existing graph.

        To create a new graph use

        >>> A=AGraph()
        >>> B=A.acyclic(copy=True) # doctest: +SKIP

        See the graphviz "acyclic" program for details of the algorithm.
        """
        data = self._run_prog("acyclic", args)
        if copy:
            return self.__class__(string=data.decode(self.encoding))
        else:
            return self.from_string(data)

    def draw(self, path=None, format=None, prog=None, args=""):
        """Output graph to path in specified format.

        An attempt will be made to guess the output format based on the file
        extension of `path`.  If that fails, then the `format` parameter will
        be used.

        Note, if `path` is a file object returned by a call to os.fdopen(),
        then the method for discovering the format will not work.  In such
        cases, one should explicitly set the `format` parameter; otherwise, it
        will default to 'dot'.

        Formats (not all may be available on every system depending on
        how Graphviz was built)

            'canon', 'cmap', 'cmapx', 'cmapx_np', 'dia', 'dot',
            'fig', 'gd', 'gd2', 'gif', 'hpgl', 'imap', 'imap_np',
            'ismap', 'jpe', 'jpeg', 'jpg', 'mif', 'mp', 'pcl', 'pdf',
            'pic', 'plain', 'plain-ext', 'png', 'ps', 'ps2', 'svg',
            'svgz', 'vml', 'vmlz', 'vrml', 'vtx', 'wbmp', 'xdot', 'xlib'


        If prog is not specified and the graph has positions
        (see layout()) then no additional graph positioning will
        be performed.

        Optional prog=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
        will use specified graphviz layout method.

        >>> G = AGraph()
        >>> G.layout()

        # use current node positions, output ps in 'file.ps'
        >>> G.draw('file.ps')

        # use dot to position, output png in 'file'
        >>> G.draw('file', format='png',prog='dot')

        # use keyword 'args' to pass additional arguments to graphviz
        >>> G.draw('test.ps',prog='twopi',args='-Gepsilon=1')

        The layout might take a long time on large graphs.

        """
        import os

        # try to guess format from extension
        if format is None and path is not None:
            p = path
            # in case we got a file handle get its name instead
            if not is_string_like(p):
                p = path.name
            format = os.path.splitext(p)[-1].lower()[1:]

        if format is None or format == "":
            format = "dot"

        if prog is None:
            if self.has_layout:
                prog = "neato"
                args += "-n2"
            else:
                raise AttributeError(
                    """Graph has no layout information, see layout() or specify prog=%s."""
                    % ("|".join(["neato", "dot", "twopi", "circo", "fdp", "nop"]))
                )

        else:
            if self.number_of_nodes() > 1000:
                sys.stderr.write(
                    "Warning: graph has %s nodes...layout may take a long time.\n"
                    % self.number_of_nodes()
                )

        if prog == "nop":  # nop takes no switches
            args = ""
        else:
            args = " ".join([args, "-T" + format])

        data = self._run_prog(prog, args)

        if path is not None:
            fh = self._get_fh(path, "w+b")
            fh.write(data)
            if is_string_like(path):
                fh.close()
            d = None
        else:
            d = data
        return d

    # some private helper functions

    def _get_fh(self, path, mode="r"):
        """ Return a file handle for given path.

        Path can be a string, pathlib.Path, or a file handle.
        Attempt to uncompress/compress files ending in '.gz' and '.bz2'.
        """
        import os

        if is_string_like(path):
            if path.endswith(".gz"):
                # import gzip
                # fh = gzip.open(path,mode=mode)  # doesn't return real fh
                fh = os.popen("gzcat " + path)  # probably not portable
            elif path.endswith(".bz2"):
                # import bz2
                # fh = bz2.BZ2File(path,mode=mode) # doesn't return real fh
                fh = os.popen("bzcat " + path)  # probably not portable
            else:
                fh = open(path, mode=mode)
        elif hasattr(path, "write"):
            # Note, mode of file handle is unchanged.
            fh = path
        elif hasattr(path, "open"):
            fh = path.open(mode=mode)
        else:
            raise TypeError("path must be a string, path, or file handle.")
        return fh

    def _which(self, name):
        """Searches for name in exec path and returns full path"""
        import os
        import glob

        paths = os.environ["PATH"]
        if os.name == "nt":
            exe = ".exe"
        else:
            exe = ""
        for path in paths.split(os.pathsep):
            match = glob.glob(os.path.join(path, name + exe))
            if match:
                return match[0]
        raise ValueError("No prog %s in path." % name)

    def _update_handle_references(self):
        try:
            self.graph_attr.handle = self.handle
            self.node_attr.handle = self.handle
            self.edge_attr.handle = self.handle
        except AttributeError:
            pass  # ignore as likely still in __init__()


class Node(_TEXT_TYPE):
    """Node object based on unicode.

    If G is a graph

    >>> G=AGraph()

    then

    >>> G.add_node(1)

    will create a node object labeled by the string "1".

    To get the object use

    >>> node=Node(G,1)

    or
    >>> node=G.get_node(1)

    The node object is derived from a string and can be manipulated as such.

    Each node has attributes that can be directly accessed through
    the attr dictionary:

    >>> node.attr['color']='red'

    """

    def __new__(self, graph, name=None, nh=None):
        if nh is not None:
            n = super().__new__(self, gv.agnameof(nh), graph.encoding)
        else:
            n = super().__new__(self, name)
            try:
                nh = gv.agnode(graph.handle, n.encode(graph.encoding), _Action.find)
            except KeyError:
                raise KeyError("Node %s not in graph." % n)

        n.ghandle = graph.handle
        n.attr = ItemAttribute(nh, 1)
        n.handle = nh
        n.encoding = graph.encoding
        return n

    def get_handle(self):
        """Return pointer to graphviz node object."""
        return gv.agnode(self.ghandle, self.encode(self.encoding), _Action.find)

    #    handle=property(get_handle)

    def get_name(self):
        name = gv.agnameof(self.handle)
        if name is not None:
            name = name.decode(self.encoding)
        return name

    name = property(get_name)


class Edge(tuple):
    """Edge object based on tuple.

    If G is a graph

    >>> G=AGraph()

    then

    >>> G.add_edge(1,2)

    will add the edge 1-2 to the graph.

    >>> edge=Edge(G,1,2)

    or
    >>> edge=G.get_edge(1,2)

    will get the edge object.

    An optional key can be used

    >>> G.add_edge(2,3,'spam')
    >>> edge=Edge(G,2,3,'spam')

    The edge is represented as a tuple (u,v) or (u,v,key)
    and can be manipulated as such.

    Each edge has attributes that can be directly accessed through
    the attr dictionary:

    >>> edge.attr['color']='red'

    """

    def __new__(self, graph, source=None, target=None, key=None, eh=None):
        # edge handle given, reconstruct node object
        if eh is not None:
            (source, target) = (gv.agtail(eh), gv.aghead(eh))
            s = Node(graph, nh=source)
            t = Node(graph, nh=target)
        # no edge handle, search for edge and construct object
        else:
            s = Node(graph, source)
            t = Node(graph, target)
            if key is not None:
                if not is_string_like(key):
                    key = str(key)
                key = key.encode(graph.encoding)
            try:
                eh = gv.agedge(graph.handle, s.handle, t.handle, key, _Action.find)
            except KeyError:
                raise KeyError(f"Edge {source}-{target} not in graph.")

        tp = tuple.__new__(self, (s, t))
        tp.ghandle = graph.handle
        tp.handle = eh
        tp.attr = ItemAttribute(eh, 3)
        tp.encoding = graph.encoding
        return tp

    def get_name(self):
        name = gv.agnameof(self.handle)
        if name is not None:
            name = name.decode(self.encoding)
        return name

    name = property(get_name)
    key = property(get_name)


class Attribute(MutableMapping):
    """Default attributes for graphs.

    Assigned on initialization of AGraph class.
    and manipulated through the class data.

    >>> G=AGraph() # initialize, G.graph_attr, G.node_attr, G.edge_attr
    >>> G.graph_attr['splines']='true'
    >>> G.node_attr['shape']='circle'
    >>> G.edge_attr['color']='red'

    See
    http://graphviz.org/doc/info/attrs.html
    for a list of all attributes.

    """

    # use for graph, node, and edge default attributes
    # atype:graph=0, node=1,edge=3
    def __init__(self, handle, atype):
        self.handle = handle
        self.type = atype
        # get the encoding
        ghandle = gv.agraphof(handle)
        root_handle = gv.agroot(ghandle)  # get root graph
        try:
            item = gv.agattrdefval(gv.agattr(root_handle, 0, b"charset", None))
            self.encoding = item if type(item) is not bytes else item.decode("utf-8")
        except KeyError:
            self.encoding = _DEFAULT_ENCODING

    def __setitem__(self, name, value):
        if name == "charset" and self.type == 0:
            raise ValueError("Graph charset is immutable!")
        if not is_string_like(value):
            value = str(value)
        ghandle = gv.agroot(self.handle)  # get root graph
        if ghandle == self.handle:
            gv.agattr_label(
                self.handle,
                self.type,
                name.encode(self.encoding),
                value.encode(self.encoding),
            )
        else:
            gv.agsafeset_label(
                ghandle,
                self.handle,
                name.encode(self.encoding),
                value.encode(self.encoding),
                b"",
            )

    def __getitem__(self, name):
        item = gv.agget(self.handle, name.encode(self.encoding))
        if item is None:
            ah = gv.agattr(self.handle, self.type, name.encode(self.encoding), None)
            item = gv.agattrdefval(ah)
        return item.decode(self.encoding)

    def __delitem__(self, name):
        gv.agattr(self.handle, self.type, name.encode(self.encoding), b"")

    def __contains__(self, name):
        try:
            self.__getitem__(name)
            return True
        except:
            return False

    def __len__(self):
        return len(list(self.__iter__()))

    def has_key(self, name):
        return self.__contains__(name)

    def keys(self):
        return list(self.__iter__())

    def __iter__(self):
        for (k, v) in self.iteritems():
            yield k

    def iteritems(self):
        ah = None
        while True:
            try:
                ah = gv.agnxtattr(self.handle, self.type, ah)
                yield (
                    gv.agattrname(ah).decode(self.encoding),
                    gv.agattrdefval(ah).decode(self.encoding),
                )
            except KeyError:  # gv.agattrdefval returned KeyError, skip
                continue
            except StopIteration:  # gv.agnxtattr is done, as are we
                return


class ItemAttribute(Attribute):
    """Attributes for individual nodes and edges.

    Assigned on initialization of Node or Edge classes
    and manipulated through the class data.

    >>> G=AGraph()
    >>> G.add_edge('a','b')
    >>> n=Node(G,'a')
    >>> n.attr['shape']='circle'
    >>> e=Edge(G,'a','b')
    >>> e.attr['color']='red'

    See
    http://graphviz.org/doc/info/attrs.html
    for a list of all attributes.
    """

    # use for individual item attributes - either a node or an edge
    # graphs and default node and edge attributes use Attribute
    def __init__(self, handle, atype):
        self.handle = handle
        self.type = atype
        self.ghandle = gv.agraphof(handle)
        # get the encoding
        root_handle = gv.agroot(self.ghandle)  # get root graph
        try:
            item = gv.agattrdefval(gv.agattr(root_handle, 0, b"charset", None))
            self.encoding = item if type(item) is not bytes else item.decode("utf-8")
        except KeyError:
            self.encoding = _DEFAULT_ENCODING

    def __setitem__(self, name, value):
        if not is_string_like(value):
            value = str(value)
        if self.type == 1 and name == "label":
            default = "\\N"
        else:
            default = ""
        gv.agsafeset_label(
            self.ghandle,
            self.handle,
            name.encode(self.encoding),
            value.encode(self.encoding),
            default.encode(self.encoding),
        )

    def __getitem__(self, name):
        val = gv.agget(self.handle, name.encode(self.encoding))
        if val is not None:
            val = val.decode(self.encoding)
        return val

    def __delitem__(self, name):
        gv.agset(self.handle, name.encode(self.encoding), b"")

    def iteritems(self):
        ah = None
        while 1:
            try:
                ah = gv.agnxtattr(self.ghandle, self.type, ah)
                value = gv.agxget(self.handle, ah)
                try:
                    defval = gv.agattrdefval(ah)  # default value
                    if defval == value:
                        continue  # don't report default
                except:  # no default, gv.getattrdefval raised error
                    pass
                    # unique value for this edge
                yield (
                    gv.agattrname(ah).decode(self.encoding),
                    value.decode(self.encoding),
                )
            except KeyError:  # gv.agxget returned KeyError, skip
                continue
            except StopIteration:  # gv.agnxtattr is done, as are we
                return


def _test_suite():
    import doctest

    suite = doctest.DocFileSuite(
        "tests/graph.txt",
        "tests/attributes.txt",
        "tests/layout_draw.txt",
        "tests/subgraph.txt",
        package="pygraphviz",
    )
    doctest.testmod()  # test docstrings in module
    return suite


if __name__ == "__main__":
    import os
    import sys
    import unittest

    if sys.version_info[:2] < (3, 6):
        print(
            "Python version 3.6 or later required for tests (%d.%d detected)."
            % sys.version_info[:2]
        )
        sys.exit(-1)
        # directory of package (relative to this)
    nxbase = sys.path[0] + os.sep + os.pardir
    sys.path.insert(0, nxbase)  # prepend to search path
    unittest.TextTestRunner().run(_test_suite())
