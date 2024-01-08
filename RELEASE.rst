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

-  Set release variables::

      export VERSION=<version number>
      export PREVIOUS=<previous version number>
      export ORG="pygraphviz"
      export REPO="pygraphviz"

-  Autogenerate release notes::

      changelist ${ORG}/${REPO} v${PREVIOUS} main --version ${VERSION}

-  Put the output of the above command at the top of ``CHANGELOG.md``

-  Update ``version`` in ``pygraphviz/__init__.py``.

-  Commit changes::

      git add pygraphviz/__init__.py CHANGELOG.md
      git commit -m "Designate ${VERSION} release"

-  Tag the release in git::

      git tag -s v${VERSION} -m "signed ${VERSION} tag"

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

      # maybe squash the last XX  Deploy GitHub Pages commits
      # git reset --soft HEAD~XX && git commit
      # check you didn't break anything
      # diff -r latest pygraphviz-<version>
      # you will then need to force the push so be careful!
      cp -a latest pygraphviz-<version>
      cp -a latest stable
      git add pygraphviz-<version> stable

-  Update ``version`` in ``pygraphviz/__init__.py``.

-  Commit changes::

      git add pygraphviz/__init__.py
      git commit -m 'Bump version'
      git push origin main
