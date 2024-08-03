# FauxPy

[![PyPI version](https://badge.fury.io/py/fauxpy.svg)](https://badge.fury.io/py/fauxpy)
![GitHub](https://img.shields.io/github/license/atom-sw/fauxpy)
[![Downloads](https://static.pepy.tech/badge/fauxpy)](https://pepy.tech/project/fauxpy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/fauxpy/badge/?version=latest)](https://fauxpy.readthedocs.io/en/latest/?badge=latest)
[![FauxPy-Test - Repository](https://img.shields.io/badge/FauxPy--Test-Repository-2ea44f)](https://github.com/mohrez86/fauxpy-test)


FauxPy (pronounced: "foh pie")
is an automated fault localization tool for Python programs.
This repository includes FauxPy's source code, and instructions
to install and use the tool.

*For comprehensive documentation, visit
[FauxPy's documentation](https://fauxpy.readthedocs.io).*


## Features

FauxPy supports seven classic fault-localization techniques in four families:

1. **SBFL** (spectrum-based) techniques Tarantula, Ochiai, and DStar.

2. **MBFL** (mutation-based) techniques Metallaxis and Muse.

3. **PS** (predicate switching) fault localization.

4. **ST** (stack-trace) fault localization.

It supports fault localization 
at the level of **statements** (statement-level granularity)
and at the level of **functions** (function-level granularity).

FauxPy is based on dynamic analysis, 
and can use tests written in the format of 
[Pytest](https://pytest.org), 
[Unittest](https://docs.python.org/3/library/unittest.html),
and [Hypothesis](https://hypothesis.works/).


## Installation

FauxPy is [on PyPI](https://pypi.org/project/fauxpy/),
so you can install it using `pip`:

```bash
pip install fauxpy
```

To install the latest (unreleased) version, use the following command:

```bash
pip install git+https://github.com/atom-sw/fauxpy
```

We mainly tested FauxPy with Python 3.6, 3.7, and 3.8,
but it should also work on later Python versions.


## Getting Started

Here is a short [demo video](https://www.youtube.com/watch?v=6ooPPiwd79g) of FauxPy
in action (~16 minutes).

[![FauxPy Demo](https://img.youtube.com/vi/6ooPPiwd79g/0.jpg)](https://www.youtube.com/watch?v=6ooPPiwd79g)

![YouTube Video Views](https://img.shields.io/youtube/views/6ooPPiwd79g)

Directory [examples/triangle_area](examples/triangle_area) includes a tutorial example of using FauxPy. Follow the instructions in the [`README.md`](examples/triangle_area/README.md).
Here is a [demo video](https://youtu.be/O4T7w-U8rZE) of part of 
this example (~ 5 minutes).

[![Triangle Area Example](https://img.youtube.com/vi/O4T7w-U8rZE/0.jpg)](https://youtu.be/O4T7w-U8rZE)

![YouTube Video Views](https://img.shields.io/youtube/views/O4T7w-U8rZE)


## Using FauxPy

FauxPy is implemented as a Pytest plugin, thus using FauxPy boils down
to passing some custom options to Pytest.

To run FauxPy, you must first `cd` to the project's directory `$PROJECT`:

```bash
cd $PROJECT
```

Then, the basic command to run FauxPy is the following, where
`$SOURCE` is the relative path to a Python package or module
inside `$PROJECT`:

```bash
python -m pytest --src $SOURCE
```

This performs statement-level spectrum-based fault localization on the
Python project in directory `$PROJECT`, using any Pytest tests in
there. 

The output is a list of program entities with their suspiciousness
score, sorted from most to least suspicious. The output is printed on
screen, and also saved in a directory `FauxPyReport_...` created in
`$PROJECT`'s parent directory.

This is the complete list of command-line arguments to control FauxPy.

```bash
python -m pytest \
	   $TESTS \
	   --src $SRC \
	   --family $FAMILY \
	   --exclude "[$EXCLUDE1, $EXCLUDE2, ...]" \
	   --granularity $GRANULARITY \
	   --top-n $N \
	   --failing-list "[$FAIL1, $FAIL2, ...]" \
	   --failing-file $FAIL
```

### `--src`: Program Source Code

Option `--src $SRC` runs FauxPy on the project considering only
the program entities under *relative* path
`$SRC`. Precisely, `$SRC` can point to a whole project, or an
individual package (subdirectory) or modules (source-code file) within
it.

In particular, option `--src .` runs FauxPy on the project in the
current directory, considering the program entites in all
the Python modules and packages existing within project.

Option `--src` is the only mandatory argument to run FauxPy.


### `--family`: Fault Localization Family

Option `--family $FAMILY` runs FauxPy using the `$FAMILY` fault
localization family of techniques. 
FauxPy currently supports families: `sbfl` (the default), `mbfl`, `ps`, and `st`.


### `--granularity`: Entity Granularity

Option `--granularity $GRANULARITY` runs FauxPy using `$GRANULARITY`
as program entities to localize. FauxPy currently supports
granularities: `statement` (the default), and `function`.

With *statement*-level granularity, FauxPy outputs a list of program locations (i.e., line numbers) that may be responsible for the fault.
With *function*-level granularity, FauxPy outputs a list of functions that may be responsible for the fault.


### `--exclude`: Exclude Directories or Files

Option `--exclude "[$EXCLUDE1, $EXCLUDE2, ...]"` ignores entities in `$EXCLUDE1`,
`$EXCLUDE2`, and so on when performing fault localization. 

Each element of the comma-separated list must be a path relative to
the analyzed project's root directory of a directory (package) or
Python source file (module).

For instance, the following command runs fault localization on the
project in the current directory, skipping directories `env` and
`tests`, and module `utilities`:

```bash
python -m pytest --src . --exclude "[env, tests, utilities.py]"
```

### `--failing-list`: Select Failures

Option `--failing-list "[$FAIL1, $FAIL2, ...]` *only* uses tests
`$FAIL1`, `$FAIL2`, and so on as *failing* tests when performing fault
localization. 

Each element of the comma-separated list must be 
the fully-qualified name of a test function in the analyzed project,
using the Pytest format `<FILE_PATH>::<CLASS_NAME>::<FUNCTION_NAME>`, 
where the `<CLASS_NAME>::` can be omitted if the test function is
top-level. 

For instance, the following command runs fault localization on the
project in the current directory, using *only* test function
`test_read_file` in class `Test_IO` as failing test:

```bash
python -m pytest --src . \
	   --failing-list "[`test/test_common/test_file.py::Test_IO::test_read_file`]"
```

Selecting specific failing tests is especially useful when
there are multiple, different faults, triggered by different
tests. Fault localization techniques are usually designed to work
under the assumption that they analyze each fault in isolation. If
the analyzed project includes multiple faults, it is advisable to
select a subset of the failing tests that trigger a single fault,
so that fault localization can perform more accurately.

### `--failing-file`: Select Failures

Option `--failing-file $FAIL` 
is the same as option `--failing-list`.
But instead of taking a list of failing tests,
it takes the path of a file relative to the analyzed project's root directory.
In file `$FAIL`, every failing test must be in a separate line.


### `--top-n`: Output List Size

Option `--top-n $N` only reports up to `$N` suspicious program
entities (statements or functions). `$N` must be a positive integer,
or `-1` (the default: no limit).


### Positional Argument: Tests

Optional positional argument `$TESTS`, specified just after `pytest`,
runs FauxPy using the tests found under path `$TESTS`. 
If this argument is missing, FauxPy will use any tests found in the
analyzed project.

`$TESTS` must be a path relative to the analyzed project's root
directory of a directory (package), a Python source file (module), or
the fully-qualified name of a test function in the analyzed project,
using the Pytest format `<FILE_PATH>::<CLASS_NAME>::<FUNCTION_NAME>`,
where the `<CLASS_NAME>::` can be omitted if the test function is
top-level.

The positional argument can be repeated to select tests at different locations.
For instance, the following command runs FauxPy using only tests
in package `tests/package_x`, module `tests/test_y.py`, 
and test function `tests/test_z.py::test_function_t`.

```bash
python -m pytest tests/package_x \
	   tests/test_y.py \
	   tests/test_z.py::test_function_t \
	   --src $SRC
```

Stack-trace and predicate switching fault localization only need to
run failing tests. If a project has many tests, but only a few are
failing, ST and PS fault localization will run more quickly if we
pass the failing tests' location using this feature. If
we don't, FauxPy will still have to run all tests, just to discover
which ones are failing and can be used for ST or PS fault
localization.


## Limitations

The current version of FauxPy has a couple of known limitations:

1. The implementation of SBFL and MBFL uses
   [Coverage.py](https://coverage.readthedocs.io) through its API to
   collect execution traces. Thus, FauxPy inherits any limitation of Coverage.py.

2. The implementation of ST does not work properly if Pytest's option
   `--tb=native` is enabled (as a command-line argument or in a
   `pytest.ini` file).

3. FauxPy is incompatible with Pytest plugin
   [`pytest-sugar`](https://pypi.org/project/pytest-sugar/). If you
   want to use FauxPy, remove `pytest-sugar` from your Python
   environment.


## Citing FauxPy and References

### Technical Report

The technical report 
[FauxPy: A Fault Localization Tool for Python](https://arxiv.org/abs/2404.18596) 
presents FauxPy in detail, including 
its implementation, architecture, and 
instructions on how to use it. 
You can cite this technical report as follows:

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
[An Empirical Study of Fault Localization in Python Programs](https://doi.org/10.1007/s10664-024-10475-3) 
presents an empirical study where we 
applied FauxPy to 135 bugs across 13 real-world Python 
programs from the curated collection 
[BugsInPy](https://github.com/soarsmu/BugsInPy). 
This paper is published in the 
*Empirical Software Engineering* (EMSE) journal. 
You can cite this empirical work as follows:

Rezaalipour, M., Furia, C. A. An empirical study of fault localization in Python programs. *Empirical Software Engineering*, 29, 92 (2024). https://doi.org/10.1007/s10664-024-10475-3

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

This repository is a public mirror of (part of)
FauxPy's private development repository.
There are two public mirrors, whose content is identical:

- https://github.com/atom-sw/fauxpy
- https://github.com/mohrez86/fauxpy
