#    Copyright (C) 2004-2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.

%module graphviz
%include exception.i

%{
#include "agraph.h"
%}



%typemap(python, in) FILE* {
    if (!PyFile_Check($input)) {
        PyErr_SetString(PyExc_TypeError, "not a file handle");
        return NULL;
    }
    $1 = PyFile_AsFile($input);
}

%typemap(python, in) char* {
    if ($input == Py_None) {
        $1 = 0;
    } else if (!PyString_Check($input)) {
            PyErr_SetString(PyExc_TypeError, "not a valid string");
            return NULL;
    } else $1 = PyString_AsString($input);
}


%typemap(python, out) char * {
    $result = Py_BuildValue("s", $1);
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
}

/* agget returns "" if no value */
%exception agget {
  $action
  if (!strcmp(result,"")) {
    PyErr_SetString(PyExc_KeyError,arg2);
    return NULL;
  }
}

/* agxget returns "" if no value */
%exception agxget {
  $action
    if (!strcmp(result,"")) {
      PyErr_SetString(PyExc_KeyError,"No symbol");
      return NULL;
    }
}


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
     PyErr_SetString(PyExc_KeyError,"No key");
     return NULL;
  }
}


%exception agnxtattr {
  $action
  if (!result) {
     PyErr_SetString(PyExc_KeyError,"agnxtattr no key");
     return NULL;
  }
}



/* graphs */
Agraph_t *agopen(char *name, Agdesc_t kind, Agdisc_t *disc);
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

Agdesc_t Agdirected, Agstrictdirected, Agundirected, Agstrictundirected;


#define AGRAPH      0               /* can't exceed 2 bits. see Agtag_t. */
#define AGNODE      1
#define AGOUTEDGE   2
#define AGINEDGE    3               /* (1 << 1) indicates an edge tag.   */
#define AGEDGE      AGOUTEDGE       /* synonym in object kind args */
