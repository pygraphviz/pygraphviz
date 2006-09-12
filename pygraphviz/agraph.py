# -*- coding: utf-8 -*-
"""
A Python interface to Graphviz.  

"""
#    Copyright (C) 2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

import graphviz as gv
import UserDict
import sys

class _Action:
    find, create = 0,1

class AGraph(object):
    """
    Class for Graphviz agraph type.

    Example use::
         
      >>> G=AGraph()         
      >>> G=AGraph(directed=True)

      G=AGraph("file.dot")   

    
    """
    def __init__(self, file=None, name=None,
                 data=None, strict=True, directed=False,
                 handle=None):

        if handle is None:
            # the graph pointer (handle)
            self.handle=gv.agraphnew(name,strict,directed)  
        else:
            self.handle=handle
        if file is not None:
            self.read(file)

        if data is not None: # dict of dicts or dict of lists
            for node in data:
                for nbr in data[node]:
                    self.add_edge(node,nbr)
            self.add_nodes_from(data.keys())        

        self.graph_attr=Attribute(self.handle,0) # default graph attributes
        self.node_attr=Attribute(self.handle,1)  # default node attributes
        self.edge_attr=Attribute(self.handle,2)  # default edge attribtes


    def __str__(self):
        # print the name of the graph, see string() for dot representation
        name=gv.agnameof(self.handle)
        if name is None:
            return ""
        else:
            return name

    def __repr__(self):
        # display the dot format of the graph
        # if it is too long, truncate to fit screen
        s=self.string().splitlines()
        if len(s)>15:
            return "\n".join(s[:7]+["\n\t.......\n"]+s[-7:])
        else:
            return "\n".join(s)

    def __eq__(self,other):
        # two graphs are equal if they have exact same string representation
        # this is not graph isomorphism
        return self.string()==other.string()

    def __iter__(self):
        # provide "for n in G"
        return self.nodes_iter()

    def __contains__(self,n):
        # provide "n in G"
        return self.has_node(n)
        
    def __len__(self):
        return self.number_of_nodes()

    def __getitem__(self,n):
        # "G[n]" returns nodes attached to n
        return self.neighbors(n)

