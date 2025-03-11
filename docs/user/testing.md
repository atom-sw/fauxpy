# Testing FauxPy

[![FauxPy-Test - Repository](https://img.shields.io/badge/FauxPy--Test-Repository-2ea44f)](https://github.com/mohrez86/fauxpy-test)

*Our top priority* is that FauxPy works seamlessly with real-world Python projects.
To ensure that, we test FauxPy with a
range of real-world projects before each release on PyPI. For this
purpose, we maintain a dedicated repository,
[FauxPy-Test](https://github.com/mohrez86/fauxpy-test).

## About the Test Repository

The *FauxPy-Test* repository contains code and data for testing new
versions of FauxPy with a set of real-world Python projects.
Currently, we use the following projects from
[BugsInPy](https://github.com/soarsmu/BugsInPy):

-   [black](https://github.com/psf/black)
-   [cookiecutter](https://github.com/cookiecutter/cookiecutter)
-   [fastapi](https://github.com/tiangolo/fastapi)
-   [httpie](https://github.com/jakubroztocil/httpie)
-   [keras](https://github.com/keras-team/keras)
-   [luigi](https://github.com/spotify/luigi)
-   [pandas](https://github.com/pandas-dev/pandas)
-   [sanic](https://github.com/huge-success/sanic)
-   [spaCy](https://github.com/explosion/spaCy)
-   [thefuck](https://github.com/nvbn/thefuck)
-   [tornado](https://github.com/tornadoweb/tornado)
-   [tqdm](https://github.com/tqdm/tqdm)
-   [youtube-dl](https://github.com/ytdl-org/youtube-dl)

The repository provides detailed instructions for testing
FauxPy with these projects, focusing on two main goals:  

- **Robustness:** Ensure the new version runs on real-world programs without crashing.
- **Functionality:** Confirm that the results produced by the new version are consistent
    with those from the previous version to ensure no
    regressions occurred during development.

## Extending the Test Repository

We plan to extend the FauxPy-Test repository by adding more
real-world Python projects to improve FauxPy's reliability.
These newly added
projects can also be used for further research in software analysis.
If you face a situation where FauxPy does not work with any project,
whether it is listed here or not, please let us know via our [Discussions
section](https://github.com/mohrez86/fauxpy/discussions).
