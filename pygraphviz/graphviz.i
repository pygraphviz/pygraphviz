%module graphviz

%begin %{
#define SWIG_PYTHON_STRICT_BYTE_CHAR
%}

%{
#include "graphviz/cgraph.h"
#include "graphviz/gvc.h"
%}

%typemap(in) FILE* input_file (int fd, PyObject *mode_obj, PyObject *mode_byte_obj, char *mode) {
    if ($input == Py_None) { $1 = NULL; }
    else {
        // work around to get hold of FILE*
        fd = PyObject_AsFileDescriptor($input);

        mode_obj = PyObject_GetAttrString($input, "mode");
        mode_byte_obj = PyUnicode_AsUTF8String(mode_obj);

        mode = PyBytes_AsString(mode_byte_obj);
        $1 = fdopen(dup(fd), mode);
        Py_XDECREF(mode_obj);
        Py_XDECREF(mode_byte_obj);
    }
}

%typemap(in) FILE* output_file (int fd, PyObject *mode_obj, PyObject *mode_byte_obj, char *mode) {
    if ($input == Py_None) { $1 = NULL; }
    else {
        // work around to get hold of FILE*
        fd = PyObject_AsFileDescriptor($input);

        mode_obj = PyObject_GetAttrString($input, "mode");
        mode_byte_obj = PyUnicode_AsUTF8String(mode_obj);

        mode = PyBytes_AsString(mode_byte_obj);
        $1 = fdopen(fd, mode);
        Py_XDECREF(mode_obj);
        Py_XDECREF(mode_byte_obj);
    }
}

%typemap(freearg) FILE* input_file {
    fclose($1);
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
Agraph_t *agread(FILE *input_file, Agdisc_t *);
int       agwrite(Agraph_t *g, FILE *output_file);
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
  Agsym_t *agattr_label(Agraph_t *g, int kind, char *name, char *val)
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



/**************** GVC ******************/
/* Could do the whole gvc.h file here. */
/* But gvParseArgs code is "a mess" (their comment in source code) */
/* It uses global variables to set default attributes */
/* It doesn't update current nodes with these defaults yet it sets */
/* any future nodes to these defaults even if in a different graph */
/* and a different gvContext. */
/* The result is that you can set a default for one graph and it doesnt */
/* do anything to that graph, but then all future graphs have that default */
//
/* This code only uses a small portion of the libgvc functions. */
/* The focus is on layout and render operations. */

/*  set up a graphviz context - and init graph - retaining old API */
GVC_t *gvContext(void);
int gvFreeContext(GVC_t *gvc);

/* Compute a layout using a specified engine */
int gvLayout(GVC_t *gvc, Agraph_t *g, char* prog);
int gvFreeLayout(GVC_t *gvc, Agraph_t *g);

/* Render layout in a specified format to an open FILE */
int gvRender(GVC_t *gvc, Agraph_t* g, char *format, FILE *output_file=NULL);
int gvRenderFilename(GVC_t *gvc, Agraph_t* g, char *format, char *filename);

/* Render layout in a specified format to an external context */
/*-------------------------------------------------------------*/
/* Writing a dot file to a string involves some pointer crazy stuff */
/* (the input strings are changed by the function... this magic makes */
/* python return the strings instead of changing the input. The next */
/* three lines are straight from the SWIG manual.  */
%include <cstring.i>
%include <typemaps.i>
%cstring_output_allocate_size(char **result, unsigned int* size, free(*$1));
int gvRenderData(GVC_t *gvc, Agraph_t* g, char *format, char **result, unsigned int *size);
/* Free memory allocated and pointed to by *result in gvRenderData */
extern void gvFreeRenderData (char* data);
