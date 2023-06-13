# Usage

## Usage example

```
pytest tests
       --src code
       --family sbfl
       --exclude "[code/library_x, code/module_x.py]"
       --granularity statement
       --top-n 3
       --failing-file target_failing_test.txt
       
```


## Arguments

###--src

The relative path to the directory in the project to 
apply fault localization on.

###--exclude

A list of relative (to the project directory) paths (files or directories) within
the directory specified by **--src:** to be excluded.

###--family

The fault localization family to apply on the project.
The options are as follows:
* `sbfl`: spectrum-based fault localization
* `st`: stacktrace-based fault localization
* `mbfl`: mutation-based fault localization
* `ps`: predicate switching fault localization

#### Notes on failing tests

The two families *stacktrace-based fault localization* 
and *predicate switching fault localization* only
consider failing tests for fault localization. Therefore,
it is better if the user only passes the target failing tests to pytest 
while using the tool
(the first argument to pytest in usage example section).

However, even if the user runs these two families with all the tests,
the technique runs all the tests and finds the failing tests automatically.
The only difference is that in the former, the tools performs faster.

The user can also specify the target failing tests using the `failing-file` argument.
In this case, the intersection of the failing tests in this file and those provided as 
the first parameter to pytest are considered for fault localization.

The *predicate switching fault localization* technique cannot collect information
from multiple failing tests. Therefore, if multiple failing tests 
are provided for *predicate switching fault localization*,
it uses every single one of them separately from the other failing tests
to perform fault localization. But, *stacktrace-based fault localization* can
use all the failing tests at the same time to locate bugs.

#### Notes on stacktrace-based fault localization

The *stacktrace-based fault localization* only supports function granularity. It
is not a limitation of FauxPy. It is a limitation of the technique itself.

###--granularity

The granularity of the entities to which a technique assigns scores.
The options are as follows:
* `statement`: statements are considered as the entities
* `function`: functions are considered as the entities

###--top-n

The number of entities to return by a technique.
The options are as follows:
* `-1`
* an integer in the range [1, +INF]

###--failing-file

A file containing the failing tests targeted by a technique.
In this file, each failing test is in a separate line.
At each line, the test is in the following format:

`[FILE_PATH]::[CLASS_NAME]::[FUNCTION_NAME]`

Examples:

1. The following is a test in unittest:

`test/test_common/test_file.py::Test_IO::test_read_file`

2. The following is a pytest parametrized tests:

Note: do not specify parameters for parametrized failing tests. For instance, if
the target failing test is `test/test_tuils.py::test_addition[1-2-3]`, remove
the parameters:

`test/test_tuils.py::test_addition` (this one is a pytest parametrized test)

###--failing-list

A list containing the failing tests targeted by a technique.
In this list, each element is in the following format:

`[FILE_PATH]::[CLASS_NAME]::[FUNCTION_NAME]`

Examples:

[`test/test_common/test_file.py::Test_IO::test_read_file` (this one is a unittest test)

`test/test_tuils.py::test_addition` (this one is a pytest parametrized test. Parameters must be removed.)

```
pytest tests
       ...
       --failing-list "[test/test_common/test_file.py::Test_IO::test_read_file,
                       test/test_tuils.py::test_addition]"
       ...       
```



# Limitations

The SBFL/MBFL family uses coverage.py to collect execution traces. So, any limitation of coverage.py is a limitation of the SBFL/MBFL family.

The stack trace family does not work with --tb=native of pytest. Do not use it in command line mode or in pytest.ini file.

The ps family uses sys.settrace function. So, any limitation of sys.settrace is a limitation of the ps family.

FauxPy is not compatible with pytest-sugar. So, in order to use FauxPy, pytest-sugar must be uninstalled (using the command `pip uninstall pytest-sugar`) form the environment.
