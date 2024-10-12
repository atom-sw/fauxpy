# FauxPy

[![PyPI version](https://badge.fury.io/py/fauxpy.svg)](https://badge.fury.io/py/fauxpy)
[![GitHub](https://img.shields.io/github/license/atom-sw/fauxpy)](LICENSE)
[![Downloads](https://static.pepy.tech/badge/fauxpy)](https://pepy.tech/project/fauxpy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/fauxpy/badge/?version=latest)](https://fauxpy.readthedocs.io/en/latest/?badge=latest)
[![FauxPy-Test - Repository](https://img.shields.io/badge/FauxPy--Test-Repository-2ea44f)](https://github.com/mohrez86/fauxpy-test)

FauxPy (pronounced: "foh pie") is an 
automated fault localization tool 
for Python programs. 
This repository includes 
FauxPy's source code and 
instructions to install 
and use the tool.

- For comprehensive documentation, visit
[FauxPy documentation](https://fauxpy.readthedocs.io/).
- You can also participate in our 
[Discussions section](https://github.com/mohrez86/fauxpy/discussions) 
for questions, feedback, and more. 
- If you encounter any issues, feel free
to open an issue on our 
[GitHub repository](https://github.com/mohrez86/fauxpy/issues).

## Features

FauxPy supports seven classic 
fault-localization techniques 
in four families:

1. **SBFL** (spectrum-based) techniques Tarantula, Ochiai, and DStar.
2. **MBFL** (mutation-based) techniques Metallaxis and Muse.
3. **PS** (predicate switching) fault localization.
4. **ST** (stack-trace) fault localization.

It supports fault localization at the
level of **statements** 
(statement-level granularity) and at
the level of **functions** 
(function-level granularity).

FauxPy is based on dynamic analysis 
and can use tests written in 
the format of 
[Pytest](https://pytest.org), 
[Unittest](https://docs.python.org/3/library/unittest.html),
and [Hypothesis](https://hypothesis.works/).

## Installation

FauxPy is [available on 
PyPI](https://pypi.org/project/fauxpy/), 
so you can install it using `pip`:

```bash
pip install fauxpy
```

To install the latest (unreleased) 
version, use the following command:

```bash
pip install git+https://github.com/atom-sw/fauxpy
```

We have mainly tested FauxPy with 
Python 3.6, 3.7, and 3.8, 
but it should also work on later 
Python versions.

## Getting Started

Check out this short 
[demo video](https://www.youtube.com/watch?v=6ooPPiwd79g) 
of FauxPy in action (~16 minutes).

[![FauxPy Demo](https://img.youtube.com/vi/6ooPPiwd79g/0.jpg)](https://www.youtube.com/watch?v=6ooPPiwd79g)

![YouTube Video Views](https://img.shields.io/youtube/views/6ooPPiwd79g)

The directory 
[examples/triangle_area](examples/triangle_area) 
includes a tutorial example of 
using FauxPy. 
Follow the instructions in the 
[`README.md`](examples/triangle_area/README.md).
Here is a [demo video](https://youtu.be/O4T7w-U8rZE) 
of part of this 
example (~ 5 minutes).

[![Triangle Area Example](https://img.youtube.com/vi/O4T7w-U8rZE/0.jpg)](https://youtu.be/O4T7w-U8rZE)

![YouTube Video Views](https://img.shields.io/youtube/views/O4T7w-U8rZE)

## Citing FauxPy and References

### Technical Report

The technical report 
[FauxPy: A Fault Localization Tool for 
Python](https://arxiv.org/abs/2404.18596) 
presents FauxPy in detail, including 
its implementation, architecture, 
and instructions on how to use it. 
You can cite this technical 
report as follows:

```bibtex
@misc{PythonFL-FauxPy-Tool,
  title={{FauxPy}: A Fault Localization Tool for {P}ython},
  author={Mohammad Rezaalipour and Carlo A. Furia},
  year={2024},
  eprint={2404.18596},
  archivePrefix={arXiv},
  primaryClass={cs.SE},
  url={https://arxiv.org/abs/2404.18596}
}
```

### Empirical Study

The paper 
[An Empirical Study of Fault 
Localization in Python 
Programs](https://doi.org/10.1007/s10664-024-10475-3) presents an empirical study where we applied FauxPy to 135 bugs across 13 real-world Python programs from the curated collection [BugsInPy](https://github.com/soarsmu/BugsInPy). This paper is published in the *Empirical Software Engineering* (EMSE) journal. You can cite this empirical work as follows:

```bibtex
@article{Rezaalipour:2024,
  title={An empirical study of fault localization in {P}ython programs},
  author={Rezaalipour, Mohammad and Furia, Carlo A.},
  journal={Empirical Software Engineering},
  volume={29},
  number={4},
  pages={92},
  year={2024},
  publisher={Springer}
}
```

## Mirrors

This repository is a public mirror of 
(part of) FauxPy's private development 
repository. There are two public 
mirrors, whose content 
is identical:

- https://github.com/atom-sw/fauxpy
- https://github.com/mohrez86/fauxpy
