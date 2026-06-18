pygraphviz 2.0rc3
=================

We're happy to announce the release of pygraphviz 2.0rc3!

Enhancements
------------

- Add aarch64 wheels for linux to cibuildwheel (`#591 <https://github.com/pygraphviz/pygraphviz/pull/591>`_).
- ENH: Export version info from wrapped graphviz (`#624 <https://github.com/pygraphviz/pygraphviz/pull/624>`_).

Bug Fixes
---------

- More precise allocation for string copy in SWIG glue (`#559 <https://github.com/pygraphviz/pygraphviz/pull/559>`_).

Documentation
-------------

- Avoid adding benchmark results to docs (`#544 <https://github.com/pygraphviz/pygraphviz/pull/544>`_).
- DOC: remove pip install as recommendation (`#551 <https://github.com/pygraphviz/pygraphviz/pull/551>`_).
- DOC: update install docs with link to graphviz 12.2.1 for windows (`#552 <https://github.com/pygraphviz/pygraphviz/pull/552>`_).
- Update docs for 2.0 (`#609 <https://github.com/pygraphviz/pygraphviz/pull/609>`_).

Maintenance
-----------

- Drop support for Python 3.10 (SPEC 0) (`#543 <https://github.com/pygraphviz/pygraphviz/pull/543>`_).
- Bump up CI builds, test with latest windows graphviz release (`#550 <https://github.com/pygraphviz/pygraphviz/pull/550>`_).
- Update fedora tests (`#554 <https://github.com/pygraphviz/pygraphviz/pull/554>`_).
- Update pre-commit (`#557 <https://github.com/pygraphviz/pygraphviz/pull/557>`_).
- Update pyproject.toml to comply with PEP 639 (`#578 <https://github.com/pygraphviz/pygraphviz/pull/578>`_).
- CI: Github actions uses MacOS 15; update macports (`#579 <https://github.com/pygraphviz/pygraphviz/pull/579>`_).
- Add support for Python 3.14 (`#576 <https://github.com/pygraphviz/pygraphviz/pull/576>`_).
- Use pytest's tmp_path fixture (`#561 <https://github.com/pygraphviz/pygraphviz/pull/561>`_).
- Bump webfactory/ssh-agent from 0.9.0 to 0.9.1 (`#562 <https://github.com/pygraphviz/pygraphviz/pull/562>`_).
- Bump scientific-python/attach-next-milestone-action from bc07be829f693829263e57d5e8489f4e57d3d420 to c9cfab10ad0c67fed91b01103db26b7f16634639 (`#560 <https://github.com/pygraphviz/pygraphviz/pull/560>`_).
- Bump actions/checkout from 4 to 6 (`#581 <https://github.com/pygraphviz/pygraphviz/pull/581>`_).
- Bump actions/setup-python from 5 to 6 (`#580 <https://github.com/pygraphviz/pygraphviz/pull/580>`_).
- CI: test CI with choco (`#556 <https://github.com/pygraphviz/pygraphviz/pull/556>`_).
- Drop support for python 3.11 (SPEC 0) (`#582 <https://github.com/pygraphviz/pygraphviz/pull/582>`_).
- CI: fix silent Windows failures and duplicate PR runs (`#588 <https://github.com/pygraphviz/pygraphviz/pull/588>`_).
- Bump webfactory/ssh-agent from 0.9.1 to 0.10.0 (`#586 <https://github.com/pygraphviz/pygraphviz/pull/586>`_).
- CI: cibuildwheel take 4 (`#583 <https://github.com/pygraphviz/pygraphviz/pull/583>`_).
- MAINT: Add swig step to build (`#590 <https://github.com/pygraphviz/pygraphviz/pull/590>`_).
- Bump conda-incubator/setup-miniconda from 3 to 4 (`#595 <https://github.com/pygraphviz/pygraphviz/pull/595>`_).
- Bump actions/upload-artifact from 4 to 7 (`#594 <https://github.com/pygraphviz/pygraphviz/pull/594>`_).
- Bump actions/download-artifact from 4 to 8 (`#593 <https://github.com/pygraphviz/pygraphviz/pull/593>`_).
- Update setuptools version requirement in pyproject.toml (`#602 <https://github.com/pygraphviz/pygraphviz/pull/602>`_).
- Graphviz support across v13 API change (`#603 <https://github.com/pygraphviz/pygraphviz/pull/603>`_).
- CI: Rm fedora/macports testing workflows (`#606 <https://github.com/pygraphviz/pygraphviz/pull/606>`_).
- CI: Build macos wheels against macos 11, and move cibuildwheel to release pipeline (`#604 <https://github.com/pygraphviz/pygraphviz/pull/604>`_).
- More 2.0 cleanups (`#610 <https://github.com/pygraphviz/pygraphviz/pull/610>`_).
- Update type of id param to IDTYPE in swig wrapper (`#611 <https://github.com/pygraphviz/pygraphviz/pull/611>`_).
- Add Python 3.11 support for 2.0 release (`#613 <https://github.com/pygraphviz/pygraphviz/pull/613>`_).
- CONF: escaped slashes in windows pathspec (`#614 <https://github.com/pygraphviz/pygraphviz/pull/614>`_).
- TST: Add tests for ``tred`` method (`#615 <https://github.com/pygraphviz/pygraphviz/pull/615>`_).
- PKG: Include examples/\*.txt in MANIFEST.in (`#617 <https://github.com/pygraphviz/pygraphviz/pull/617>`_).
- TST: Add unit test for gh-123 (`#622 <https://github.com/pygraphviz/pygraphviz/pull/622>`_).
- TST: Add example from gh-162 as unit test (`#621 <https://github.com/pygraphviz/pygraphviz/pull/621>`_).
- CI: See what happens when freethreading enabled (`#616 <https://github.com/pygraphviz/pygraphviz/pull/616>`_).
- TST: Attempt regression test for gh-585 (`#618 <https://github.com/pygraphviz/pygraphviz/pull/618>`_).
- TST: Assert hex colors don't cause runtime warnings (`#619 <https://github.com/pygraphviz/pygraphviz/pull/619>`_).
- Bump packaged graphviz version (`#623 <https://github.com/pygraphviz/pygraphviz/pull/623>`_).
- TST: Add regression test for gh-171 (`#620 <https://github.com/pygraphviz/pygraphviz/pull/620>`_).

