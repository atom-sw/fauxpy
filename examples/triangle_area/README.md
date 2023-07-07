# Triangle Area

After installing FauxPy, follow this walkthrough 
to see how it can be used on the two simple examples in this
directory.


## Project Structure

The current example has two 
packages: [code](code) and [tests](tests).
The code package contains the project's source
code, which are two Python 
modules: [code/equilateral.py](code/equilateral.py)
and [code/isosceles.py](code/isosceles.py).
The function in module `equilateral.py`
computes the area of an equilateral triangle
and the function in module `isosceles.py` computes
the area of an isosceles triangle.

Both functions have a bug.  The bug locations are marked with comment
`bug` within source code, and the patch for each bug is in the line
following the bug location, in the form of a comment.

The `tests` package contains the project's
test suite, including two test modules
[tests/test_equilateral.py](tests/test_equilateral.py)
and [tests/test_isosceles.py](tests/test_isosceles.py)
for modules `equilateral.py` and `isosceles.py`,
respectively. Each of these two test modules has two
tests, one failing (i.e., revealing the bug) and
one passing on 
their corresponding modules in package `code`.


## Preparing the Python Environment

We first need to create a 
Python environment for this project, following
the instructions below.

1. Create a Python 3.8 virtual environment `env`. (More recent Python
   versions should also work.)

```bash
python3.8 -m venv env
```

2. Activate environment `env`. Henceforth, all commands assume
   environment `env` is activated.

```bash
source env/bin/activate
```

3. Install FauxPy in environment `env`.

```bash
pip install fauxpy
```


## Locating the Bug in `equilateral.py`

FauxPy is a Pytest plugin, and thus, running it
is similar to running Pytest.
Let's first use Pytest to run all the
tests in package `tests`.

```bash
python -m pytest tests
```

Running the command prints the following message, indicating there
are 4 tests in the project, 2 of which are failing.

```
2 failed, 2 passed in 0.07s
```


### Running Spectrum-Based Fault Localization (SBFL)

Now let's run FauxPy.
FauxPy has only one mandatory command line option
`--src`, which takes a package (directory)
or module (`.py` file) in the current project.
Since the source code of our project is in package `code`,
we pass `code` to `--src`.

```bash
python -m pytest tests --src code
```

By default, FauxPy runs SBFL (spectrum-based fault localization). The
command finishes quickly, printing three lists, one for each SBFL
technique currently supported by FauxPy: Tarantula, Ochiai, and DStar.

The list for Tarantula looks something like
the following. Each row in this list
shows a line number in package `code`
and a number (e.g., 1.1) denoting the line's suspiciousness score
according to Tarantula.

The location of the bug in `equilateral.py` is `equilateral.py::11`,
and the location of the bug in `isosceles.py` is `isosceles.py::6`.
Thus, Tarantula detected the locations of both bugs.

``` 
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::13', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::5', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::11', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)
```

While we just used FauxPy 
to localize multiple bugs in one go,
it is normally preferable to analyze each bug separately from the others.
In FauxPy, we can do this in two ways:

1. Selecting tests

2. Selecting failing tests


#### Selecting tests

The following command runs FauxPy
using only the tests in `tests/test_equilateral.py`.
Since the failing test in `tests/test_equilateral.py`
is related to only a single bug,
FauxPy only localizes that one bug.

```bash
python -m pytest tests/test_equilateral.py --src code
```

Tarantula's output list is now as follows, including only lines in
`equilateral.py`.

```
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::13', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.6)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)
```


#### Selecting failing tests

The following command runs FauxPy using the whole test suite `tests`
but **only** one *failing* test
`tests/test_equilateral.py::test_ea_fail`, which triggers the bug in
`equilateral.py`.

