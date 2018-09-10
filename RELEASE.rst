How to make a new release of ``pygraphviz``
===========================================

- Update the release notes:

  1. Review and cleanup ``doc/source/reference/api_notes.rst``
     and ``doc/source/reference/news.rst``,

  2. Fix code in documentation by running
     ``cd doc && make doctest``.

- Toggle ``dev = True`` to ``dev = False`` in ``pygraphviz/release.py``.

- Commit changes.

- Add the version number as a tag in git::

   git tag -s [-u <key-id>] pygraphviz-<major>.<minor>

  (If you do not have a gpg key, use -m instead; it is important for
  Debian packaging that the tags are annotated)

- Push the new meta-data to github::

   git push --tags upstream master

  (where ``upstream`` is the name of the
   ``github.com:pygraphviz/pygraphviz`` repository.)

- Review the github release page::

  https://github.com/pygraphviz/pygraphviz/releases

- Publish on PyPi::

   git clean -fxd
   pip install -U pip setuptools wheel
   pip intsall -U twine
   python setup.py sdist --formats=gztar,zip bdist_wheel
   twine upload -s dist/*

- Update documentation on the web:
  The documentation is kept in a separate repo: pygraphviz/documentation

  - Sync your branch with the remote repo: ``git pull``.
  - Copy the documentation built by Travis.
    Assuming you are at the top-level of the ``documentation`` repo::

      cp -a latest pygraphviz-<major>.<minor> 
      git add pygraphviz-<major>.<minor>
      ln -sfn pygraphviz-<major>.<minor> stable
      git commit -m "Add <major>.<minor> docs"
      # maybe squash all the Deploy GitHub Pages commits
      # git rebase -i HEAD~XX where XX is the number of commits back
      # check you didn't break anything
      # diff -r latest pygraphviz-<major>.<minor>
      # you will then need to force the push so be careful!
      git push

 - Increase the version number

  - Toggle ``dev = False`` to ``dev = True`` in ``pygraphviz/release.py``.
  - Update ``version`` in ``pygraphviz/release.py``.

- Update the web frontpage:
  The webpage is kept in a separate repo: pygraphviz/website

  - Sync your branch with the remote repo: ``git pull``.
    If you try to ``make github`` when your branch is out of sync, it
    creates headaches.
  - Update ``_templates/sidebar_versions.html``.
  - Edit ``_static/docversions.js`` and commit
  - Push your changes to the repo.
  - Deploy using ``make github``.

- Post release notes on mailing list.

  - pygraphviz-discuss@googlegroups.com