# not implemented, but could be...
#    def __setitem__(self,u,v):
#        self.add_edge(u,v)

    def add_node(self, n):
        """Add a single node n to the graph.

        If n is not a string, conversion to a string will be attempted.
        String conversion will work if n has valid string representation
        (try str(n) if you are unsure).

        >>> G=AGraph()
        >>> G.add_node('a')
        >>> G.nodes()
        ['a']
        >>> G.add_node(1) # will be converted to a string
        >>> G.nodes()
        ['a', '1']
        
        """
        if not self._is_string_like(n):  n=str(n)
        try:
            nh=gv.agnode(self.handle,n,_Action.find)
        except KeyError:
            nh=gv.agnode(self.handle,n,_Action.create)

    def add_nodes_from(self, nbunch):
        """Add nodes to graph from a container nbunch.

        nbunch can be any iterable container such as a list or dictionary

        >>> G=AGraph()
        >>> nlist=['a','b',1,'spam']
        >>> G.add_nodes_from(nlist)
        >>> sorted(G.nodes())
        ['1', 'a', 'b', 'spam']
        
        """
        for n in nbunch:
            self.add_node(n)

    def delete_node(self,n):
        """Delete the single node n from graph.

        Attempting to delete a node that isn't in the graph will produce
        an error.
        
        >>> G=AGraph()
        >>> G.add_node('a')
        >>> G.delete_node('a')

        """
        if not self._is_string_like(n):  n=str(n)
        try:
            nh=gv.agnode(self.handle,n,_Action.find)
            gv.agdelnode(nh)
        except KeyError:
            raise KeyError("node %s not in graph"%n)

    def delete_nodes_from(self,nbunch):
        """Delete nodes in graph from a container nbunch.

        nbunch can be any iterable container such as a list or dictionary

        >>> G=AGraph()
        >>> nlist=['a','b',1,'spam']
        >>> G.add_nodes_from(nlist)
        >>> G.delete_nodes_from(nlist)
        """
        for n in nbunch: 
            self.delete_node(n)

    def nodes_iter(self):
        """Return an iterator over all the nodes in the graph."""
        nh=gv.agfstnode(self.handle)
        while nh is not None:
            yield Node(self,gv.agnameof(nh))
            nh=gv.agnxtnode(nh)
        raise StopIteration

    iternodes=nodes_iter

    def nodes(self):
        """Return a list of all nodes in the graph."""
        return list(self.nodes_iter())

    def number_of_nodes(self):
        """Return the number of nodes in the graph."""
        return gv.agnnodes(self.handle)

    def order(self):
        """Return the number of nodes in the graph."""
        return self.number_of_nodes()

    def has_node(self,n):
        """Return True if n is in the graph or False if not.

        >>> G=AGraph()
        >>> G.add_node('a')
        >>> G.has_node('a')
        True
        >>> 'a' in G  # same as G.has_node('a')
        True

        """
        try:
            node=Node(self,n)
            return True
        except KeyError:
            return False

    def get_node(self,n):
        """Return a node object (Node) corresponding to node n.

        >>> G=AGraph()
        >>> G.add_node('a')
        >>> node=G.get_node('a')
        >>> print node
        a
        """
        return Node(self,n)

    def add_edge(self,u,v=None,key=None):  
        """Add a single edge between nodes u and v to the graph.

        If u and v are not nodes in they graph they will added.

        If u and v is not a strings, conversion to a string will be attempted.
        String conversion will work if u and v have valid string representation
        (try e.g. str(u) if you are unsure).
        
        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.edges()
        [('a', 'b')]

        The optional key argument allows assignment of a key to the
        edge.  This is especially useful to distinguish between
        parallel edges in multi-edge graphs (strict=False).

        >>> G=AGraph(strict=False)
        >>> G.add_edge('a','b','first')
        >>> G.add_edge('a','b','second')
        >>> sorted(G.edges())
        [('a', 'b', 'first'), ('a', 'b', 'second')]

        """
        if v is None: (u,v)=u  # no v given, assume u is an edge tuple
        try:
            uh=Node(self,u).get_handle()
        except:
            self.add_node(u)
            uh=Node(self,u).get_handle()
        try:
            vh=Node(self,v).get_handle()
        except:
            self.add_node(v)
            vh=Node(self,v).get_handle()
        try:
            eh=gv.agedge(uh,vh,key,_Action.create)
        except KeyError:
            return None # silent failure for strict graph, already added

    def add_edges_from(self, ebunch):  
        """Add nodes to graph from a container ebunch.

        ebunch is a container of edges such as a list or dictionary.

        >>> G=AGraph()
        >>> elist=[('a','b'),('b','c')]
        >>> G.add_edges_from(elist)
        """
        for e in ebunch:
            self.add_edge(e)

    def get_edge(self, u, v, key=None):
        """Return an edge object (Edge) corresponding to edge (u,v).

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> edge=G.get_edge('a','b')
        >>> print edge
        ('a', 'b')

        With optional key argument will only get edge matching (u,v,key).

        """
        return Edge(self,u,v,key)


    def delete_edge(self, u, v=None, key=None):
        """Delete edge between nodes u and v from the graph.

        With optional key argument  will only delete an edge
        matching (u,v,key).

        """
        if v is None: (u,v)=u  # no v given, assume u is an edge tuple
        e=Edge(self,u,v,key)
        try:
            gv.agdeledge(e.get_handle())
        except KeyError:
            raise KeyError("edge %s-%s not in graph"%(u,v))

    def delete_edges_from(self, ebunch): 
        """Delete edges from ebunch (a container of edges)."""
        for e in ebunch:
            self.delete_edge(e)

    def has_edge(self, u, v=None, key=None):
        """Return True an edge u-v is in the graph or False if not.

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.has_edge('a','b')
        True
        
        Optional key argument will restrict match to edges (u,v,key).

        """

        if v is None: (u,v)=u  # no v given, assume u is an edge tuple
        try:
            Edge(self,u,v,key)
            return True
        except KeyError:
            return False

    def edges_iter(self, nbunch=None):
        """Return iterator over edges in the graph.

        If the optional nbunch (container of nodes) only edges
        adjacent to nodes in nbunch will be returned.
        """

        if nbunch is None:   # all nodes
            nh=gv.agfstnode(self.handle)
            while nh is not None:
                eh=gv.agfstout(nh)
                while eh is not None:
                    (s,t)=(gv.agtail(eh),gv.aghead(eh))
                    (u,v)=(gv.agnameof(s),gv.agnameof(t))
                    key=gv.agnameof(eh)
                    yield Edge(self,u,v,key)
                    eh=gv.agnxtout(eh)
                nh=gv.agnxtnode(nh)
        elif nbunch in self: # if nbunch is a single node 
            n=Node(self,nbunch)
            nh=n.get_handle()
            eh=gv.agfstedge(nh)
            while eh is not None:
                (s,t)=(gv.agtail(eh),gv.aghead(eh))
                (u,v)=(gv.agnameof(s),gv.agnameof(t))
                yield Edge(self,u,v,gv.agnameof(eh))
                eh=gv.agnxtedge(eh,nh)
        else:                # if nbunch is a sequence of nodes
            try: bunch=[n for n in nbunch if n in self]
            except TypeError:
                raise TypeError(
                      "nbunch is not a node or a sequence of nodes")
            for n in nbunch:
                try: 
                    nh=Node(self,n).get_handle()
                except KeyError:
                    continue
                eh=gv.agfstout(nh)
                while eh is not None:
                    (s,t)=(gv.agtail(eh),gv.aghead(eh))
                    (u,v)=(gv.agnameof(s),gv.agnameof(t))
                    yield Edge(self,u,v,gv.agnameof(eh))
                    eh=gv.agnxtout(eh)
        raise StopIteration
 
    iteredges=edges_iter

    def edges(self, nbunch=None):
        """Return list of edges in the graph.

        If the optional nbunch (container of nodes) only edges
        adjacent to nodes in nbunch will be returned.
        
        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.add_edge('c','d')
        >>> print sorted(G.edges())
        [('a', 'b'), ('c', 'd')]
        >>> print G.edges('a')
        [('a', 'b')]
        """
        return list(self.edges_iter(nbunch))

    def has_neighbor(self, u, v, key=None):
        """Return True if u has an edge to v or False if not.

        >>> G=AGraph()
        >>> G.add_edge('a','b')
        >>> G.has_neighbor('a','b')
        True

        Optional key argument will only find edges (u,v,key).
        """
        return self.has_edge(u,v)


    def neighbors_iter(self,n):
        """Return iterator over the nodes attached to n."""
        n=Node(self,n)
        nh=n.get_handle()
        eh=gv.agfstedge(nh)
        while eh is not None:
            (s,t)=(gv.agtail(eh),gv.aghead(eh))
            (u,v)=(gv.agnameof(s),gv.agnameof(t))
            if u==n:
                yield Node(self,v)
            else:
                yield Node(self,u)
            eh=gv.agnxtedge(eh,nh)
        raise StopIteration

    def neighbors(self, n):
        """Return a list of the nodes attached to n."""
        return list(self.neighbors_iter(n))

    iterneighbors=neighbors_iter

    def out_edges_iter(self, nbunch=None):
        """Return iterator over out edges in the graph.

        If the optional nbunch (container of nodes) only out edges
        adjacent to nodes in nbunch will be returned.
        """
        if nbunch is None:   # all nodes
            nh=gv.agfstnode(self.handle)
            while nh is not None:
                eh=gv.agfstout(nh)
                while eh is not None:
                    (s,t)=(gv.agtail(eh),gv.aghead(eh))
                    (u,v)=(gv.agnameof(s),gv.agnameof(t))
                    yield Edge(self,u,v,gv.agnameof(eh))
                    eh=gv.agnxtout(eh)
                nh=gv.agnxtnode(nh)
        elif nbunch in self: # if nbunch is a single node 
            n=Node(self,nbunch)
            nh=n.get_handle()
            eh=gv.agfstout(nh)
            while eh is not None:
                (s,t)=(gv.agtail(eh),gv.aghead(eh))
                (u,v)=(gv.agnameof(s),gv.agnameof(t))
                yield Edge(self,u,v,gv.agnameof(eh))
                eh=gv.agnxtout(eh)
        else:                # if nbunch is a sequence of nodes
            try: bunch=[n for n in nbunch if n in self]
            except TypeError:
                raise TypeError(
                      "nbunch is not a node or a sequence of nodes")
            for n in nbunch:
                try: 
                    nh=Node(self,n).get_handle()
                except KeyError:
                    continue
                eh=gv.agfstout(nh)
                while eh is not None:
                    (s,t)=(gv.agtail(eh),gv.aghead(eh))
                    (u,v)=(gv.agnameof(s),gv.agnameof(t))
                    yield Edge(self,u,v,gv.agnameof(eh))
                    eh=gv.agnxtout(eh)
        raise StopIteration
 

    iteroutedges=out_edges_iter

    def in_edges_iter(self, nbunch=None):
        """Return iterator over out edges in the graph.

        If the optional nbunch (container of nodes) only out edges
        adjacent to nodes in nbunch will be returned.
        """
        if nbunch is None:   # all nodes
            nh=gv.agfstnode(self.handle)
            while nh is not None:
                eh=gv.agfstin(nh)
                while eh is not None:
                    (s,t)=(gv.agtail(eh),gv.aghead(eh))
                    (u,v)=(gv.agnameof(s),gv.agnameof(t))
                    yield Edge(self,u,v,gv.agnameof(eh))
                    eh=gv.agnxtin(eh)
                nh=gv.agnxtnode(nh)
        elif nbunch in self: # if nbunch is a single node 
            n=Node(self,nbunch)
            nh=n.get_handle()
            eh=gv.agfstin(nh)
            while eh is not None:
                (s,t)=(gv.agtail(eh),gv.aghead(eh))
                (u,v)=(gv.agnameof(s),gv.agnameof(t))
                yield Edge(self,u,v,gv.agnameof(eh))
                eh=gv.agnxtin(eh)
        else:                # if nbunch is a sequence of nodes
            try: bunch=[n for n in nbunch if n in self]
            except TypeError:
                raise TypeError(
                      "nbunch is not a node or a sequence of nodes")
            for n in nbunch:
                try: 
                    nh=Node(self,n).get_handle()
                except KeyError:
                    continue
                eh=gv.agfstin(nh)
                while eh is not None:
                    (s,t)=(gv.agtail(eh),gv.aghead(eh))
                    (u,v)=(gv.agnameof(s),gv.agnameof(t))
                    yield Edge(self,u,v,gv.agnameof(eh))
                    eh=gv.agnxtin(eh)
        raise StopIteration


    iterinedges=in_edges_iter

    # define edges to be out_edges implicitly since edges uses edges_iter
    edges_iter=out_edges_iter
            
    def out_edges(self, nbunch=None):
        """Return list of out edges in the graph.

        If the optional nbunch (container of nodes) only out edges
        adjacent to nodes in nbunch will be returned.
        """
        return list(self.out_edges_iter(nbunch))

    def in_edges(self, nbunch=None):
        """Return list of in edges in the graph.
        If the optional nbunch (container of nodes) only in edges
        adjacent to nodes in nbunch will be returned.
        """
        return list(self.in_edges_iter(nbunch))


    def predecessors_iter(self,n):
        """Return iterator over predecessor nodes of n."""
        n=Node(self,n)
        nh=n.get_handle()
        eh=gv.agfstin(nh)
        while eh is not None:
            (s,t)=(gv.agtail(eh),gv.aghead(eh))
            (u,v)=(gv.agnameof(s),gv.agnameof(t))
            if u==n:
                yield Node(self,v)
            else:
                yield Node(self,u)
            eh=gv.agnxtin(eh)
        raise StopIteration


    iterpred=predecessors_iter

    def successors_iter(self,n):
        """Return iterator over successor nodes of n."""
        n=Node(self,n)
        nh=n.get_handle()
        eh=gv.agfstout(nh)
        while eh is not None:
            (s,t)=(gv.agtail(eh),gv.aghead(eh))
            (u,v)=(gv.agnameof(s),gv.agnameof(t))
            if u==n:
                yield Node(self,v)
            else:
                yield Node(self,u)
            eh=gv.agnxtout(eh)
        raise StopIteration

    itersucc=successors_iter

    def successors(self, n):
        """Return list of successor nodes of n."""
        return list(self.successors_iter(n))


    def predecessors(self, n):
        """Return list of predecessor nodes of n."""
        return list(self.predecessors_iter(n))

    # digraph definintions 
    out_neighbors=successors
    in_neighbors=predecessors

    def degree_iter(self,nbunch=None,with_labels=False,indeg=True,outdeg=True):
        """Return an iterator over the degree of the nodes given in
        nbunch container.
        
        Using optional with_labels=True returns paris of (node,degree) .

        """
        # prepare nbunch
        if nbunch is None:   # include all nodes via iterator
            bunch=[n for n in self.nodes_iter()]
        elif nbunch in self: # if nbunch is a single node 
            bunch=[Node(self,nbunch)]
        else:                # if nbunch is a sequence of nodes
            try: bunch=[Node(self,n) for n in nbunch if n in self]
            except TypeError:
                raise TypeError("nbunch is not a node or a sequence of nodes")
        if with_labels:
            for n in bunch:
                yield (Node(self,n),gv.agdegree(n.get_handle(),indeg,outdeg))
        else:
            for n in bunch:
                yield gv.agdegree(n.get_handle(),indeg,outdeg)



    def in_degree_iter(self,nbunch=None,with_labels=False):
        """Return an iterator over the in-degree of the nodes given in
        nbunch container.
        
        Using optional with_labels=True returns paris of (node,degree) .

        """
        return self.degree_iter(nbunch,with_labels,indeg=True,outdeg=False)

    def out_degree_iter(self,nbunch=None,with_labels=False):
        """Return an iterator over the out-degree of the nodes given in
        nbunch container.
        
        Using optional with_labels=True returns paris of (node,degree) .

        """

        return self.degree_iter(nbunch,with_labels,indeg=False,outdeg=True)

    iteroutdegree=out_degree_iter
    iterindegree=in_degree_iter

    def out_degree(self,nbunch=None, with_labels=False):
        """Return the out-degree of nodes given in nbunch container.
        
        Using optional with_labels=True returns a dictionary
        keyed by node with value set to the degree.
        """
        if with_labels:
            return dict(self.out_degree_iter(nbunch,with_labels))
        else:
            dlist=list(self.out_degree_iter(nbunch,with_labels))
            if nbunch in self:
                return dlist[0]
            else:
                return dlist


    def in_degree(self,nbunch=None, with_labels=False):
        """Return the in-degree of nodes given in nbunch container.
        
        Using optional with_labels=True returns a dictionary
        keyed by node with value set to the degree.
        """

        if with_labels:
            return dict(self.in_degree_iter(nbunch,with_labels))
        else:
            dlist=list(self.in_degree_iter(nbunch,with_labels))
            if nbunch in self:
                return dlist[0]
            else:
                return dlist

        
    def reverse(self):
        """Return copy of directed graph with edge directions reversed."""
        if self.is_directed():
            # new empty DiGraph
            H=self.__class__(strict=self.is_strict(),directed=True) 
            H.add_nodes_from(self)
            H.add_edges_from([(v,u) for (u,v) in self.edges_iter()])
            return H
        else:
            return self


    def degree(self,nbunch=None,with_labels=False):
        """Return the degree of nodes given in nbunch container.
        
        Using optional with_labels=True returns a dictionary
        keyed by node with value set to the degree.

        """
        if with_labels:
            return dict(self.degree_iter(nbunch,with_labels))
        else:
            dlist=list(self.degree_iter(nbunch,with_labels))
            if nbunch in self:
                return dlist[0]
            else:
                return dlist

    iterdegree=degree_iter                
                
    def number_of_edges(self):
        """Return the number of edges in the graph."""
        return sum(self.degree())/2

    def size(self):
        """Return the number of edges in the graph."""
        return self.number_of_edges()


    def clear(self):
        """Remove all nodes, edges, and attributes from the graph."""
        for a in self.edge_attr:  del self.edge_attr[a]
        for a in self.node_attr:  del self.node_attr[a]
        for a in self.graph_attr: del self.graph_attr[a]
        self.delete_edges_from(self.edges())
        self.delete_nodes_from(self.nodes())


    def copy(self):
        """Return a copy of the graph."""
        import os
        (fd_read, fd_write) = os.pipe()
        fh_read = os.fdopen(fd_read, 'r')
        fh_write = os.fdopen(fd_write, 'w')
        self.write(fh_write)
        fh_write.close()
        return self.__class__(file=fh_read)


    def add_path(self, nlist):
        """Add the path of nodes given in nlist."""
        fromv = nlist.pop(0)
        while len(nlist) > 0:
            tov=nlist.pop(0)
            self.add_edge(fromv,tov)
            fromv=tov

    def add_cycle(self, nlist):
        """Add the cycle of nodes given in nlist."""
        self.add_path(nlist+[nlist[0]]) 

    def prepare_nbunch(self,nbunch=None):
        # private function to build bunch from nbunch
        if nbunch is None:   # include all nodes via iterator
            bunch=self.nodes_iter()
        elif nbunch in self: # if nbunch is a single node 
            bunch=[Node(self,nbunch)]
        else:                # if nbunch is a sequence of nodes
            try:   # capture error for nonsequence/iterator entries.
                bunch=[Node(self,n) for n in nbunch if n in self]
                # bunch=(n for n in nbunch if n in self) # need python 2.4
            except TypeError:
               raise TypeError("nbunch is not a node or a sequence of nodes")
        return bunch


    def subgraph(self, nbunch, inplace=False, name=None, create_using=None):
        """Return subgraph of graph induced by nodes in nbunch.

        This does not make a graphviz subgraph (see pygraphviz.graphviz).

        Optional inplace=True demolishes the graph instead of returning a
        new graph.

        """
        bunch=self.prepare_nbunch(nbunch)
        if inplace: # demolish all nodes (and attached edges) not in nbunch
            bunch=dict.fromkeys(bunch) # make a dict
            self.delete_nodes_from([n for n in self if n not in bunch])
            return self
        # create new graph        
        if create_using is None:  
            H=self.__class__(strict=self.is_strict(),directed=self.is_directed())
        else:                     # user specified graph
            H=create_using
            H.clear()
        H.add_nodes_from(bunch)
        for (u,v) in self.edges():
            if u in H and v in H: 
                H.add_edge(u,v)
        return H

    # directed, undirected tests and conversions

    def is_strict(self):
        """Return True if graph is strict or False if not.

        Strict graphs do not allow parallel edges or self loops.
        """
        if gv.agisstrict(self.handle)==1:
            return True
        else:
            return False
        

    def is_directed(self):
        """Return True if graph is directed or False if not."""
        if gv.agisdirected(self.handle)==1:
            return True
        else:
            return False

    def is_undirected(self):
        """Return True if graph is undirected or False if not."""
        if gv.agisundirected(self.handle)==1:
            return True
        else:
            return False

    def to_undirected(self):
        """Return undirected copy of graph."""
        if self.is_undirected():
            return self.copy()
        else:
            U=AGraph(strict=self.is_strict())
            for (k,v) in self.edge_attr.iteritems(): U.edge_attr[k]=v
            for (k,v) in self.node_attr.iteritems(): U.node_attr[k]=v
            for (k,v) in self.graph_attr.iteritems(): U.graph_attr[k]=v
            for n in self.nodes():
                U.add_node(n)
                new_n=Node(U,n)
                for (k,v) in n.attr.iteritems():
                    new_n.attr[k]=v
            for e in self.edges():
                (u,v)=e
                U.add_edge(u,v)
                uv=U.get_edge(u,v)
                for (k,v) in e.attr.iteritems():
                    uv.attr[k]=v
            return U


    def to_directed(self,**kwds):
        """Return directed copy of graph.

        Each undirected edge u-v is represented as two directed
        edges u->v and v->u.
        """
        if self.is_undirected():
            D=AGraph(strict=self.is_strict(),directed=True)
            for (k,v) in self.edge_attr.iteritems(): D.edge_attr[k]=v
            for (k,v) in self.node_attr.iteritems(): D.node_attr[k]=v
            for (k,v) in self.graph_attr.iteritems(): D.graph_attr[k]=v
            for n in self.nodes():
                D.add_node(n)
                new_n=Node(D,n)
                for (k,v) in n.attr.iteritems():
                    new_n.attr[k]=v
            for e in self.edges():
                (u,v)=e
                D.add_edge(u,v)
                D.add_edge(v,u)
                uv=D.get_edge(u,v)
                vu=D.get_edge(v,u)
                for (k,v) in e.attr.iteritems():
                    uv.attr[k]=v
                    vu.attr[k]=v
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
        fh=self._get_fh(path)
        try: 
            self.handle = gv.agread(fh,None)
        except IOError:
            print "IO error reading file"

    def write(self, path=None):
        """Read graph in dot format to file on path.
        
        path can be a file name or file handle

        use::

           G.write('file.dot')
        """
        if path is None:
            path=sys.stdout
        fh=self._get_fh(path,'w')
        try: 
            gv.agwrite(self.handle,fh)
        except IOError:
            print "IO error writing file"


    def string(self):
        """Return string representation of graph in dot format.""" 
        return self.draw(format='dot',prog='nop') 

    def _get_prog(self,prog):
        # private: get path of graphviz program
        try:
            gvprogs=dict.fromkeys(\
                ['neato','dot','twopi','circo','fdp','nop'])
            p=gvprogs[prog]
        except KeyError:
            raise ValueError("prog %s is not one of %s"%\
                           (prog,', '.join(gvprogs.keys()))) 
    
        try: # user must pick one of the graphviz programs...
            runprog = self._which(prog)
        except:
            raise ValueError("program %s not found in path"%prog) 
        return runprog


    def layout(self,prog='neato',args='',fmt='dot'):
        """Assign positions to nodes in graph.
        
        Optional prog=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
        will use specified graphviz layout method.

        >>> A=AGraph()
        >>> A.layout() # uses neato 
        >>> A.layout(prog='dot')

        Use keyword args to add additional arguments to graphviz programs.

        The layout might take a long time on large graphs.

        """
        import os

        if self.number_of_nodes()>1000:
            sys.stderr.write(\
              "Warning: graph has %s nodes...layout may take a long time.\n"%\
              self.number_of_nodes())
        runprog=self._get_prog(prog)
        cmd=' '.join([runprog,args,"-T"+fmt])
        stdin,stdout,stderr=os.popen3(cmd, 'b')
        self.write(stdin)
        stdin.close()
        try:
            self.read(stdout)
            stdout.close(); stderr.close()
        except:
            print stderr.read()
            stdout.close(); stderr.close()
            raise IOError("the graphviz layout with %s failed"%(prog))
        self.has_layout=True
        return


    def draw(self,path=None,format=None,prog=None,args=''):
        """Output graph to to path in specified format.

        An attempt will be made to guess the output format based
        on the file extension.  If that fails the format keyword
        will be used.
        
        Formats::

             ['canon','dot','xdot','cmap','dia','fig','gd','gd2',
             'gif','hpgl','imap','cmapx','ismap','jpg','jpeg',
             'mif','mp','pcl','pic','plain','plain-ext','png','ps',
             'ps2','svg','svgz','vrml','vtx','wbmp']

        If prog is not specified and the graph has positions
        (see layout()) then no additional graph positioning will
        be preformed.
                 
        Optional prog=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
        will use specified graphviz layout method.

        >>> G=AGraph()
        >>> G.layout()

        # use current node positions, output ps in 'file.ps'
        >>> G.draw('file.ps')

        # use dot to position, output png in 'file'
        >>> G.draw('file', format='png',prog='dot') 

        Use keyword args to add additional arguments to graphviz programs.

        The layout might take a long time on large graphs.

        """
        import os

        if path is not None:
            format=os.path.splitext(path)[1].lower()[1:]  # get extension

        if format is None:
            format='dot'
        else:
            formats=dict.fromkeys(
                ['canon','dot','xdot','cmap','dia','fig','gd','gd2',\
                 'gif','hpgl','imap','cmapx','ismap','jpg','jpeg',\
                 'mif','mp','pcl','pic','plain','plain-ext','png','ps',\
                 'ps2','svg','svgz','vrml','vtx','wbmp'])
            try:
                format in formats==True
            except KeyError:
                raise ValueError("format %s is not one of %s"%\
                           (format,', '.join(formats.keys()))) 
                
        if prog is None:
            try:
                self.has_layout==True
                prog='neato'
                args+=" -n2"
            except:
                raise AttributeError(\
                    "graph has no layout information, see layout()")

        else:
            if self.number_of_nodes()>1000:
                sys.stderr.write(\
              "Warning: graph has %s nodes...layout may take a long time.\n"%\
              self.number_of_nodes())

        runprog=self._get_prog(prog)
        cmd=''.join([prog,args," -T",format])
        stdin,stdout,stderr=os.popen3(cmd, 'b')
        self.write(stdin)
        stdin.close()
        data=None
        try:
            if path is None:
                data=stdout.read()
            else:
                fh=self._get_fh(path,'w')
                fh.write(stdout.read())
            stdout.close(); stderr.close()
        except:
            print stderr.read()
            stdout.close(); stderr.close()
            raise IOError("the graphviz layout with %s failed"%(prog))
        return data


    # some private helper functions

    def _is_string_like(self,obj): # from John Hunter, types-free version
        try:
            obj + ''
        except (TypeError, ValueError):
            return False
        return True


    def _get_fh(self, path, mode='r'):
        """ Return a file handle for given path.

        Path can be a string or a file handle.
        Attempt to uncompress/compress files ending in '.gz' and '.bz2'.
        """
        import os
        if self._is_string_like(path):
            if path.endswith('.gz'):
