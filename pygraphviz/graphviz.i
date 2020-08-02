//    Copyright (C) 2004-2006 by 
//    Aric Hagberg <hagberg@lanl.gov>
//    Dan Schult <dschult@colgate.edu>
//    Manos Renieris, http://www.cs.brown.edu/~er/
//    Distributed with BSD license.     
//    All rights reserved, see LICENSE for details.

%module graphviz

%{
#include "graphviz/cgraph.h"
%}

%{
static PyObject *PyIOBase_TypeObj;

static int init_file_emulator(void)
{
    PyObject *io = PyImport_ImportModule("_io");
    if (io == NULL)
        return -1;
    PyIOBase_TypeObj = PyObject_GetAttrString(io, "_IOBase");
    if (PyIOBase_TypeObj == NULL)
        return -1;
    return 0;
}
%}

%init %{
if (init_file_emulator() < 0) {
    return NULL;
}
%}

%typemap(in) FILE* (int fd, PyObject *mode_obj, PyObject *mode_byte_obj, char *mode) {
    if (!PyObject_IsInstance($input, PyIOBase_TypeObj)) {
        PyErr_SetString(PyExc_TypeError, "not a file handle");
        return NULL;
    }
    // work around to get hold of FILE*
    fd = PyObject_AsFileDescriptor($input);

    mode_obj = PyObject_GetAttrString($input, "mode");
    mode_byte_obj = PyUnicode_AsUTF8String(mode_obj);

    mode = PyBytes_AsString(mode_byte_obj);
    $1 = fdopen(fd, mode);
    Py_XDECREF(mode_obj);
    Py_XDECREF(mode_byte_obj);
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

/* agsetsafeset_label returns -1 on error */
%exception agsafeset_label {
  $action
  if (result==-1) {
     PyErr_SetString(PyExc_KeyError,"agsafeset_label: Error");
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


%exception agattr_label {
  $action
  if (!result) {
     PyErr_SetString(PyExc_KeyError,"agattr_label: no key");
     return NULL;
  }
}

%exception agread {
  $action
  if (!result) {
     PyErr_SetString(PyExc_ValueError,"agread: bad input data");
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


/* nodes */
Agnode_t *agnode(Agraph_t *g, char *name, int createflag);
Agnode_t *agidnode(Agraph_t * g, unsigned long id, int createflag); 
Agnode_t *agsubnode(Agraph_t *g, Agnode_t *n, int createflag);
Agnode_t *agfstnode(Agraph_t *g);
Agnode_t *agnxtnode(Agraph_t *g, Agnode_t *n);
Agnode_t *aglstnode(Agraph_t * g); 
Agnode_t *agprvnode(Agraph_t * g, Agnode_t * n); 
/* Agsubnode_t *agsubrep(Agraph_t * g, Agnode_t * n); */

/* edges */ 

Agedge_t *agedge(Agraph_t * g, Agnode_t * t, Agnode_t * h,
 		char *name, int createflag);
Agedge_t *agidedge(Agraph_t * g, Agnode_t * t, Agnode_t * h,
 		  unsigned long id, int createflag);
Agedge_t *agsubedge(Agraph_t * g, Agedge_t * e, int createflag);
Agedge_t *agfstin(Agraph_t * g, Agnode_t * n);
Agedge_t *agnxtin(Agraph_t * g, Agedge_t * e);
Agedge_t *agfstout(Agraph_t * g, Agnode_t * n);
Agedge_t *agnxtout(Agraph_t * g, Agedge_t * e);
Agedge_t *agfstedge(Agraph_t * g, Agnode_t * n);
Agedge_t *agnxtedge(Agraph_t * g, Agedge_t * e, Agnode_t * n);


Agnode_t *aghead(Agedge_t *e);
Agnode_t *agtail(Agedge_t *e);

/* attributes */
Agsym_t *agattr(Agraph_t *g, int kind, char *name, char *value);
Agsym_t *agattrsym(void *obj, char *name);
Agsym_t *agnxtattr(Agraph_t *g, int kind, Agsym_t *attr);
char    *agget(void *obj, char *name);
char    *agxget(void *obj, Agsym_t *sym);
int      agset(void *obj, char *name, char *value);
int      agxset(void *obj, Agsym_t *sym, char *value);
int      agsafeset(void *obj, char *name, char *value, char *def);

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

/* styled from gv.cpp in Graphviz to handle <> html data in label */
%inline %{
  int agsafeset_label(Agraph_t *g, void *obj, char *name, char *val, char *def)
{
    int len;
    char *hs;

    if (val[0] == '<' && (strcmp(name, "label") == 0 || strcmp(name, "xlabel") == 0)) {
        len = strlen(val);
        if (val[len-1] == '>') {
            hs = strdup(val+1);
                *(hs+len-2) = '\0';
            val = agstrdup_html(g,hs);
            free(hs);
        }
    }
    return agsafeset(obj, name, val,def);
}
  %}




/* styled from gv.cpp in Graphviz to handle <> html data in label */
%inline %{
  int agattr_label(Agraph_t *g, int kind, char *name, char *val)
{
    int len;
    char *hs;

    if (val[0] == '<' && (strcmp(name, "label") == 0 || strcmp(name, "xlabel") == 0)) {
        len = strlen(val);
        if (val[len-1] == '>') {
            hs = strdup(val+1);
                *(hs+len-2) = '\0';
            val = agstrdup_html(g,hs);
            free(hs);
        }
    }
    return agattr(g, kind, name, val);
}
  %}




/* subgraphs */
Agraph_t *agsubg(Agraph_t *g, char *name, int createflag);
Agraph_t *agfstsubg(Agraph_t *g); 
Agraph_t *agnxtsubg(Agraph_t *subg);
Agraph_t *agparent(Agraph_t *g);  
Agraph_t *agroot(Agraph_t *g);
/* Agedge_t *agsubedge(Agraph_t *g, Agedge_t *e, int createflag); */
long      agdelsubg(Agraph_t *g, Agraph_t *sub);


/* cardinality */
int agnnodes(Agraph_t * g);
int agnedges(Agraph_t * g);
int agdegree(Agraph_t * g, Agnode_t * n, int in, int out);

/* generic */
Agraph_t  *agraphof(void*);
char      *agnameof(void*);

int agdelnode(Agraph_t * g, Agnode_t * arg_n);
int agdeledge(Agraph_t * g, Agedge_t * arg_e);

/* This pretty code finds anonymous items (start with %) or
   items with no label and returns None.
   Useful for anonymous edges .
*/
%pythoncode %{
def agnameof(handle):
  name=_graphviz.agnameof(handle)
  if name is None:
     return None
  if name==b'' or name.startswith(b'%'):
    return None
  else:
    return name 
%}




/* Agdesc_t Agdirected, Agstrictdirected, Agundirected, Agstrictundirected;  */
/* constants are safer */
/* directed, strict, noloops, maingraph */
const Agdesc_t Agdirected = { 1, 0, 0, 1 };
const Agdesc_t Agstrictdirected = { 1, 1, 0, 1 };
const Agdesc_t Agundirected = { 0, 0, 0, 1 };
const Agdesc_t Agstrictundirected = { 0, 1, 0, 1 };


#define AGRAPH      0               /* can't exceed 2 bits. see Agtag_t. */
#define AGNODE      1
#define AGOUTEDGE   2
#define AGINEDGE    3               /* (1 << 1) indicates an edge tag.   */
#define AGEDGE      AGOUTEDGE       /* synonym in object kind args */



