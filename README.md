# 1. FauxPy

![GitHub](https://img.shields.io/github/license/atom-sw/fauxpy.git)

The current repository contains the source code of FauxPy,
an automated fault localization tool for Python programs.
FauxPy supports seven well-known fault-localization
techniques in four families (spectrum-based, 
mutation-based, predicate switching, and stack-trace based).
The techniques FauxPy currently supports are as follows:

1. Tarantula
2. Ochiai
3. DStar
4. Metallaxis
5. Muse
6. Predicate switching
7. Stack trace

FauxPy has been tested on 13 real-world Python
programs (e.g., Keras, Pandas, ...), detailed in
our paper ["An Empirical Study of Fault Localization in Python Programs"](#16-citations) 
by Mohammad Rezaalipour and Carlo A. Furia.

In the following video, we demonstrate some of 
FauxPy's fault localization techniques in action.

[![FauxPy Demo](https://img.youtube.com/vi/6ooPPiwd79g/0.jpg)](https://www.youtube.com/watch?v=6ooPPiwd79g)

## 1.1 Installation

To install FauxPy, run the following command:

```
pip install fauxpy
```

We have tested FauxPy on Python 3.6, 3.7, and 3.8.
But it should work on other versions of Python as well.

## 1.2 Using FauxPy

FauxPy is a Pytest plugin, installing which adds new 
command line options to Pytest, allowing users to 
control FauxPy's behaviour.
Thus, using FauxPy is very similar to using Pytest.
For instance, imagine we have a Python project `my_project`
the has two packages: `code`, and `tests`.
Package `code` contains all the source code of the project, and
package `tests` includes the project's test suite.
Executing the following commands run FauxPy
on package `code`, using all the test cases
inside package `tests`, resulting in a list of
line numbers along with their suspiciousness scores.
This list is shown in the command line, and also, saved as
a csv file in a directory next to the project's directory.

```
cd my_project
```

```
python -m pytest --src code
```

The following repository provides step-by-step instructions
on how to use FauxPy on some simple projects.

[https://github.com/atom-sw/fauxpy-examples](https://github.com/atom-sw/fauxpy-examples)

It is advised to first take a look at the repository mentioned above, 
before going any further with the instructions in the current repository,
especially, if you do not know much about fault localization in general.

## 1.3 Command Line Options

FauxPy adds 7 command line options to Pytest, 
explained in the rest of this section.

The following command shows an example of using all
of FauxPy's options at the same time. However, many of
these options are not mandatory and can be skipped
based on the usage scenario users have in mind.

```
python -m pytest tests \
  --src code \
  --family sbfl \
  --exclude "[code/package_x, code/module_x.py]" \
  --granularity statement \
  --top-n 3 \
  --failing-list "[tests/test_module_y.py::test_function_z]"
```

### 1.3.1 Targeted Source Code

- **Name:** `--src`

- **Type:** Mandatory

Option `--src` is the only mandatory command line option of FauxPy.
It takes a relative path to a Python package or module
within the project at hand. FauxPy only considers
program entities in the package or module passed 
as `--src` while
performing fault localization.
If users want to involve the whole project in
FauxPy's fault localization session, they can pass `.` 
(current directory's path) as the argument.


### 1.3.2 Fault Localization Family

- **Name:** `--family`

- **Choices:** {`sbfl`, `mbfl`, `ps`, `st`}

- **Type:** Optional

- **Default:** `sbfl`

FauxPy supports four fault localization families: SBFL, MBFL, PS, and ST.
Using option `--family`, users can decided which fault localization
family should be used during their fault localization session.
Option `--family` is an optional argument. If it is not provided,
FauxPy picks `sbfl` by default.


### 1.3.3 Fault Localization Granularity

- **Name:** `--granularity`

- **Choices:** {`statement`, `function`}

- **Type:** Optional

- **Default:** `statement`

The current version of FauxPy supports two different 
granularity levels: statement, and function.
Using statement-level granularity, FauxPy's default choice,
FauxPy outputs a list of line numbers and their suspiciousness scores.
Using the function-level granularity, FauxPy returns suspicious functions
instead of line numbers.


### 1.3.4 Excluded Items

- **Name:** `--exclude`

- **Type:** Optional

- **Default:** No packages and modules are excluded

Sometimes, users need to exclude a package or module from
a fault localization session. For instance, if `.` is passed to
option `--src`, users might want to exclude package `tests`
(project's test suite) or directory `env` 
(virtual environment of the project) from their
fault localization session. If such items are not excluded,
FauxPy includes in its output the program entities in these
directories, as well. In such cases, users can use option `--exclude`.
This option takes a comma separated list of relative paths to
directories that are supposed to be excluded.

For instance, the following command runs FauxPy on
the whole project but the two directories `env` and `tests`.

```
python -m pytest tests \
  --src . \
  --exclude "[env, tests]"
```

### 1.3.5 Targeted Failing Tests

- **Name:** `--failing-list`

- **Type:** Optional

- **Default:** all the failing tests in the test suite.

Technically, FauxPy can perform fault localization
when the project at hand has multiple bugs, revealed 
by different failing tests. How fault localization techniques
behave in this situation requires further research.
In any case, FauxPy can be configured to only consider
certain failing tests during a fault localization session, providing
option `--failing-list`. We call these tests *"targeted failing tests"*.
If this option is used, FauxPy only considers the targeted failing tests
while computing suspiciousness scores, avoiding the noise
caused by other bugs and their corresponding failing tests.
If this option is not used, FauxPy includes in
the fault localization session all the failing tests
in the given test suite.

The argument passed to this option is a comma seperated list
of test functions in the Pytest format. A test in Pytest is identified
by its path, class name, and function name in the following format:

`[FILE_PATH]::[CLASS_NAME]::[FUNCTION_NAME]`

For example, Pytest identifies a test function named
`test_read_file`, whose 
relative path is `test/test_common/test_file.py`,
and is inside class `Test_IO` as follows:

`test/test_common/test_file.py::Test_IO::test_read_file`

If the targeted failing test is parametrized, the
parameter part of the name must be
removed while it is passed to `--failing-list`.
For instance, if test `test/test_tuils.py::test_addition[1-2-3]`
is a targeted failing test,`test/test_tuils.py::test_addition` must be
one of the elements in the list passed to `--failing-list`.

FauxPy provides another option `--failing-file`.
The functionality of this option is the same as
that of `--failing-list`; but option `--failing-file`
takes a path to a file that includes the targeted failing
tests, each in a separate line.


### 1.3.6 Top n Results

- **Name:** `--top-n`

- **Choices:** {-1} &#8746; Integer[1, Inf]

- **Type:** Optional

- **Default:** -1

Sometimes the list of program entities FauxPy outputs has too many records.
In this case, option `--top-n` can be used to shorten the list.
This option takes an integer greater than 0, indicating the number of records
that FauxPy is expected to include in its output.
Passing -1, the default option, means FauxPy must return all the records.

### 1.3.7 Test-suite Subset

FauxPy allows users to run the whole test suite
in a fault localization session, or just a subset of it such as
a certain test package, test module, test function
or even a combination of them.
For instance, the following command runs FauxPy while using only tests
in package `tests/package_x`, module `tests/test_y.py`, 
and test function `tests/test_z.py::test_function_t`.
In this case, FauxPy only considers these tests in the
fault localization session.

```
python -m pytest tests/package_x \
                 tests/test_y.py \
                 tests/test_z.py::test_function_t \
                 --src code
```


## 1.4 Guidelines

As the first step of every fault localization session, FauxPy
runs the whole test suite passed to it.
Unlike SBFL and MBFL techniques, the two families ST and PS
only use failing tests to perform fault localization.
These two techniques simply ignore the information provided
by running passing tests.
Thus, it is better to run PS and ST using only the targeted failing
tests in the test suite. In this way, FauxPy performs more efficiently;
however, the result is going to be the same even if the passing tests are also
involved. Section [1.3.7 Test-suite Subset](#136-test-suite-subset) explains
how the test suite size can be controlled.


## 1.5 Limitations

1. Both SBFL and MBFL families use [Coverage.py](https://coverage.readthedocs.io),
through its API,
to collect execution
traces. So, any limitation of Coverage.py is a
limitation of these two families.

2. The Stack Trace (ST) family does not work properly
if Pytest's option `--tb=native` is used.
Do not use `--tb=native` neither as a command line argument
nor as included in a `pytest.ini` file.

3. FauxPy is not compatible with `pytest-sugar`.
So, in order to use FauxPy, `pytest-sugar` must be uninstalled
(run `pip uninstall pytest-sugar`) from your Python environment.

## 1.6 Citations

In the following paper, we used FauxPy
to conduct an empirical
study of fault localization:

[An Empirical Study of Fault Localization in Python Programs:](https://arxiv.org/abs/2305.19834)

```
@misc{Rezaalipour:2023,
      title={An Empirical Study of Fault Localization in Python Programs}, 
      author={Mohammad Rezaalipour and Carlo A. Furia},
      year={2023},
      eprint={2305.19834},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```

The following repository contains the replication package of
this paper. This replication package contains 540 bash scripts,
each running FauxPy on a real-world program.
You can run some of them to see FauxPy's behaviour
on real-world programs (see Section 
[3. Running
the experiments
](https://github.com/atom-sw/fauxpy-experiments#3-running-the-experiments) in
the following repository).

https://github.com/atom-sw/fauxpy-experiments


# 2. Mirrors

The current repository is a public mirror of
our internal private repository.
We have two public mirrors, which are as follows:

- https://github.com/atom-sw/fauxpy
- https://github.com/mohrez86/fauxpy