#                import gzip
#                fh = gzip.open(path,mode=mode)  # doesn't return real fh
                 fh=os.popen("gzcat "+path) # probably not portable
            elif path.endswith('.bz2'):
#                import bz2
#                fh = bz2.BZ2File(path,mode=mode) # doesn't return real fh
                 fh=os.popen("bzcat "+path) # probably not portable
            else:
                fh = file(path,mode=mode)
        elif hasattr(path, 'seek'):
            fh = path
        else:
            raise TypeError('path must be a string or file handle')
        return fh


    def _which(self,name):
        """Searches for name in exec path and returns full path"""
        import os
        import glob
        paths = os.environ["PATH"]
        for path in paths.split(os.pathsep):
            match=glob.glob(os.path.join(path, name))
            if match:
                return match[0]
        raise ValueError, "no prog %s in path"%name        



class Node(str):
    """Node object based on string.

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
    def __new__(self,graph,name):
        n=str.__new__(self,name)
        n.ghandle=graph.handle
        try:
            nh=gv.agnode(graph.handle,n,_Action.find)
        except KeyError:
            raise KeyError("node %s not in graph"%n)
        n.attr=ItemAttribute(nh,1)
        return n

    def get_handle(self):
        """Return pointer to graphviz node object.""" 
        return gv.agnode(self.ghandle,self,_Action.find)
        

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
    def __new__(self,graph,source,target,key=None):
        s=Node(graph,source)
        t=Node(graph,target)

        try:
            eh=gv.agedge(s.get_handle(),t.get_handle(),key,_Action.find)
        except KeyError:
            raise KeyError("edge %s-%s not in graph"%(source,target))

        if key is None:
            tp=tuple.__new__(self,(s,t))
        else:
            tp=tuple.__new__(self,(s,t,key))

        tp.ghandle=graph.handle
        tp.attr=ItemAttribute(eh,3)
        return tp

    def get_handle(self):
        """Return pointer to graphviz edge object.""" 
        try:
            sh=gv.agnode(self.ghandle,self[0],_Action.find)
        except KeyError:
            raise KeyError("node %s not in graph"%source)
        try:
            th=gv.agnode(self.ghandle,self[1],_Action.find)
        except KeyError:
            raise KeyError("node %s not in graph"%target)
        try:
            if len(self)==3:
                key=self[2]
            else:
                key=None
            return gv.agedge(sh,th,key,_Action.find)
        except KeyError:
            raise KeyError("edge %s-%s not in graph"%(source,target))



class Attribute(UserDict.DictMixin):
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
    def __init__(self,handle,atype):
        self.__dict__['handle']=handle
        self.__dict__['type']=atype

    def __setitem__(self, name, value):
        gv.agattr(self.handle,self.type,name,value)

    def __getitem__(self, name):
        try:
            ah=gv.agattr(self.handle,self.type,name,None)
            return gv.agattrdefval(ah)
        except KeyError:
            raise KeyError("no attribute found")

    def __delitem__(self, name):
        gv.agattr(self.handle,self.type,name,'')

    def __contains__(self, name):
        try:
            self.__getitem__(name)
            return True
        except:
            return False

    def has_key(self, name):
        return self.__contains__(name)

    def keys(self):
        return(list(self.__iter__()))

    def __iter__(self):
        for (k,v) in self.iteritems():
            yield k

    def iteritems(self):
        ah=None
        while True:
            try:
                ah=gv.agnxtattr(self.handle,self.type,ah)
                yield gv.agattrname(ah),gv.agattrdefval(ah)
            except KeyError: # gv.agattrdefval returned KeyError, skip
                continue

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
    def __init__(self,handle,atype):
        self.__dict__['handle']=handle
        self.__dict__['type']=atype
        self.__dict__['ghandle']=gv.agraphof(handle)

    def __setitem__(self, name, value):
        try:
            gv.agset(self.handle,name,value)
        except KeyError: # not in default dict, set default to be empty string
            gv.agattr(self.ghandle,self.type,name,'')
            gv.agset(self.handle,name,value)

    def __getitem__(self, name):
        return gv.agget(self.handle,name)

    def __delitem__(self, name):
        gv.agset(self.handle,name,'')

    def iteritems(self):
        ah=None
        while 1:
            try:
                ah=gv.agnxtattr(self.ghandle,self.type,ah) 
                value=gv.agxget(self.handle,ah)
                try: 
                    defval=gv.agattrdefval(ah) # default value
                    if defval==value: 
                        continue # don't report default
                except: # no default, gv.getattrdefval raised error
                    pass
                yield gv.agattrname(ah),value # unique value for this edge
            except KeyError: # gv.agxget returned KeyError, skip
                continue
    

def _test_suite():
    import doctest
    suite = doctest.DocFileSuite('tests/graph.txt',
                                 'tests/attributes.txt',
                                 'tests/layout_draw.txt',
                                 package='pygraphviz')
    doctest.testmod() # test docstrings in module
    return suite


if __name__ == "__main__":
    import os
    import sys
    import unittest
    if sys.version_info[:2] < (2, 4):
        print "Python version 2.4 or later required for tests (%d.%d detected)." %  sys.version_info[:2]
        sys.exit(-1)
    # directory of package (relative to this)
    nxbase=sys.path[0]+os.sep+os.pardir
    sys.path.insert(0,nxbase) # prepend to search path
    unittest.TextTestRunner().run(_test_suite())
    
