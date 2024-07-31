==============
Extensive Test
==============

*Our top priority* is that FauxPy
works on real-world Python projects.
To ensure that, we verify that FauxPy
maintains its functionality across a range
of real-world projects before
every release on PyPI.
We have a
`separate repository <https://github.com/mohrez86/fauxpy-test>`_,
dedicated to this goal.

About the Test Repository
=========================

This repository contains code and data
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

The repository provides detailed instructions
on running FauxPy on these projects,
ensuring each new version undergoes thorough testing
against real-world code. This process verifies that
the results produced by the new version of FauxPy
align with those of previous versions,
confirming that no regressions have been introduced
during the development of the new version.

Extending the Test Repository
=============================

We plan to extend this test repository
by including more real-world Python projects
in the future, further enhancing our
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
