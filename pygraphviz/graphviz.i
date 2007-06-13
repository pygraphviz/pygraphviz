#    Copyright (C) 2004-2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

%module graphviz

%{
#include "agraph.h"
%}


%typemap(in) FILE* {
    if (!PyFile_Check($input)) {
        PyErr_SetString(PyExc_TypeError, "not a file handle");
        return NULL;
    }
    $1 = PyFile_AsFile($input);
}


%exception agnode {
  $action
  if (!result) {
     PyErr_SetString(PyExc_KeyError,"agnode: no key");
     return NULL;
  }
}

%exception agedge {
  $action
  if (!result) {
     PyErr_SetString(PyExc_KeyError,"agedge: no key");
     return NULL;
  }
}

/* agset returns -1 on error */
%exception agset {
  $action
  if (result==-1) {
     PyErr_SetString(PyExc_KeyError,"agset: no key");
     return NULL;
  }
} */

/* agdelnode returns -1 on error */
%exception agdelnode {
  $action
  if (result==-1) {
     PyErr_SetString(PyExc_KeyError,"agdelnode: no key");
     return NULL;
  }
}

/* agdeledge returns -1 on error */
%exception agdeledge {
  $action
  if (result==-1) {
     PyErr_SetString(PyExc_KeyError,"agdeledge: no key");
     return NULL;
  }
}

%exception agnxtattr {
  $action
  if (!result) {
     PyErr_SetString(PyExc_StopIteration,"agnxtattr");
     return NULL;
  }
}


%exception agattr {
  $action
  if (!result) {
     PyErr_SetString(PyExc_KeyError,"agattr: no key");
     return NULL;
  }
}


/* agattrdefval returns "" if no value */
%exception agattrdefval {
  $action
    if (!strcmp(result,"")) {
      PyErr_SetString(PyExc_KeyError,"agattrdefval: no symbol");
      return NULL;
    }
}


/* graphs */
Agraph_t *agopen(char *name, Agdesc_t kind, Agdisc_t *disc);

/* some helpers to avoid using cvar in python modules */
%pythoncode %{
def agraphnew(name,strict=False,directed=False):
    if strict:
       if directed:
            return _graphviz.agopen(name,cvar.Agstrictdirected,None)
       else:
            return _graphviz.agopen(name,cvar.Agstrictundirected,None)
    else:
        if directed:
            return _graphviz.agopen(name,cvar.Agdirected,None)
        else:		 
            return _graphviz.agopen(name,cvar.Agundirected,None)
%}

int       agclose(Agraph_t *g);
Agraph_t *agread(FILE *file, Agdisc_t *);
int       agwrite(Agraph_t *g, FILE *file);
int	  agisundirected(Agraph_t * g);
int       agisdirected(Agraph_t * g);
int       agisstrict(Agraph_t * g);
/* void      agclean(Agraph_t *g, int kind, int *rec)   */
/* Agraph_t        *agconcat(Agraph_t *g, FILE *file, Agdisc_t *disc); */


/* subgraphs */
Agraph_t *agsubg(Agraph_t *g, char *name, int createflag);
Agraph_t *agfstsubg(Agraph_t *g); 
Agraph_t *agnxtsubg(Agraph_t *subg);
Agraph_t *agparent(Agraph_t *g);  
Agraph_t *agroot(Agraph_t *g);
Agnode_t *agsubnode(Agraph_t *g, Agnode_t *n, int createflag);
Agedge_t *agsubedge(Agraph_t *g, Agedge_t *e, int createflag);
long      agdelsubg(Agraph_t *g, Agraph_t *sub);

/* nodes */
Agnode_t *agnode(Agraph_t *g, char *name, int createflag);
Agnode_t *agfstnode(Agraph_t *g);
Agnode_t *agnxtnode(Agnode_t *n);
int       agdelnode(Agnode_t *n);


/* edges */ 

Agedge_t *agedge(Agnode_t *t, Agnode_t *h, char *name, int createflag);
Agnode_t *aghead(Agedge_t *e);
Agnode_t *agtail(Agedge_t *e);
Agedge_t *agfstedge(Agnode_t *n);
Agedge_t *agnxtedge(Agedge_t *e, Agnode_t *n);
Agedge_t *agfstin(Agnode_t *n);
Agedge_t *agnxtin(Agedge_t *e);
Agedge_t *agfstout(Agnode_t *n);
Agedge_t *agnxtout(Agedge_t *e);
int       agdeledge(Agedge_t *e);

/* attributes */
Agsym_t *agattr(Agraph_t *g, int kind, char *name, char *value);
Agsym_t *agattrsym(void *obj, char *name);
Agsym_t *agnxtattr(Agraph_t *g, int kind, Agsym_t *attr);
char    *agget(void *obj, char *name);
char    *agxget(void *obj, Agsym_t *sym);
int      agset(void *obj, char *name, char *value);
int      agxset(void *obj, Agsym_t *sym, char *value);

%inline %{
  char *agattrname(Agsym_t *atsym) {	
    return atsym->name;
  }
  %}

%inline %{
  char *agattrdefval(Agsym_t *atsym) {
    return atsym->defval;
  }
  %}



/* cardinality */
int agnnodes(Agraph_t *g);
int agnedges(Agraph_t *g);
int agdegree(Agnode_t *n, int use_inedges, int use_outedges);


/* generic */
Agraph_t  *agraphof(void*);
char      *agnameof(void*);

/* this pretty code finds anonymous items (start with %) or
   items with no label and returns None - useful for anonymous
   edges 
*/
%pythoncode %{
def agnameof(handle):
  name=_graphviz.agnameof(handle)
  if name=='' or name.startswith('%'):
    return None
  else:
    return name 
%}


/* Agdesc_t Agdirected, Agstrictdirected, Agundirected, Agstrictundirected;  */
/* constants are safer */
const Agdesc_t Agdirected = { 1, 0, 0, 1 };
const Agdesc_t Agstrictdirected = { 1, 1, 0, 1 };
const Agdesc_t Agundirected = { 0, 0, 0, 1 };
const Agdesc_t Agstrictundirected = { 0, 1, 0, 1 };


#define AGRAPH      0               /* can't exceed 2 bits. see Agtag_t. */
#define AGNODE      1
#define AGOUTEDGE   2
#define AGINEDGE    3               /* (1 << 1) indicates an edge tag.   */
#define AGEDGE      AGOUTEDGE       /* synonym in object kind args */