Other
-----

- WIP: Using cgraph/gvc lib interface for wheel building (`#421 <https://github.com/pygraphviz/pygraphviz/pull/421>`_).
- docs: replace deprecated --global-option with --config-settings (`#574 <https://github.com/pygraphviz/pygraphviz/pull/574>`_).
- Fix FILE* resource leak in agwrite() wrapper (`#585 <https://github.com/pygraphviz/pygraphviz/pull/585>`_).
- CI: Build macos wheels with quartz; no gd (`#608 <https://github.com/pygraphviz/pygraphviz/pull/608>`_).

Contributors
------------

13 authors added to this release (alphabetically):

- `@dependabot[bot] <https://github.com/apps/dependabot>`_
- Bryan Gin-ge Chen (`@bryangingechen <https://github.com/bryangingechen>`_)
- Cat Chenal (`@CatChenal <https://github.com/CatChenal>`_)
- Dan Schult (`@dschult <https://github.com/dschult>`_)
- Jarrod Millman (`@jarrodmillman <https://github.com/jarrodmillman>`_)
- Matthew Fernandez (`@Smattr <https://github.com/Smattr>`_)
- Matěj Cepl (`@mcepl <https://github.com/mcepl>`_)
- Miroslav Šedivý (`@eumiro <https://github.com/eumiro>`_)
- Mridul Seth (`@MridulS <https://github.com/MridulS>`_)
- Rob Taylor (`@robtaylor <https://github.com/robtaylor>`_)
- Ross Barnowski (`@rossbar <https://github.com/rossbar>`_)
- Yatin (`@YatinAdityaT <https://github.com/YatinAdityaT>`_)
- Ülgen Sarıkavak (`@ulgens <https://github.com/ulgens>`_)

5 reviewers added to this release (alphabetically):

- Dan Schult (`@dschult <https://github.com/dschult>`_)
- Jarrod Millman (`@jarrodmillman <https://github.com/jarrodmillman>`_)
- Matthew Fernandez (`@Smattr <https://github.com/Smattr>`_)
- Mridul Seth (`@MridulS <https://github.com/MridulS>`_)
- Ross Barnowski (`@rossbar <https://github.com/rossbar>`_)

_These lists are automatically generated, and may not be complete or may contain
duplicates._
