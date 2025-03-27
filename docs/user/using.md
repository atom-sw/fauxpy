# Command-Line Options

FauxPy is implemented as a Pytest plugin, thus using FauxPy boils down
to passing some custom options to Pytest.

To run FauxPy, you must first `cd` to the project's
directory `$PROJECT`:

``` bash
cd $PROJECT
```

Then, the basic command to run FauxPy is the following, where `$SOURCE`
is the relative path to a Python package or module inside `$PROJECT`:

``` bash
python -m pytest --src $SOURCE
```

This performs statement-level spectrum-based fault localization on the
Python project in directory `$PROJECT`, using any Pytest tests in there.

The output is a list of program entities with their suspiciousness
score, sorted from most to least suspicious. The output is printed on
screen, and also saved in a directory `FauxPyReport_...` created in
`$PROJECT`'s parent directory.

This is the complete list of command-line arguments to control FauxPy.

``` bash
python -m pytest \
       $TESTS \
       --src $SRC \
       --family $FAMILY \
       --exclude "[$EXCLUDE1, $EXCLUDE2, ...]" \
       --granularity $GRANULARITY \
       --top-n $N \
       --failing-list "[$FAIL1, $FAIL2, ...]" \
       --failing-file $FAIL \
       --mutation $MUTATION
```

## Option `--src`: Program Source Code

Option `--src $SRC` runs FauxPy on the project considering only the
program entities under *relative* path `$SRC`. Precisely, `$SRC` can
point to a whole project, or an individual package (subdirectory) or
modules (source-code file) within it.

In particular, option `--src .` runs FauxPy on the project in the
current directory, considering the program entities in all the Python
modules and packages existing within the project.

Option `--src` is the only mandatory argument to run FauxPy.

## Option `--family`: Fault Localization Family

Option `--family $FAMILY` runs FauxPy using the `$FAMILY` fault
localization family of techniques. FauxPy currently supports families:
`sbfl` (the default), `mbfl`, `ps`, and `st`.

## Option `--granularity`: Entity Granularity

Option `--granularity $GRANULARITY` runs FauxPy using `$GRANULARITY` as
program entities to localize. FauxPy currently supports granularities:
`statement` (the default), and `function`.

With *statement*-level granularity, FauxPy outputs a list of program
locations (i.e., line numbers) that may be responsible for the fault.
With *function*-level granularity, FauxPy outputs a list of functions
that may be responsible for the fault.

## Option `--exclude`: Exclude Directories or Files

Option `--exclude "[$EXCLUDE1, $EXCLUDE2, ...]"` ignores entities in
`$EXCLUDE1`, `$EXCLUDE2`, and so on when performing fault localization.

Each element of the comma-separated list must be a path relative to the
analyzed project's root directory of a directory (package) or Python
source file (module).

For instance, the following command runs fault localization on the
project in the current directory, skipping directories `env` and
`tests`, and module `utilities`:

``` bash
python -m pytest --src . --exclude "[env, tests, utilities.py]"
```

## Option `--failing-list`: Select Failures

Option `--failing-list "[$FAIL1, $FAIL2, ...]"` *only* uses tests
`$FAIL1`, `$FAIL2`, and so on as *failing* tests when performing fault
localization.

Each element of the comma-separated list must be the fully-qualified
name of a test function in the analyzed project, using the Pytest format
`<FILE_PATH>::<CLASS_NAME>::<FUNCTION_NAME>`, where the `<CLASS_NAME>::`
can be omitted if the test function is top-level.

For instance, the following command runs fault localization on the
project in the current directory, using *only* test function
`test_read_file` in class `Test_IO` as failing test:

``` bash
python -m pytest --src . \
       --failing-list "[test/test_common/test_file.py::Test_IO::test_read_file]"
```

Selecting specific failing tests is especially useful when there are
multiple, different faults, triggered by different tests. Fault
localization techniques are usually designed to work under the
assumption that they analyze each fault in isolation. If the analyzed
project includes multiple faults, it is advisable to select a subset of
the failing tests that trigger a single fault, so that fault
localization can perform more accurately.

## Option `--failing-file`: Select Failures

Option `--failing-file $FAIL` is the same as option `--failing-list`,
but instead of taking a list of failing tests, it takes the path of a
file relative to the analyzed project's root directory. In file
`$FAIL`, every failing test must be in a separate line.

## Option `--top-n`: Output List Size

Option `--top-n $N` only reports up to `$N` suspicious program entities
(statements or functions). `$N` must be a positive integer, or `-1` (the
default: no limit).

## Option `--mutation`: Mutation Generation Strategy

Option `--mutation $MUTATION` specifies the mutation 
generation strategy to be used for Mutation-Based Fault 
Localization (MBFL).

Note that the `--mutation` option is only meaningful when 
the **MBFL** (Mutation-Based Fault Localization) family 
is selected with the `--family` option. 
When using other families, this option will have no effect 
and will be ignored,
as other families 
do not rely on mutant generation.

Currently supported mutation 
strategies `$MUTATION` are:

- `t` (default): Use Cosmic Ray with traditional mutation operators.
- `tgpt4ominiapi`: Use Cosmic Ray, and when it cannot generate a mutant for a statement, fall back to GPT-4o-mini via its API.
- `gpt4ominiapi`: Use only GPT-4o-mini via its API for mutant generation, without Cosmic Ray.
- `tgpt4oapi` - Use Cosmic Ray, and when it cannot generate a mutant for a statement, fall back to GPT-4o via its API.
- `gpt4oapi` - Use only GPT-4o via its API for mutant generation, without Cosmic Ray.

!!! note
    If the `--mutation` option is not provided, it is 
    equivalent to `--mutation t`, which is the 
    default behavior. 
    In this case, FauxPy's MBFL techniques behave like previous 
    versions, using only 
    traditional mutation operators.

For instance, the following command runs 
FauxPy using traditional 
mutation operators (default behavior):

```bash
python -m pytest --src $SRC --mutation t --family mbfl
```

The above command is equivalent to the 
following (note that `--mutation t` is removed):

```bash
python -m pytest --src $SRC --family mbfl
```

As another example, the following command runs FauxPy using traditional mutation operators 
and falls back to GPT-4o-mini when traditional mutation operators fail to generate mutants for a line:

```bash
python -m pytest --src $SRC --mutation tgpt4ominiapi --family mbfl
```

## Positional Argument: Tests

Optional positional argument `$TESTS`, specified just after `pytest`,
runs FauxPy using the tests found under path `$TESTS`. If this argument
is missing, FauxPy will use any tests found in the analyzed project.

`$TESTS` must be a path relative to the analyzed project's root
directory of a directory (package), a Python source file (module), or
the fully-qualified name of a test function in the analyzed project,
using the Pytest format `<FILE_PATH>::<CLASS_NAME>::<FUNCTION_NAME>`,
where the `<CLASS_NAME>::` can be omitted if the test function is
top-level.

The positional argument can be repeated to select tests at different
locations. For instance, the following command runs FauxPy using only
tests in package `tests/package_x`, module `tests/test_y.py`, and test
function `tests/test_z.py::test_function_t`.

``` bash
python -m pytest tests/package_x \
       tests/test_y.py \
       tests/test_z.py::test_function_t \
       --src $SRC
```

Stack-trace and predicate switching fault localization only need to run
failing tests. If a project has many tests, but only a few are failing,
ST and PS fault localization will run more quickly if we pass the
failing tests' location using this feature. If we don't, FauxPy will
still have to run all tests, just to discover which ones are failing and
can be used for ST or PS fault localization.
