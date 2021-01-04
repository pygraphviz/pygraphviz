How to make a new release of ``pygraphviz``
===========================================

- Update the release notes:

  1. Review and cleanup ``doc/source/reference/api_notes.rst``
     and ``doc/source/reference/news.rst``,

  2. Fix code in documentation by running
     ``cd doc && make doctest``.

- Update ``__version__`` in ``pygraphviz/__init__.py``.

- Commit changes.

- Add the version number as a tag in git::

   git tag -s [-u <key-id>] pygraphviz-<version> -m 'signed <version> tag'

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
   python setup.py sdist --formats=zip
   twine upload -s dist/pygraphviz*.zip

- Update documentation on the web:
  The documentation is kept in a separate repo: pygraphviz/documentation

  - Sync your branch with the remote repo: ``git pull``.
  - Copy the built documentation.

- Update ``__version__`` in ``pygraphviz/__init__.py``.

- Update the web frontpage:
  The webpage is kept in a separate repo: pygraphviz/website

  - Sync your branch with the remote repo: ``git pull``.
    If you try to ``make github`` when your branch is out of sync, it
    creates headaches.
  - Update ``documentation.rst``.
  - Update ``_templates/sidebar_versions.html``.
  - Push your changes to the repo.
  - Deploy using ``make github``.

- Post release notes on mailing list.

  - pygraphviz-discuss@googlegroups.com
