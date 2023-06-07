.. _contributor_guide:

Contributor Guide
=================

.. note::
   This document assumes some familiarity with contributing to open source
   scientific Python projects using GitHub pull requests.

.. _dev_workflow:

Development Workflow
--------------------

1. If you are a first-time contributor:

   * You'll need to install GraphViz on your local computer, if you haven't
     already.  For OS-specific installation instructions, refer to `INSTALL.txt
     <https://github.com/pygraphviz/pygraphviz/blob/main/INSTALL.txt>`_.

   * Go to `https://github.com/pygraphviz/pygraphviz
     <https://github.com/pygraphviz/pygraphviz>`_ and click the
     "fork" button to create your own copy of the project.

   * Clone the project to your local computer::

      git clone git@github.com:your-username/pygraphviz.git

   * Navigate to the folder pygraphviz and add the upstream repository::

      git remote add upstream git@github.com:pygraphviz/pygraphviz.git

   * Now, you have remote repositories named:

     - ``upstream``, which refers to the ``pygraphviz`` repository
     - ``origin``, which refers to your personal fork

   * Next, you need to set up your build environment.
     Here are instructions using ``venv``:

     * ``venv`` (pip based)

       ::

         # Create a virtualenv named ``pygraphviz-dev`` that lives in the directory of
         # the same name
         python -m venv pygraphviz-dev
         # Activate it
         source pygraphviz-dev/bin/activate
         # Install main development and runtime dependencies of pygraphviz
         pip install -r requirements/test.txt -r requirements/developer.txt
         #
         # Build and install pygraphviz from source
         pip install -e .
         # Test your installation
         PYTHONPATH=. pytest pygraphviz

   * Finally, we recommend you use a pre-commit hook, which runs black when
     you type ``git commit``::

       pre-commit install

2. Develop your contribution:

   * Pull the latest changes from upstream::

      git checkout main
      git pull upstream main

   * Create a branch for the feature you want to work on. Since the
     branch name will appear in the merge message, use a sensible name
     such as 'bugfix-for-issue-1480'::

      git checkout -b bugfix-for-issue-1480

   * Commit locally as you progress (``git add`` and ``git commit``)

3. Test your contribution:

   * Run the test suite locally (see `Testing`_ for details)::

      PYTHONPATH=. pytest pygraphviz

   * Running the tests locally *before* submitting a pull request helps catch
     problems early and reduces the load on the continuous integration
     system.

4. Submit your contribution:

   * Push your changes back to your fork on GitHub::

      git push origin bugfix-for-issue-1480

   * Go to GitHub. The new branch will show up with a green Pull Request
     button---click it.

   * If you want, post on the `mailing list
     <https://groups.google.com/forum/#!forum/pygraphviz-discuss>`_ to explain your changes or
     to ask for review.

