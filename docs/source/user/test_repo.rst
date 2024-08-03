=================
Extensive Testing
=================

.. https://michaelcurrin.github.io/badge-generator
.. image:: https://img.shields.io/badge/FauxPy--Test-Repository-2ea44f
   :target: https://github.com/mohrez86/fauxpy-test
   :alt: FauxPy-Test - Repository

*Our top priority* is that FauxPy
works with real-world Python projects.
To ensure that, we rigorously test
FauxPy's functionality across a range
of real-world projects before
each release on PyPI.
For this purpose, we maintain a
dedicated repository,
`FauxPy-Test <https://github.com/mohrez86/fauxpy-test>`_.

About the Test Repository
=========================

The *FauxPy-Test* repository contains code and data
for testing new versions of FauxPy on
a selection of real-world Python projects.
Currently, our tests cover the
following projects from the
`BugsInPy <https://github.com/soarsmu/BugsInPy>`_
framework of real-world Python
projects and bugs:

- `black <https://github.com/psf/black>`_
- `cookiecutter <https://github.com/cookiecutter/cookiecutter>`_
- `fastapi <https://github.com/tiangolo/fastapi>`_
- `httpie <https://github.com/jakubroztocil/httpie>`_
- `keras <https://github.com/keras-team/keras>`_
- `luigi <https://github.com/spotify/luigi>`_
- `pandas <https://github.com/pandas-dev/pandas>`_
- `sanic <https://github.com/huge-success/sanic>`_
- `spaCy <https://github.com/explosion/spaCy>`_
- `thefuck <https://github.com/nvbn/thefuck>`_
- `tornado <https://github.com/tornadoweb/tornado>`_
- `tqdm <https://github.com/tqdm/tqdm>`_
- `youtube-dl <https://github.com/ytdl-org/youtube-dl>`_

The FauxPy-Test repository provides detailed
instructions on running FauxPy with these
projects to verify two key aspects:

1. Ensure the new version runs
   on real-world programs without crashing.

2. Confirm that the results produced by the
   new version are consistent with those
   from the previous version. This helps
   us ensure no regressions occurred
   during development.

Extending the Test Repository
=============================

We plan to extend the
FauxPy-Test repository
by including more real-world Python projects
in the future to further enhance our
confidence in FauxPy's reliability.
Additionally, the newly added
projects can be used for further research
in the software analysis domain.

If you discover any case where FauxPy
does not work
with a project, whether it's one
of the included ones or a different
real-world project,
please let us know so that
we can fix bugs, improve FauxPy, and add
new projects to our test repository.

Email: **rezaalipour [dot] mohammad [at] gmail [dot] com**
