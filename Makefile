all:

swig:
	swig -python pygraphviz/graphviz.i
	# DOS endings to not corrupt the diff.
	@unix2dos pygraphviz/graphviz.py
	@unix2dos pygraphviz/graphviz_wrap.c

# Clean all build and test artifacts.
clean c:
	rm -rf build *.pyc *.egg-info MANIFEST .noseids __pycache__ .tox
	find pygraphviz -name '*.pyc' -delete
	find pygraphviz -name '*.so' -delete
	find pygraphviz -name '__pycache__' -type d | xargs --no-run-if-empty rm -r