5. Review process:

   * Every Pull Request (PR) update triggers a set of `continuous integration
     <https://en.wikipedia.org/wiki/Continuous_integration>`_ services
     that check that the code is up to standards and passes all our tests.
     These checks must pass before your PR can be merged.  If one of the
     checks fails, you can find out why by clicking on the "failed" icon (red
     cross) and inspecting the build and test log.

   * Reviewers (the other developers and interested community members) will
     write inline and/or general comments on your PR to help
     you improve its implementation, documentation, and style.  Every single
     developer working on the project has their code reviewed, and we've come
     to see it as friendly conversation from which we all learn and the
     overall code quality benefits.  Therefore, please don't let the review
     discourage you from contributing: its only aim is to improve the quality
     of project, not to criticize (we are, after all, very grateful for the
     time you're donating!).

   * To update your PR, make your changes on your local repository
     and commit. As soon as those changes are pushed up (to the same branch as
     before) the PR will update automatically.

   .. note::

      If the PR closes an issue, make sure that GitHub knows to automatically
      close the issue when the PR is merged.  For example, if the PR closes
      issue number 1480, you could use the phrase "Fixes #1480" in the PR
      description or commit message.

      To reviewers: make sure the merge message also has a brief description of
      the change(s).

Divergence from ``upstream main``
---------------------------------

If GitHub indicates that the branch of your Pull Request can no longer
be merged automatically, merge the main branch into yours::

   git fetch upstream main
   git merge upstream/main

If any conflicts occur, they need to be fixed before continuing.  See
which files are in conflict using::

   git status

Which displays a message like::

   Unmerged paths:
     (use "git add <file>..." to mark resolution)

     both modified:   file_with_conflict.txt

Inside the conflicted file, you'll find sections like these::

   <<<<<<< HEAD
   The way the text looks in your branch
   =======
   The way the text looks in the main branch
   >>>>>>> main

Choose one version of the text that should be kept, and delete the
rest::

   The way the text looks in your branch

Now, add the fixed file::


   git add file_with_conflict.txt

Once you've fixed all merge conflicts, do::

   git commit

.. note::

   Advanced Git users may want to rebase instead of merge,
   but we squash and merge PRs either way.

Guidelines
----------

* All code should have tests.
* All code should be documented, to the same
  `standard <https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_
  as NumPy and SciPy.
* All changes are reviewed.  Ask on the
  `mailing list <https://groups.google.com/forum/#!forum/pygraphviz-discuss>`_ if
  you get no response to your pull request.

Testing
-------

To run all tests::

    $ PYTHONPATH=. pytest pygraphviz

Or tests from a specific file::

    $ PYTHONPATH=. pytest pygraphviz/tests/test_readwrite.py

Use ``--doctest-modules`` to run doctests.
For example, run all tests and all doctests using::

    $ PYTHONPATH=. pytest --doctest-modules pygraphviz

Tests for a module should ideally cover all code in that module,
i.e., statement coverage should be at 100%.

To measure the test coverage, run::

  $ PYTHONPATH=. pytest --cov=pygraphviz pygraphviz

This will print a report with one line for each file in `pygraphviz`,
detailing the test coverage::

  Name                     Stmts   Miss  Cover
  --------------------------------------------
  pygraphviz/__init__.py      12      4    67%
  pygraphviz/agraph.py      1022    196    81%
  pygraphviz/graphviz.py     179     42    77%
  pygraphviz/scraper.py       26     18    31%
  pygraphviz/testing.py       16      0   100%
  --------------------------------------------
  TOTAL                     1255    260    79%

Adding tests
------------

If you're **new to testing**, see existing test files for examples of things to do.
**Don't let the tests keep you from submitting your contribution!**
If you're not sure how to do this or are having trouble, submit your pull request
anyway.
We will help you create the tests and sort out any kind of problem during code review.

Adding examples
---------------

The gallery examples are managed by
`sphinx-gallery <https://sphinx-gallery.readthedocs.io/>`_.
The source files for the example gallery are ``.py`` scripts in ``examples/`` that
generate one or more figures. They are executed automatically by sphinx-gallery when the
documentation is built. The output is gathered and assembled into the gallery.

You can **add a new** plot by placing a new ``.py`` file in one of the directories inside the
``examples`` directory of the repository. See the other examples to get an idea for the
format.

.. note:: Gallery examples should start with ``plot_``, e.g. ``plot_new_example.py``

General guidelines for making a good gallery plot:

* Examples should highlight a single feature/command.
* Try to make the example as simple as possible.
* Data needed by examples should be included in the same directory and the example script.
* Add comments to explain things are aren't obvious from reading the code.
* Describe the feature that you're showcasing and link to other relevant parts of the
  documentation.

SWIG Wrapper
------------

``pygraphviz`` uses SWIG to generate wrappers around the graphviz C code.
Any modifications to C source code should be made in the SWIG wrapper file,
``graphviz.i``, not ``graphviz_wrap.c`` as this file is auto-generated by
SWIG and any manual changes will be overwritten.
The wrappers can be generated with: ``swig -python pygraphviz/graphviz.i``.
This requires SWIG to be installed.

.. note::

   The wrappers must be generated from the top-level directory, i.e. ::

       swig -python pygraphviz/graphviz.i

   Attempting to regenerate the wrappers from another directory will result
   in broken builds.

Bugs
----

Please `report bugs on GitHub <https://github.com/pygraphviz/pygraphviz/issues>`_.
