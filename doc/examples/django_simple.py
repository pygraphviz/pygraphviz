#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple example for rendering a graph with the Django web framework.
See
http://www.djangoproject.com/
and
http://www.djangobook.com/en/beta/chapter11/

"""
#    Copyright (C) 2007 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""

from django.http import HttpResponse
def pygraphviz_graph(request):
    import pygraphviz as P
    A=P.AGraph() # init empty graph
    # set some default node attributes
    A.node_attr['style']='filled'
    A.node_attr['shape']='circle'
    # Add edges (and nodes)
    A.add_edge(1,2)
    A.add_edge(2,3)
    A.add_edge(1,3)
    A.layout() # layout with default (neato)
    png=A.draw(format='png') # draw png
    return HttpResponse(png, mimetype='image/png')

