"""
A python interface to the graphviz library.
"""
#    Copyright (C) 2004,2005 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

import graphviz as gv

class ACTION:
    CREATE=1
    SEARCH=0


class Agraph(object):
    def __init__(self, agraph = None, name="Graphviz",
                 type=gv.cvar.Agundirected):
        if agraph==None:
            self.agraph = gv.agopen(name, type, None)
        else:
            self.agraph = agraph

    def __str__(self):
        return gv.agnameof(self.agraph)

    def close(self):
        gv.agclose(self.agraph)

    def read(self, fp):
        try: 
            self.agraph = gv.agread(fp,None)
        except IOError:
            print "Can\'t read file"

    def write(self, fp):
        try: 
            gv.agwrite(self.agraph, fp)
        except IOError:
            print "Can\'t write file"

    def nnodes(self):
        return gv.agnnodes(self.agraph)

    def nedges(self):
        return gv.agnedges(self.agraph)

    def is_directed(self):
        if gv.agisdirected(self.agraph)==1:
            return True
        else:
            return False

    def is_undirected(self):
        if gv.agisundirected(self.agraph)==1:
            return True
        else:
            return False

    def nodes(self):
        nodeslist = []
        a = gv.agfstnode(self.agraph)
        while a is not None:
            nodeslist.append(Agraph.Node(a))
            a = gv.agnxtnode(a)
        return nodeslist

    def edges(self):
        edgeslist = []
        nodes = self.nodes()
        for n in nodes:
            e = gv.agfstout(n.anode)
            while e is not None:
                edgeslist.append(Agraph.Edge(e))
                e = gv.agnxtout(e)
        return edgeslist

    def add_node(self, name):
        return Agraph.Node(gv.agnode(self.agraph, name, ACTION.CREATE))

    def get_node(self, name):
        try: 
            a = gv.agnode(self.agraph, name, ACTION.SEARCH)
            return Agraph.Node(a)
        except KeyError:
            print "No node \"%s\" in graph"%(name)
            return Nonep


    def delete_node(self, name):
        try:
            a=gv.agnode(self.agraph, name, ACTION.SEARCH)
            gv.agdelnode(a)
        except KeyError:
            print "No node \"%s\" in graph"%(name)
            return None


    def add_edge(self, source, target, name):
        try:
            s = Agraph.Node(gv.agnode(self.agraph, source, ACTION.CREATE))
            t = Agraph.Node(gv.agnode(self.agraph, target, ACTION.CREATE))
            return Agraph.Edge(gv.agedge(s.anode, t.anode, name, ACTION.CREATE))
        except:
            print "Can\'t create edge \"%s-%s\""%(source,target)

    def get_edge(self, source, target, name=None):
        try: 
            s = gv.agnode(self.agraph, source, ACTION.SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(source)
        try: 
            t = gv.agnode(self.agraph, target, ACTION.SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(target)
        try:
            e = gv.agedge(s, t, name, ACTION.SEARCH)
            return Agraph.Edge(e)
        except:
            print "No edge \"%s-%s\" \"%s\" in graph"%(source,target,name)
            return None

    def delete_edge(self, source, target, name):
        try:
            s = gv.agnode(self.agraph, source, ACTION.SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(source)
            return
        try:
            t = gv.agnode(self.agraph, target, Acdtion.SEARCH)
        except KeyError:
            print "No node \"%s\" in graph"%(target)
            return
        try: 
            e = gv.agedge(s, t, name, ACTION.SEARCH)
            gv.agdeledge(e)
        except KeyError:
            print "No edge \"%s-%s\" \"%s\" in graph"%(source,target,name)

    def graph(self):
        return Agraph(gv.agraphof(self.agraph))

    def get_all_attr(self, node=None, edge=None):
        if node is not None:
            n=self.get_node(str(node))
            pointer=n.anode
            type=gv.AGNODE
        elif edge is not None:
            (u,v)=edge
            e=self.get_edge(str(u),str(v))
            pointer=e.aedge
            type=gv.AGEDGE
        else:
            pointer=self.agraph
            type=gv.AGRAPH
            
        attr={}
        try:
            attrp=gv.agnxtattr(self.agraph,type,None) # pointer to 1st attr
        except KeyError:
            return attr
        while 1:
            try:
                attr[gv.agattrname(attrp)]=gv.agxget(pointer,attrp)
                attrp=gv.agnxtattr(self.agraph,type,attrp) # get next attr
            except KeyError:
                return attr

    def get_attr(self,name):
        try: 
            return gv.agget(self.agraph, name)
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
                gv.agset(self.agraph, str(name), str(value))
            except KeyError:
                gv.agattr(self.agraph, gv.AGRAPH, str(name), str(value))
            
    def set_graph_attr(self,attr=None, **kwds):
        self.set_attr(attr=attr, **kwds)

    def del_attr(self, name):
        # doesn't really delete anything, sets value to ""
        try: 
            gv.agset(self.agraph, name, "")
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
                    gv.agattr(self.agraph, gv.AGNODE, str(name), str(value))
                except KeyError:
                    print "Failed to set node attr \"%s\""%(name)
        else:
            if not isinstance(nodes,list): nodes=[nodes]
            for n in nodes:
                np=self.get_node(str(n))
                for (name,value) in attr.items():
                    try: 
                        gv.agset(np.anode, str(name), str(value))
                    except KeyError:
                        gv.agattr(self.agraph, gv.AGNODE, str(name), "")
                        try:
                            gv.agset(np.anode, str(name), str(value))
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
                    attr[n][name]=gv.agget(np.anode, name)
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
            gv.agattr(self.agraph, gv.AGNODE, name, "")
        except KeyError:
            print "No node attribute \"%s\" in graph"%(name)


    def set_edge_attr(self, edges=None, attr=None, **kwds):
        if attr is None:
            attr={}
        attr.update(kwds)
        if edges == None:
            for (name,value) in attr.items():
                try: 
                    gv.agattr(self.agraph, gv.AGEDGE, name, value)
                except KeyError:
                    print "Failed to set edge attr \"%s\""%(name)
        else:
            if not isinstance(edges,list): edges=[edges]
            for (u,v) in edges:
                ep=self.get_edge(str(u),str(v))
                for (name,value) in attr.items():
                    try: 
                        gv.agset(ep.aedge, str(name), str(value))
                    except KeyError:
                        gv.agattr(self.agraph, gv.AGEDGE, str(name), "")
                        try:
                            gv.agset(ep.aedge, str(name), str(value))
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
                    attr[e][name]=gv.agget(ep.aedge, name)
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
            gv.agattr(self.agraph, gv.AGEDGE, name, "")
        except KeyError:
            print "No edge attribute \"%s\" in graph"%(name)


    class Node(object):
        def __init__(self, anode):
            self.anode=anode

        def __str__(self):
            return gv.agnameof(self.anode)

        def get_attr(self, name):
            try:
                return gv.agget(self.anode, name)
            except KeyError:
                print "Node \"%s\" does not have attribute \"%s\""%(self,name)

        def set_attr(self, attr=None, **kwds):
            if attr is None:
                attr={}
            attr.update(kwds)
            for (name,value) in attr.items():
                try:
                    gv.agset(self.anode, str(name), str(value))
                except KeyError:
                    print "Node attribute \"%s\" not in graph."%(name),
                    print "Use set_node_attr(\"%s\",default)."%(name)

        def graph(self):
            return Agraph(gv.agraphof(self.anode))

    class Edge(object):
        def __init__(self, aedge):
            self.aedge=aedge

        def __str__(self):
            return gv.agnameof(self.aedge)

        def target(self):
            return Agraph.Node(gv.aghead(self.aedge))

        def source(self):
            return Agraph.Node(gv.agtail(self.aedge))

        def get_attr(self, name):
                try:
                    return gv.agget(self.aedge, name)
                except KeyError:
                    print "Edge attribute \"%s\" does not exist"%(name)

        def set_attr(self, attr=None, **kwds):
            if attr is None:
                attr={}
            attr.update(kwds)
            for (name,value) in attr.items():
                try:
                    gv.agset(self.aedge, str(name), str(value))
                except KeyError:
                    print "Edge attribute \"%s\" not in graph."%(name),
                    print "Use set_node_attr(\"%s\",default)."%(name)

        def graph(self):
            return Agraph(gv.agraphof(self.aedge))

    

def _test_suite():
    import doctest
    suite = doctest.DocFileSuite('tests/pygraphviz_test.txt',
                                 package='pygraphviz')
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
    
