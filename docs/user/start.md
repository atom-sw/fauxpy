# Quick Start

This page provides two examples demonstrating how to use FauxPy:

- [Example 1](#example-1) shows how to use
  the four classic fault localization families supported by FauxPy,
  how to apply different granularity levels,
  and best practices for using FauxPy and fault localization in general.
- [Example 2](#example-2) shows
  how to use FauxPy's **Mutation Strategy** feature to perform
  Mutation-Based Fault Localization (MBFL) using LLMs.

## Example 1

The following walkthrough starts by introducing the project structure of 
[Example 1](https://github.com/atom-sw/fauxpy/tree/main/examples/example1), 
and then provides instructions on setting up an environment
and running FauxPy with this example.

### Project Structure

Figure 1 shows *Example 1*'s project structure.
This project has two packages:
[code](https://github.com/atom-sw/fauxpy/tree/main/examples/example1/code)
and
[tests](https://github.com/atom-sw/fauxpy/tree/main/examples/example1/tests).
The code package contains the project's source code, which are two
Python modules:
[code/equilateral.py](https://github.com/atom-sw/fauxpy/blob/main/examples/example1/code/equilateral.py)
and
[code/isosceles.py](https://github.com/atom-sw/fauxpy/blob/main/examples/example1/code/isosceles.py),
demonstrated in Figures 2 and 3, respectively. The function in module
`equilateral.py` computes the area of an equilateral triangle and the
function in module `isosceles.py` computes the area of an isosceles
triangle.


``` title="Figure 1: Project structure of Example 1."
example1/
├── code/
│   ├── __init__.py
│   ├── equilateral.py
│   └── isosceles.py
└── tests/
    ├── __init__.py
    ├── test_equilateral.py
    └── test_isosceles.py
```

```python hl_lines="11" linenums="1" title="Figure 2: equilateral.py" 
import math


def equilateral_area(a):
    const = math.sqrt(3) / 4

    if a == 1:
        return const

    term = math.pow(a, 2)
    area = const + term  # bug
    # area = const * term  # patch
    return area
```

```python hl_lines="6" linenums="1" title="Figure 3: isosceles.py" 
import math


def isosceles_area(leg, base):
    def height():
        t1, t2 = math.pow(base, 2), math.pow(leg, 2) / 4  # bug
        # t1, t2 = math.pow(leg, 2), math.pow(base, 2) / 4  # patch
        return math.sqrt(t1 - t2)

    area = 0.5 * base * height()
    return area
```

Both functions have a bug. The bug locations are marked with comment
`bug`, and highlighted, within code in Figures 2 and 3. The patch
for each bug is in the line following the bug location, in the form of a
comment.

The `tests` package contains the project's test suite, including two
test modules
[tests/test_equilateral.py](https://github.com/atom-sw/fauxpy/blob/main/examples/example1/tests/test_equilateral.py)
(Figure 4) and
[tests/test_isosceles.py](https://github.com/atom-sw/fauxpy/blob/main/examples/example1/tests/test_isosceles.py)
(Figure 5) for modules `equilateral.py` and `isosceles.py`,
respectively. Each of these two test modules has two tests, one failing
(i.e., revealing the bug) and one passing on their corresponding modules
in package `code`.

```python linenums="1" title="Figure 4: test_equilateral.py"
import math

import pytest

from code.equilateral import equilateral_area


def test_ea_fail():
    a = 3
    area = equilateral_area(a)
    assert area == pytest.approx(9 * math.sqrt(3) / 4)


def test_ea_pass():
    a = 1
    area = equilateral_area(a)
    assert area == pytest.approx(math.sqrt(3) / 4)
```

```python linenums="1" title="Figure 5: test_isosceles.py"
import math

import pytest

from code.isosceles import isosceles_area


def test_ia_crash():
    leg, base = 9, 4

    area = isosceles_area(leg, base)
    assert area == pytest.approx(2 * math.sqrt(77))


def test_ia_pass():
    leg = base = 4

    area = isosceles_area(leg, base)
    assert area == pytest.approx(2 * math.sqrt(12))
```

### Preparing the Python Environment

To get started with FauxPy, you'll first need to set up your
environment. Follow these steps to prepare your machine for the
walkthrough:

1.  **Clone the FauxPy Repository:**

    Begin by cloning the [FauxPy
    repository](https://github.com/atom-sw/fauxpy) from GitHub:

    ``` bash
    git clone git@github.com:atom-sw/fauxpy.git
    ```

2.  **Copy the Example Project:**

    Example 1 is located in the
    `fauxpy/examples/example1` directory. Copy this directory to a
    location of your choice (e.g., your home directory):

    ``` bash
    cp -r fauxpy/examples/example1 ~/example1
    ```

3.  **Navigate to the Example Directory:**

    Change your directory to the location where you copied the
    `example1` example:

    ``` bash
    cd ~/example1
    ```

4.  **Set Up a Python Virtual Environment:**

    Create a Python 3.8 virtual environment named `env`. Later Python
    versions should also be compatible:

    ``` bash
    python3.8 -m venv env
    ```

5.  **Activate the Virtual Environment:**

    Activate the `env` environment. Ensure that this environment remains
    active for the following commands:

    ``` bash
    source env/bin/activate
    ```

6.  **Install FauxPy:**

    With the virtual environment active, install FauxPy using pip:

    ``` bash
    pip install fauxpy
    ```

### Locating the Bug in `equilateral.py`

FauxPy is a Pytest plugin, and thus, running it is similar to running
Pytest. Let's first use Pytest to run all the tests in package `tests`.

``` bash
python -m pytest tests
```

Running the command prints the following message, indicating there are 4
tests in the project, 2 of which are failing.

```
2 failed, 2 passed in 0.07s
```

#### Running Spectrum-Based Fault Localization (SBFL)

Now let's run FauxPy. FauxPy has only one mandatory command line option
`--src`, which takes a package (directory) or module (`.py` file) in the
current project. Since the source code of our project is in package
`code`, we pass `code` to `--src`.

``` bash
python -m pytest tests --src code
```

By default, FauxPy runs SBFL (spectrum-based fault localization). The
command finishes quickly, printing three lists, one for each SBFL
technique currently supported by FauxPy: Tarantula, Ochiai, and DStar.

The list for Tarantula looks something like the following. Each row in
this list shows a line number in package `code` and a number (e.g., 1.1)
denoting the line's suspiciousness score according to Tarantula.

The location of the bug in `equilateral.py` is `equilateral.py::11`, and
the location of the bug in `isosceles.py` is `isosceles.py::6`. Thus,
Tarantula detected the locations of both bugs.

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

While we just used FauxPy to localize multiple bugs in one go, it is
normally preferable to analyze each bug separately from the others. In
FauxPy, we can do this in two ways:

1.  Selecting tests
2.  Selecting failing tests

##### Selecting Tests

The following command runs FauxPy using only the tests in
`tests/test_equilateral.py`. Since the failing test in
`tests/test_equilateral.py` is related to only a single bug, FauxPy only
localizes that one bug.

``` bash
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

##### Selecting Failing Tests

The following command runs FauxPy using the whole test suite `tests` but
**only** one *failing* test `tests/test_equilateral.py::test_ea_fail`,
which triggers the bug in `equilateral.py`.

``` bash
python -m pytest tests --src code --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

Tarantula's output list is now as follows, including lines from any
files but correctly ranking line `equilateral.py::11` in the top
suspiciousness position.

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

As you can see, both approaches report the bug line in `equilateral.py`
as the second element in the output list, tied with two other lines in
the same file. Note that the order of lines with the same suspiciousness
score is immaterial; thus, a user would have to go through all three
lines to determine if one of them is indeed the correct fault location.

#### Running Mutation-Based Fault Localization (MBFL)

To run MBFL techniques, we pass option `--family mbfl`.

``` bash
python -m pytest tests --src code --family mbfl --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

The command prints two lists, one for each MBFL technique currently
supported by FauxPy: Metallaxis and Muse.

The list for Muse looks something like the following.

``` 
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::11', 0.09090909090909091)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::10', 0.0)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::7', -0.039660506068057426)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::5', -0.055524708495280385)
```

Remember that `equilateral.py::11` is the actual bug location in
`equilateral.py`. This line is ranked top, and all other lines have a
strictly lower suspiciousness score. Thus, Muse localizes this bug
perfectly.

Note that you cannot compare the value of suspiciousness scores between
techniques: what matters is the ranking of lines by suspiciousness.

#### Running Stack Trace (ST) and Predicate Switching (PS) Fault Localization

To run the ST technique, we pass option `--family st`.

``` bash
python -m pytest tests --src code --family st --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

And, to run the PS technique, we pass option `--family ps`:

``` bash
python -m pytest tests --src code --family ps --failing-list "[tests/test_equilateral.py::test_ea_fail]"
```

Both techniques return an empty output list, which means that they
failed to localize the bug in `equilateral.py`.

### Locating the Bug in `isosceles.py`

Now, let's run some of the techniques on the other bug in `isosceles.py`.

Here is how to run SBFL. Note that we changed the argument
`--failing-list`, so that we switch to `isosceles.py`'s bug.

``` bash
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

``` bash
python -m pytest tests --src code --family mbfl --failing-list "[tests/test_isosceles.py::test_ia_crash]"
```

Metallaxis's output list is as follows:

``` 
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::10', 0.5)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::6', 0.5)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::8', 0.5)
```

We could also run ST and PS by simply replacing `mbfl` with `st` or `ps`
in the previous command. However, ST and PS only need failing tests;
rather than letting FauxPy run all tests and discover which ones are
failing, we can point it directly to only use a specific failing test,
which may save some time if our test suite includes many passing tests
(useless for ST and PS). To this end, we invoke FauxPy as follows to run
ST:

``` bash
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
`8` in the top position). This is because ST cannot distinguish between
statements within the same function, and hence it will always cluster
function bodies together.

Similarly, we run PS with only the failing test as follows:

``` bash
python -m pytest tests/test_isosceles.py::test_ia_crash --src code --family ps
```

PS returns an empty list of lines on this example as well. PS can only
localize bugs that originate in branching predicates (such as
conditionals and loop exit conditions), and hence it is a poor match for
these examples.

### Function-level Granularity

In all the examples seen so far, FauxPy ran with statement-level
granularity. This means that it localizes *lines* within a program.

FauxPy also supports function-level granularity; in this case, it
reports a list of *functions* within a program, each with a certain
suspiciousness score.

To run any of the previous examples with function-level granularity,
pass option `--granularity function`, which overrides the default
`--granularity statement`.

For instance, here is how to run SBFL with function-level granularity on `isosceles.py`.

``` bash
python -m pytest tests --src code --family sbfl --granularity function --failing-list "[tests/test_isosceles.py::test_ia_crash]"
```

Tarantula's output list is as follows:

``` 
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::isosceles_area::4::11', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/isosceles.py::height::5::8', 0.75625)
('~/fauxpy-examples-dev/triangle_area/code/equilateral.py::equilateral_area::4::13', 0.1)
```

## Example 2

This walkthrough demonstrates how to use FauxPy's new **Mutation Strategy**
feature, which leverages
[PyLLMut](https://pyllmut.readthedocs.io/), 
an LLM-driven mutant 
generator for Python.
The walkthrough begins by introducing the project structure of 
[Example 2](https://github.com/atom-sw/fauxpy/tree/main/examples/example2)
and then provides instructions on setting up the environment
and running FauxPy with this example.

### Project Structure

As shown in Figure 6, *Example 2* consists of two packages:
[code](https://github.com/atom-sw/fauxpy/tree/main/examples/example2/code) and
[tests](https://github.com/atom-sw/fauxpy/tree/main/examples/example2/tests).
The `code` package contains the module 
[code/isosceles.py](https://github.com/atom-sw/fauxpy/blob/main/examples/example2/code/isosceles.py),
which includes the project's source code, as shown in
Figure 7.
The function in `code/isosceles.py`
computes the area of an isosceles triangle.
There is a bug in line 13, highlighted
in Figure 7. The bug arises because the function
returns `base`
instead of `area`.

!!!note
    Unlike Example 1, in this example, we do not specify
    the bug location and patch using comments, as
    they may bias the LLM during mutant generation.

The `tests` package contains the project's test suite,
which includes a single test module,
[tests/test_isosceles.py](https://github.com/atom-sw/fauxpy/blob/main/examples/example2/tests/test_isosceles.py) 
(Figure 8).
The module consists of one passing test and one
failing test (i.e., revealing the bug),
both of which test the function in `code/isosceles.py`.

``` title="Figure 6: Project structure of Example 2."
example2/
├── code/
│   ├── __init__.py
│   ├── isosceles.py
└── tests/
    ├── __init__.py
    └── test_isosceles.py
```

```python hl_lines="13" linenums="1" title="Figure 7: Implementation of 'isosceles.py', which includes a function that computes the area of an isosceles triangle but contains a bug on line 13." 
import math


def isosceles_area(leg, base):
    def height():
        t1, t2 = math.pow(leg, 2), math.pow(base, 2) / 4
        return math.sqrt(t1 - t2)

    if leg == 0 or base == 0:
        return 0

    area = 0.5 * base * height()
    return base
```

```python linenums="1" title="Figure 8: Test suite in 'test_isosceles.py', which includes one passing test and one failing test that reveals the bug."
import math

import pytest

from code.isosceles import isosceles_area


def test_ia_fail():
    leg, base = 9, 4

    area = isosceles_area(leg, base)
    assert area == pytest.approx(2 * math.sqrt(77))

def test_ia_pass():
    leg = 4
    base = 0

    area = isosceles_area(leg, base)
    assert area == 0
```

### Preparing the Python Environment

To get started with FauxPy, follow these steps to set up your environment:

1.  **Clone the FauxPy Repository:**

    Clone the [FauxPy
    repository](https://github.com/atom-sw/fauxpy) from GitHub:

    ``` bash
    git clone git@github.com:atom-sw/fauxpy.git
    ```

2.  **Copy the Example Project:**

    Example 2 is located in the
    `fauxpy/examples/example2` directory. Copy this directory to a
    location of your choice (e.g., your home directory):

    ``` bash
    cp -r fauxpy/examples/example2 ~/fauxpy_example2
    ```

3.  **Navigate to the Example Directory:**

    Change your directory to where you copied Example 2:

    ``` bash
    cd ~/fauxpy_example2
    ```

4.  **Set Up a Python Virtual Environment:**

    Create a Python virtual environment named `env`.
    On some machines (e.g., MacBooks), 
    you may need to use `python3` instead of `python`.

    ``` bash
    python -m venv env
    ```

5.  **Activate the Virtual Environment:**

    Activate the `env` environment.
    Keep this environment active for the following commands:

    ``` bash
    source env/bin/activate
    ```

6.  **Install FauxPy:**

    With the virtual environment active, install FauxPy using `pip`:

    ``` bash
    pip install fauxpy
    ```
    
    For this example, since we are using LLM-driven mutation strategies 
    that rely on LLMs through their APIs, you must also **set up 
    your LLM API key**. The setup instructions are available on the
    [installation page](./install.md#setting-up-your-llm-api-key).

### Running LLM-Driven MBFL

Let's first run MBFL techniques 
without using LLM-driven mutation strategies:

``` bash
python -m pytest tests --src code --family mbfl
```

Note that you could add `--mutation t` to specify 
that the mutation strategy should be *Traditional*. 
However, since this is the default mutation strategy, 
it is not necessary to provide it.

Additionally, we do not specify the failing test using `--failing-list` 
because there is only a single failing test in the 
test suite (Figure 8).

Muse's output list is as follows:

```
('~/fauxpy_example2/code/isosceles.py::12', 0.0)
('~/fauxpy_example2/code/isosceles.py::6', 0.0)
('~/fauxpy_example2/code/isosceles.py::7', 0.0)
('~/fauxpy_example2/code/isosceles.py::9', 0.0)
```

Metallaxis's output list is as follows:

```
('~/fauxpy_example2/code/isosceles.py::12', 1.0)
('~/fauxpy_example2/code/isosceles.py::6', 1.0)
('~/fauxpy_example2/code/isosceles.py::7', 1.0)
('~/fauxpy_example2/code/isosceles.py::9', 1.0)
```

As you can see, line 13 is not even listed by either of the two
MBFL techniques, Muse and Metallaxis.
The reason is that the traditional mutation operators were unable
to generate any mutants for line 13 in Figure 7.

Now, let's run MBFL techniques using LLM-driven mutation strategies,
starting with the `tgpt4oapi` strategy. This mutation strategy
first attempts to generate mutants using traditional mutation operators.
Then, it uses *GPT-4o* to generate mutants for lines where traditional
operators failed to do so.

``` bash
python -m pytest tests --src code --family mbfl --mutation tgpt4oapi
```

Muse's output list is as follows, correctly ranking line
`isosceles.py::13` in the top suspiciousness position. 
All other lines have a strictly 
lower suspiciousness score, so 
Muse localizes this bug perfectly, thanks to
mutants generated by the LLM.

```
('~/fauxpy_example2/code/isosceles.py::13', 0.14285714285714285)
('~/fauxpy_example2/code/isosceles.py::12', 0.0)
('~/fauxpy_example2/code/isosceles.py::6', 0.0)
('~/fauxpy_example2/code/isosceles.py::7', 0.0)
('~/fauxpy_example2/code/isosceles.py::9', 0.0)
```

!!! note
    Given the nondeterministic nature of LLMs
    and AI in general, you might get different results on your machine or even
    in different runs when using FauxPy with LLM-driven mutation strategies.
    Even your internet speed can affect the results,
    as mutant generation for some lines might time out if your internet 
    connection is too slow.
    This is a general issue
    for any application of LLMs.

Now, let's run MBFL techniques using another LLM-driven strategy `gpt4oapi`.
This strategy purely relies on *GPT-4o* to generate mutants without using
traditional mutation operators.

``` bash
python -m pytest tests --src code --family mbfl --mutation gpt4oapi
```

Muse's output list is as follows, again correctly ranking line
`isosceles.py::13` in the top suspiciousness position.

```
('~/fauxpy_example2/code/isosceles.py::13', 0.14285714285714285)
('~/fauxpy_example2/code/isosceles.py::12', 0.0)
('~/fauxpy_example2/code/isosceles.py::6', 0.0)
('~/fauxpy_example2/code/isosceles.py::7', 0.0)
('~/fauxpy_example2/code/isosceles.py::9', 0.0)
```
