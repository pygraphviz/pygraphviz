all:

# Mirror the SWIG options passed by setup.py (keep the two in sync).
GRAPHVIZ_VERSION = $(shell dot -V 2>&1 | sed -nE 's/.*graphviz version ([0-9]+)\.([0-9]+)\.([0-9]+).*/\1 \2 \3/p')
SWIG_OPTS = -DGRAPHVIZ_VERSION_MAJOR=$(word 1,$(GRAPHVIZ_VERSION)) \
	-DGRAPHVIZ_VERSION_MINOR=$(word 2,$(GRAPHVIZ_VERSION)) \
	-DGRAPHVIZ_VERSION_PATCH=$(word 3,$(GRAPHVIZ_VERSION)) \
	-nogil

swig:
	swig -python $(SWIG_OPTS) pygraphviz/graphviz.i

# Clean all build and test artifacts.
clean c:
	rm -rf build *.pyc *.egg-info MANIFEST __pycache__ .tox
	find pygraphviz -name '*.pyc' -delete
	find pygraphviz -name '*.so' -delete
	find pygraphviz -name '__pycache__' -type d | xargs --no-run-if-empty rm -r
