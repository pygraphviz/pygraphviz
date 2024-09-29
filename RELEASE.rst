Release process for ``pygraphviz``
================================

Introduction
------------

Example ``version number``

-  1.8.dev0 # development version of 1.8 (release candidate 1)
-  1.8rc1 # 1.8 release candidate 1
-  1.8rc2.dev0 # development version of 1.8 release candidate 2
-  1.8 # 1.8 release
-  1.9.dev0 # development version of 1.9 (release candidate 1)

Process
-------

- Set release variables::

      export VERSION=<version number>
      export PREVIOUS=<previous version number>
      export ORG="pygraphviz"
      export REPO="pygraphviz"

  If this is a prerelease:

      export NOTES="doc/source/release/release_dev.rst"

  If this is release:

      export NOTES="doc/source/release/release_${VERSION}.rst"
      git rm doc/source/release/release_dev.rst

- Autogenerate release notes::

      changelist ${ORG}/${REPO}  pygraphviz-${PREVIOUS} main --version ${VERSION}  --out ${NOTES} --format rst
      changelist ${ORG}/${REPO}  pygraphviz-${PREVIOUS} main --version ${VERSION} --out ${VERSION}.md

- Update ``doc/source/release/index.rst``

- Edit ``doc/source/_static/version_switcher.json`` in order to add the release, move the
  key value pair `"preferred": true` to the most recent stable version, and commit.

-  Update ``version`` in ``pygraphviz/__init__.py``.

-  Commit changes::

      git add doc/source/release/index.rst ${NOTES}
      git add pygraphviz/__init__.py doc/source/_static/version_switcher.json
      pre-commit run -a
      git commit -m "Designate ${VERSION} release"

-  Tag the release in git::

      git tag -s pygraphviz-${VERSION} -m "signed ${VERSION} tag"

   If you do not have a gpg key, use -u instead; it is important for
   Debian packaging that the tags are annotated

-  Push the new meta-data to github::

      git push --tags origin main

   where ``origin`` is the name of the
   ``github.com:pygraphviz/pygraphviz`` repository

-  Review the github release page::

      https://github.com/pygraphviz/pygraphviz/tags

- Update documentation on the web:
  The documentation is kept in a separate repo: pygraphviz/documentation

  - Wait for the CI service to deploy to GitHub Pages
  - Sync your branch with the remote repo: ``git pull``.
  - Copy the documentation built by the CI service.
    Assuming you are at the top-level of the ``documentation`` repo::

      # FIXME - use eol_banner.html
      cp -a latest ../pygraphviz-${VERSION}
      git reset --hard <commit from last release>
      mv ../pygraphviz-${VERSION} .
      rm -rf stable
      cp -rf pygraphviz-${VERSION} stable
      git add pygraphviz-${VERSION} stable
      git commit -m "Add ${VERSION} docs"
      git push  # force push---be careful!

-  Update ``version`` in ``pygraphviz/__init__.py``.

-  Commit changes::

      git add pygraphviz/__init__.py
      git commit -m 'Bump version'
      git push origin main
