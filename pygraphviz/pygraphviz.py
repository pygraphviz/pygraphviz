"""
A python interface to the graphviz library.
"""
#    Copyright (C) 2004,2005 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

from graphviz import *

CREATE=1
SEARCH=0

class Agraph(object):
    def __init__(self, agraph = None, name="Graphviz", type=cvar.Agundirected):
        if agraph==None:
            self.agraph = agopen(name, type, None)
        else:
            self.agraph = agraph

    def __str__(self):
        return agnameof(self.agraph)

    def close(self):
        agclose(self.agraph)

    def read(self, fp):
        try: 
            self.agraph = agread(fp,None)
        except IOError:
            print "Can\'t read file"

    def write(self, fp):
        try: 
            agwrite(self.agraph, fp)
        except IOError:
            print "Can\'t write file"

    def nnodes(self):
        return agnnodes(self.agraph)

    def nedges(self):
        return agnedges(self.agraph)

    def is_directed(self):
        try:
            agisdirected(self.agraph)
            return True
        except:
            pass
        return False

    def is_undirected(self):
        try:
            agisundirected(self.agraph)
            return True
        except:
            pass
        return  False


    def nodes(self):
        nodeslist = []
        try:
            a = agfstnode(self.agraph)
        except KeyError:
            return nodeslist
        while 1:
            try:
                nodeslist.append(Agraph.Node(a))
                a = agnxtnode(a)
            except KeyError:
                return tuple(nodeslist)

    def edges(self):
        edgeslist = []
        nodes = self.nodes()
        for n in nodes:
            try: 
                e = agfstout(n.anode)
                edgeslist.append(Agraph.Edge(e))
            except:
                continue
            while 1:
                try:
                    e = agnxtout(e)
                    edgeslist.append(Agraph.Edge(e))
                except KeyError:
                    break
        return tuple(edgeslist)

    def add_node(self, name):
        return Agraph.Node(agnode(self.agraph, name, CREATE))

    def get_node(self, name):
        try: 
            a = agnode(self.agraph, name, SEARCH)
            return Agraph.Node(a)
        except KeyError:
            print "No node \"%s\" in graph"%(name)
            return None


    def delete_node(self, name):
        try:
            a=agnode(self.agraph, name, SEARCH)
            agdelnode(a)
        except KeyError:
            print "No node \"%s\" in graph"%(name)
            return None


    def add_edge(self, source, target, name):
        try:
            s = Agraph.Node(agnode(self.agraph, source, CREATE))
            t = Agraph.Node(agnode(self.agraph, target, CREATE))
            return Agraph.Edge(agedge(s.anode, t.anode, name, CREATE))
        except:
            print "Can\'t create edge \"%s-%s\""%(source,target)

    def get_edge(self, source, target, name=None):
        try: 
            s = agnode(self.agraph, source, SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(source)
        try: 
            t = agnode(self.agraph, target, SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(target)
        try:
            e = agedge(s, t, name, SEARCH)
            return Agraph.Edge(e)
        except:
            print "No edge \"%s-%s\" \"%s\" in graph"%(source,target,name)
            return None

    def delete_edge(self, source, target, name):
        try:
            s = agnode(self.agraph, source, SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(source)
            return
        try:
            t = agnode(self.agraph, target, SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(target)
            return
        try: 
            e = agedge(s, t, name, SEARCH)
            agdeledge(e)
        except KeyError:
            print "No edge \"%s-%s\" \"%s\" in graph"%(source,target,name)

    def graph(self):
        return Agraph(agraphof(self.agraph))

    def get_all_attr(self, node=None, edge=None):
        if node is not None:
            n=self.get_node(str(node))
            pointer=n.anode
            type=AGNODE
        elif edge is not None:
            (u,v)=edge
            e=self.get_edge(str(u),str(v))
            pointer=e.aedge
            type=AGEDGE
        else:
            pointer=self.agraph
            type=AGRAPH
            
        attr={}
        try:
            attrp=agnxtattr(self.agraph,type,None) # pointer to 1st attr
        except KeyError:
            return attr
        while 1:
            try:
                attr[agattrname(attrp)]=agxget(pointer,attrp)
                attrp=agnxtattr(self.agraph,type,attrp) # get next attr
            except KeyError:
                return attr

    def get_attr(self,name):
        try: 
            return agget(self.agraph, name)
        except KeyError:
            print "Attribute \"%s\" does not exist"%(name)

    def get_graph_attr(self,name):
        self.get_attr(name)

    def set_attr(self, attr=None, **kwds):
        if attr is None:
            attr={}
        attr.update(kwds)
        for (name,value) in attr.items():
            try: 
                agset(self.agraph, str(name), str(value))
            except KeyError:
                agattr(self.agraph, AGRAPH, str(name), str(value))
            
    def set_graph_attr(self,attr=None, **kwds):
        self.set_attr(attr=attr, **kwds)

    def del_attr(self, name):
        # doesn't really delete anything, sets value to ""
        try: 
            agset(self.agraph, name, "")
        except KeyError:
            print "No attribute \"%s\" in graph."%(name)

    def del_graph_attr(self,name):
        self.del_attr(name)

    def set_node_attr(self, nodes=None, attr=None, **kwds):
        if attr is None:
            attr={}
        attr.update(kwds)
        if nodes is None:
            for (name,value) in attr.items():
                try: 
                    agattr(self.agraph, AGNODE, str(name), str(value))
                except KeyError:
                    print "Failed to set node attr \"%s\""%(name)
        else:
            if not isinstance(nodes,list): nodes=[nodes]
            for n in nodes:
                np=self.get_node(str(n))
                for (name,value) in attr.items():
                    try: 
                        agset(np.anode, str(name), str(value))
                    except KeyError:
                        agattr(self.agraph, AGNODE, str(name), "")
                        try:
                            agset(np.anode, str(name), str(value))
                        except KeyError:
                            print "Failed to set attr \"%s\" for node \"%s\""%(name, n)

    def get_node_attr(self, nodes, items=[]):
        if not isinstance(items,list): items=[items]
        if not isinstance(nodes,list): nodes=[nodes]
        attr={}
        for n in nodes:
            attr[n]={}
            np=self.get_node(str(n))
            for name in items:
                try: 
                    attr[n][name]=agget(np.anode, name)
                except KeyError:
                    print "Failed to get attr \"%s\" for node \"%s\""%(name, n)

        if len(attr)==1:
            if len(attr[n])==1:
                return attr[n][name]
            else:
                return attr[n]
        else:
            return attr


    def del_node_attr(self, name):
        # doesn't really delete anything, sets value to ""
        try: 
            agattr(self.agraph, AGNODE, name, "")
        except KeyError:
            print "No node attribute \"%s\" in graph"%(name)


    def set_edge_attr(self, edges=None, attr=None, **kwds):
        if attr is None:
            attr={}
        attr.update(kwds)
        if edges == None:
            for (name,value) in attr.items():
                try: 
                    agattr(self.agraph, AGEDGE, name, value)
                except KeyError:
                    print "Failed to set edge attr \"%s\""%(name)
        else:
            if not isinstance(edges,list): edges=[edges]
            for (u,v) in edges:
                ep=self.get_edge(str(u),str(v))
                for (name,value) in attr.items():
                    try: 
                        agset(ep.aedge, str(name), str(value))
                    except KeyError:
                        agattr(self.agraph, AGEDGE, str(name), "")
                        try:
                            agset(ep.aedge, str(name), str(value))
                        except KeyError:
                            print "Failed to set attr \"%s\" for edge \"%s\""%(name, ep)


    def get_edge_attr(self, edges, items=[]):
        if not isinstance(items,list): items=[items]
        if not isinstance(edges,list): edges=[edges]
        attr={}
        for e in edges:
            attr[e]={}
            (u,v)=e
            ep=self.get_edge(str(u),str(v))
            for name in items:
                try: 
                    attr[e][name]=agget(ep.aedge, name)
                except KeyError:
                    print "Failed to get attr \"%s\" for edge \"%s\""%(name, e)

        if len(attr)==1:
            if len(attr[e])==1:
                return attr[e][name]
            else:
                return attr[e]
        else:
            return attr


    def del_edge_attr(self, name):
        # doesn't really delete anything, sets value to ""
        try: 
            agattr(self.agraph, AGEDGE, name, "")
        except KeyError:
            print "No edge attribute \"%s\" in graph"%(name)


    class Node(object):
        def __init__(self, anode):
            self.anode=anode

        def __str__(self):
            return agnameof(self.anode)

        def get_attr(self, name):
            try:
                return agget(self.anode, name)
            except KeyError:
                print "Node \"%s\" does not have attribute \"%s\""%(self,name)

        def set_attr(self, attr=None, **kwds):
            if attr is None:
                attr={}
            attr.update(kwds)
            for (name,value) in attr.items():
                try:
                    agset(self.anode, str(name), str(value))
                except KeyError:
                    print "Node attribute \"%s\" not in graph."%(name),
                    print "Use set_node_attr(\"%s\",default)."%(name)

        def graph(self):
            return Agraph(agraphof(self.anode))

    class Edge(object):
        def __init__(self, aedge):
            self.aedge=aedge

        def __str__(self):
            return agnameof(self.aedge)

        def target(self):
            return Agraph.Node(aghead(self.aedge))

        def source(self):
            return Agraph.Node(agtail(self.aedge))

        def get_attr(self, name):
                try:
                    return agget(self.aedge, name)
                except KeyError:
                    print "Edge attribute \"%s\" does not exist"%(name)

        def set_attr(self, attr=None, **kwds):
            if attr is None:
                attr={}
            attr.update(kwds)
            for (name,value) in attr.items():
                try:
                    agset(self.aedge, str(name), str(value))
                except KeyError:
                    print "Edge attribute \"%s\" not in graph."%(name),
                    print "Use set_node_attr(\"%s\",default)."%(name)

        def graph(self):
            return Agraph(agraphof(self.aedge))