```bash
python -m pytest tests --src code --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

Tarantula's output list is now as follows, including lines from any files but
correctly ranking line `equilateral.py::11` in the top suspiciousness position.

```
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::13', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 1.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::5', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::11', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)
```

As you can see, both approaches report the bug line in
`equilateral.py` as the second element in the output list, tied with
two other lines in the same file. Note that the order of lines with the same suspiciousness score is immaterial; thus, a user would have to go through all three lines to determine if one of them is indeed the correct fault location.


### Running Mutation-Based Fault Localization (MBFL)

To run MBFL techniques, we pass option `--family mbfl`.

```bash
python -m pytest tests --src code --family mbfl --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

The command prints two lists, one for each MBFL
technique currently supported by FauxPy: Metallaxis and Muse.

The list for Muse looks something like the following. 

```
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 0.09090909090909091)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 0.0)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', -0.039660506068057426)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', -0.055524708495280385)
```

Remember that `equilateral.py::11` is the actual bug location in `equilateral.py`.
This line is ranked top, and all other lines have a strictly lower suspiciousness score. Thus, Muse localizes this bug perfectly. 

Note that you cannot compare the value of suspiciousness scores
between techniques: what matters is the ranking of lines by
suspiciousness.


### Running Stack Trace (ST) and Predicate Switching (PS) Fault Localization

To run the ST technique, we pass option `--family st`.

```bash
python -m pytest tests --src code --family st --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

And, to run the PS technique, we pass option `--family ps`:

```bash
python -m pytest tests --src code --family ps --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

Both techniques return an empty output list, which means that
they failed to localize the bug in `equilateral.py`.


## Locating the Bug in `isosceles.py`

Now, let's run some of the techniques on the other bug in `isosceles.py`.

Here is how to run SBFL.  Note that we changed the argument
`--failing-list`, so that we switch to `isosceles.py`'s bug.

```bash
python -m pytest tests --src code --family sbfl --failing-list "[tests/test_isosceles.py::test_ia_crash]"
```

Tarantula's output list is as follows:

```
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::5', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::11', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::8', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', 0.1)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', 0.1)
```

Now we run MBFL:

```bash
python -m pytest tests --src code --family mbfl --failing-list "[tests/test_isosceles.py::test_ia_crash]"
```

Metallaxis's output list is as follows:

```
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.5)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.5)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.5)
```

We could also run ST and PS by simply by replacing `mbfl` with `st` or
`ps` in the previous command. However, ST and PS only need failing
tests; rather than letting FauxPy run all tests and discover which
ones are failing, we can point it directly to only use a specific
failing test, which may save some time if our test suite includes many
passing tests (useless for ST and PS). To this end, we invoke FauxPy
as follows to run ST:

```bash
python -m pytest tests/test_isosceles.py::test_ia_crash --src code --family st
```

Note that we no longer need option `--failing-list`, since the test
suite we are using now contains one single failing test.

ST's output is as follows.

```
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::height::5::8', 1.0)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::isosceles_area::4::11', 0.5)
```

Each entry specifies a *range* of lines (such as from line `5` to line
`8` in the top position). This is because ST cannot distinguish
between statements within the same function, and hence it will always
cluster function bodies together.

Similarly, we run ST with only the failing test as follows:

```bash
python -m pytest tests/test_isosceles.py::test_ia_crash --src code --family ps
```

PS returns an empty list of lines on this example as well. PS can only
localize bugs that originate in branching predicates (such as
conditionals and loop exit conditions), and hence it is a poor match
for these examples.


## Function-level Granularity

In all the examples seen so far, FauxPy ran with statement-level
granularity.  This means that it localizes *lines* within a program.

FauxPy also supports function-level granularity; in this case, it
reports a list of *functions* within a program, each with a certain
suspiciousness score.

To run any of the previous examples with the function-level
granularity, pass option `--granularity function`, which overrides the
default `--granularity statement`.

For instance, here is how to run SBFL with function-level granularity
on `isosceles.py`.

```bash
python -m pytest tests --src code --family sbfl --granularity function --failing-list "[tests/test_isosceles.py::test_ia_crash]"
```

Tarantula's output list is as follows:

```
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::isosceles_area::4::11', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::height::5::8', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::equilateral_area::4::13', 0.1)
```
