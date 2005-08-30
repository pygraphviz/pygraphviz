#    Copyright (C) 2004,2005 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    All rights reserved, see COPYING for details.
#
#    pygraphviz is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    pygraphviz is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pygraphviz; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

%module graphviz
%{
#include "agraph.h"
%}

%typemap(python, in) FILE* {
    if (!PyFile_Check($input)) {
        PyErr_SetString(PyExc_TypeError, "not a file");
        return NULL;
    }
    $1 = PyFile_AsFile($input);
}

%typemap(python, in) char* {
    if ($input == Py_None) {
        $1 = 0;
    } else if (!PyString_Check($input)) {
            PyErr_SetString(PyExc_TypeError, "not a string");
            return NULL;
    } else $1 = PyString_AsString($input);
}

%typemap(python, out) char * {
    $result = Py_BuildValue("s", $1);
}

%exception {
  $action
  if (!result) {
     PyErr_SetString(PyExc_KeyError,"No key");
     return NULL;
  }
}

/* agset returns -1 on error */
%exception agset {
  $action
  if (result==-1) {
     PyErr_SetString(PyExc_KeyError,"No key");
     return NULL;
  }
}

/* agget returns "" if no value */
%exception agget {
  $action
  if (!strcmp(result,"")) {
     PyErr_SetString(PyExc_KeyError,"No key");
     return NULL;
  }
}

/* agdelnode returns -1 on error */
%exception agdelnode {
  $action
  if (result==-1) {
     PyErr_SetString(PyExc_KeyError,"No key");
     return NULL;
  }
}

/* agdeledge returns -1 on error */
%exception agdeledge {
  $action
  if (result==-1) {
     PyErr_SetString(PyExc_KeyError,"No key");
     return NULL;
  }
}

%exception agnxtattr {
  $action
  if (!result) {
     PyErr_SetString(PyExc_KeyError,"No key");
     return NULL;
  }
}

/* figure out how to handle these */
%exception agwrite {
   $action  	   
}

%exception agread {
  $action
}

Agraph_t        *agopen(char *name, Agdesc_t kind, Agdisc_t *disc);
int             agclose(Agraph_t *g);
Agraph_t        *agread(FILE *file, Agdisc_t *);
Agraph_t        *agconcat(Agraph_t *g, void *chan, Agdisc_t *disc);
int             agwrite(Agraph_t *g, FILE *file);
int             agnnodes(Agraph_t *g),agnedges(Agraph_t *g);
int	        agisundirected(Agraph_t * g);
int             agisdirected(Agraph_t * g);



Agraph_t        *agsubg(Agraph_t *g, char *name, int createflag);
Agraph_t        *agfstsubg(Agraph_t *g), *agnxtsubg(Agraph_t *);
Agraph_t        *agparent(Agraph_t *g),  *agroot(Agraph_t *g);
long            agdelsubg(Agraph_t *g, Agraph_t *sub);

Agnode_t        *agnode(Agraph_t *g, char *name, int createflag);
Agnode_t        *agidnode(Agraph_t *g, unsigned long id, int createflag);
Agnode_t        *agsubnode(Agraph_t *g, Agnode_t *n, int createflag);
Agnode_t        *agfstnode(Agraph_t *g);
Agnode_t        *agnxtnode(Agnode_t *n);
int             agdelnode(Agnode_t *n);
int             agdegree(Agnode_t *n, int use_inedges, int use_outedges);

Agedge_t        *agedge(Agnode_t *t, Agnode_t *h, char *name, int createflag);
Agedge_t        *agsubedge(Agraph_t *g, Agedge_t *e, int createflag);
int             agdeledge(Agedge_t *e);

Agnode_t        *aghead(Agedge_t *e);
Agnode_t        *agtail(Agedge_t *e);
Agedge_t        *agfstedge(Agnode_t *n);
Agedge_t        *agnxtedge(Agedge_t *e, Agnode_t *n);
Agedge_t        *agfstin(Agnode_t *n);
Agedge_t        *agnxtin(Agedge_t *e);
Agedge_t        *agfstout(Agnode_t *n);
Agedge_t        *agnxtout(Agedge_t *e);

Agsym_t     *agattrsym(void *obj, char *name);
Agsym_t     *agattr(Agraph_t *g, int kind, char *name, char *value);
Agsym_t     *agnxtattr(Agraph_t *g, int kind, Agsym_t *attr);
char        *agget(void *obj, char *name);
char        *agxget(void *obj, Agsym_t *sym);
int         agset(void *obj, char *name, char *value);
int         agxset(void *obj, Agsym_t *sym, char *value);


%inline %{
 char        *agattrname(Agsym_t *atsym) {
              return atsym->name;
              }
         %}
%inline %{
 char        *agattrdefval(Agsym_t *atsym) {
              return atsym->defval;
              }
         %}


Agraph_t  *agraphof(void*);
char      *agnameof(void*);
int            agisarootobj(void*);
Agrec_t        *AGDATA(void *obj);
unsigned long          AGID(void *obj);
int            AGTYPE(void *obj);

Agdesc_t Agdirected, Agstrictdirected, Agundirected, Agstrictundirected;

#define AGRAPH      0               /* can't exceed 2 bits. see Agtag_t. */
#define AGNODE      1
#define AGOUTEDGE   2
#define AGINEDGE    3               /* (1 << 1) indicates an edge tag.   */
#define AGEDGE      AGOUTEDGE       /* synonym in object kind args */
