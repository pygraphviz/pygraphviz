all:

swig:
	swig -python pygraphviz/graphviz.i

# Clean all build and test artifacts.
clean c:
	rm -rf build *.pyc *.egg-info MANIFEST __pycache__ .tox
	find pygraphviz -name '*.pyc' -delete
	find pygraphviz -name '*.so' -delete
	find pygraphviz -name '__pycache__' -type d | xargs --no-run-if-empty rm -r
