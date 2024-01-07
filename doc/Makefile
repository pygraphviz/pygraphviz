# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =

# Internal variables.
ALLSPHINXOPTS   = -d build/doctrees $(SPHINXOPTS) source

.PHONY: help clean html dirhtml linkcheck doctest

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  dirhtml   to make HTML files named index.html in directories"
	@echo "  linkcheck to check all external links for integrity"
	@echo "  doctest   to run all doctests embedded in the documentation (if enabled)"


clean:
	-rm -rf build/* source/reference/generated/* source/examples/* source/static/examples doc/source/*.pdf doc/source/*.zip
	-rm -rf ../examples/*/*.png
	-rm -rf source/auto_examples

generate: build/generate-stamp
build/generate-stamp: $(wildcard source/reference/*.rst)
	mkdir -p build
	touch build/generate-stamp

html: generate
	#make latex
	#make -C build/latex all-pdf
	#cp build/latex/pygraphviz.pdf source/.
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) build/html
	@echo
	@echo "Build finished. The HTML pages are in build/html."

dirhtml: generate
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) build/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in build/dirhtml."

linkcheck: generate
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) build/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in build/linkcheck/output.txt."

doctest: generate
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) build/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in build/doctest/output.txt."
