How to make a new release of ``pygraphviz``
===========================================

- Update the release notes:

  1. Review and cleanup ``doc/source/reference/api_notes.rst``
     and ``doc/source/reference/news.rst``,

  2. Fix code in documentation by running
     ``cd doc && make doctest``.

  3. Remove ::

       {% block document %}
           {% include "dev_banner.html" %}
           {{ super() }}
       {% endblock %}

     from ``doc/source/_templates/layout.html``

- Update ``__version__`` in ``pygraphviz/__init__.py``.

- Commit changes::

  git add pygraphviz/__init__.py
  git commit -m 'Designate <version> release'

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

  - Wait for the CI service to deploy to GitHub Pages
  - Sync your branch with the remote repo: ``git pull``.
  - Copy the documentation built by the CI service.
    Assuming you are at the top-level of the ``documentation`` repo::

      # FIXME - use eol_banner.html
      cp -a latest pygraphviz-<version>
      ln -sfn pygraphviz-<version> stable
      git add pygraphviz-<version> stable
      git commit -m "Add <version> docs"
      # maybe squash the last XX  Deploy GitHub Pages commits
      # git reset --soft HEAD~XX && git commit
      # check you didn't break anything
      # diff -r latest pygraphviz-<version>
      # you will then need to force the push so be careful!
      git push

- Update ``__version__`` in ``pygraphviz/__init__.py``.

- Add ::

     {% block document %}
         {% include "dev_banner.html" %}
         {{ super() }}
     {% endblock %}

   to ``doc/source/_templates/layout.html``

- Commit changes::

  git add pygraphviz/__init__.py doc/source/_templates/layout.html
  git commit -m 'Bump version'

- Update the web frontpage:
  The webpage is kept in a separate repo: pygraphviz/website

  - Sync your branch with the remote repo: ``git pull``.
    If you try to ``make github`` when your branch is out of sync, it
    creates headaches.
  - Update ``build/index.html``.
  - Update ``build/_static/docversions.js``.
  - Push your changes to the repo.
  - Deploy using ``make github``.

- Post release notes on mailing list.

  - pygraphviz-discuss@googlegroups.com
