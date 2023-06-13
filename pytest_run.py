from typing import List

import pytest
import os


def runCommand(cmd: List[str], workingDir: str):
    import subprocess
    execOut = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               cwd=workingDir)

    print("--------------------HERE_BEGIN_PYTEST_RUN---------------------")
    # print(execOut.stdout)
    # print(execOut.stderr)
    for line in execOut.stdout:
        print(line.replace('\n', ''))
    for line in execOut.stderr:
        print(line.replace('\n', ''))
    print("--------------------HERE_END_PYTEST_RUN---------------------")


def runCommandScript(cmd: str, workingDir: str):
    import subprocess
    cmdLst = cmd.split(" ")
    execOut = subprocess.Popen(cmdLst,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               cwd=workingDir)

    print("--------------------HERE_BEGIN_PYTEST_RUN---------------------")
    # print(execOut.stdout)
    # print(execOut.stderr)
    for line in execOut.stdout:
        print(line.replace('\n', ''))
    for line in execOut.stderr:
        print(line.replace('\n', ''))
    print("--------------------HERE_END_PYTEST_RUN---------------------")


# TODO: check concurrency
#  check pytest.ini
#  check tox.ini
#  check .coveragerc
#  check coverage.py
# pytest.ini|tox.ini|setup.cfg
# https://doc.pytest.org/en/latest/reference/customize.html

# TODO: sbfl.config
# {
#     "include": {
#         "dir": [],
#         "file": []
#     },
#     "exclude": {
#         "dir": [],
#         "file": []
#     }
# }

# TODO: see thefuck problem (done). Also in fastapi (done). Also in tornado (partially done).
# What should we do with the tests that have no execution traces?
# Should we remove them from metric computations?

# TODO: check the solved problem for black. Why is it solved?

# TODO: is COV.stop() at the correct location? (Done. Seems to be OK. Added a check CURRENT_TEST)

# TODO: why in tornado there are more empty exec tests than tests not in the execution trace? (Done. They collected, but skipped.)

# Note: within the experiments, I think we should only consider the
# only failing test reported for the bug. Because some failing tests
# might be failing because of unseen stuff such as concurrency stuff.

# Note: for some parametrized tests, the execution trace
#  only contains the executed lines (spacy-bug6) within the test.
#  It happens because it seems they are in .pyx files.
#  Adding a feature that takes multiple fault localization and
#  test directories and files seems to be important.

# currentWD = os.getcwd()
# os.chdir("/home/moe/Desktop/NewStudy/AFL4Python/samples/example")
# retcode = pytest.main(["--src", "src", "--family", "mbfl", "--granularity", "statement", "--top-n", "5"])
# retcode = pytest.main(["test", "--src", "my_code", "--family", "ps", "--granularity", "statement", "--top-n", "-1"])
# retcode = pytest.main(["test", "tests", "my_test", "--src", "src", "--family", "mbfl", "--granularity", "statement", "--top-n", "5"])
# retcode = pytest.main(["--src", "src", "--family", "mbfl", "--granularity", "statement", "--top-n", "5"])
# retcode = pytest.main(["--collect-mode", "1"])

# os.chdir("/home/moe/Desktop/NewStudy/AFL4Python/samples/simple_example")
# retcode = pytest.main(["--dir", "src"])

# /home/moe/Desktop/NewStudy/AFL4Python/samples/example3/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/AFL4Python/samples/example3")
# retcode = pytest.main(["--src", "src", "--family", "mbfl", "--granularity", "statement", "--top-n", "5"])

# workDir = "/home/moe/Desktop/NewStudy/AFL4Python/samples/example"
# command = ["python", "-m", "pytest",
#            "test",
#            "--src", "my_code", "--family", "mbfl", "--granularity", "statement", "--top-n", "-1",
#            "--failing-file", "failing_tests_targeted.txt",
#            # "--failing-list", "[\
#            #                     test/test_calc_module1.py::test_calculation1[1-2-3],\
#            #                     test/test_calc_module2.py::TestCalc2::test_calculation21,\
#            #                     test/test_crash_exp_2.py::test_crash_myFunc,\
#            #                     test/test_stack_trace.py::test_crash_example\
#            #                    ]",
#            # "--exclude", "[my_code/crash_exp_2.py]",
#            # "--timeout", "1"
#            ]
# runCommand(command, workDir)

# ---------------------------------------------------------------------------------------------------------------

# Problem1: debugger does not work on this one (fixed) (use --no-cov tag). Does not exist in coverage.py
# version. No need to run with --no-cov tag.
# Problem2: execution trace does not contain some of the tests (fixed). Does not exist in coverage.py version.
# /home/moe/Desktop/NewStudy/BugsInPy/repos/cookiecutter/bug3/buggy/cookiecutter/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/cookiecutter/bug3/buggy/cookiecutter")
# pytest tests --src cookiecutter --family sbfl --technique ochiai --granularity statement --top-n 10
# retcode = pytest.main(["tests", "--no-cov ", "--src", "cookiecutter",
#                        "--family", "ps",
#                        "--granularity", "statement",
#                        "--top-n", "10"
#                        ])

# pytest tests --src cookiecutter --family ps --granularity statement

# workDir = "/home/moe/Desktop/NewStudy/BugsInPy/repos/cookiecutter/bug3/buggy/cookiecutter"
# command = ["python", "-m", "pytest", "tests",
#            "--src", "cookiecutter", "--family", "mbfl", "--granularity", "statement", "--top-n", "30"]
# runCommand(command, workDir)

# Note: the structure of this project is not good. Tests and code are
# not seperated properly. There are also some tests testing
# .pyx files and because of that, the execution traces of these
# tests do not contain useful information.
# Examples of parametrized, skipped, xfailed, and xpassed
# /home/moe/Desktop/NewStudy/BugsInPy/repos/spaCy/bug6/buggy/spacy/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/spaCy/bug6/buggy/spacy")
# retcode = pytest.main(["spacy/tests/serialize", "--dir", "spacy"])
# retcode = pytest.main(["spacy/tests", "--dir", "spacy"])

# Error: this one works on terminal when calling pytest. But does not work with the following.
# But, it works as an installed plugin. But still, some tests do not
# get executed (it was not observed in the coverage.py version).
# /home/moe/Desktop/NewStudy/BugsInPy/repos/httpie/bug2/buggy/httpie/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/httpie/bug2/buggy/httpie")
# retcode = pytest.main(["tests", "--dir", "httpie"])

# TO-DO: Find a way to reduce the number of tests during development.
# Note: do not run it in command line using the following environment as
# python. Set the environment in the IDE and use the play button.
# I have not tested using the tool as an installed plugin to see
# how it works.
# Error (tests/keras/backend): the execution trace reported is always empty.
# It is not observed in the coverage.py version. But, not other problems exist.
# To fix it, comment out -n 2 option within the pytest.ini file, and run the tool as
# installed plugin (tested on tests/keras/backend tests).
# /home/moe/Desktop/NewStudy/BugsInPy/repos/keras/bug1/buggy/keras/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/keras/bug1/buggy/keras")
# retcode = pytest.main(["tests", "--dir", "keras"])
# retcode = pytest.main(["tests/keras/backend", "--dir", "keras"])
# retcode = pytest.main(["tests/keras/backend", "--dir", "keras", "--no-cov"]) No need in the coverage.py version.

# Problem: execution trace is empty for (1261) some tests (fixed).
# A bug fix is applied. Now only 24 tests are empty which is correct.
# (e.g., "tests/rules/test_open.py::30::test_match[kde-open foo.com]").
# This problem exists in the coverage.py version.
# /home/moe/Desktop/NewStudy/BugsInPy/repos/thefuck/bug3/buggy/thefuck/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/thefuck/bug3/buggy/thefuck")
# retcode = pytest.main(["--dir", "thefuck"])

# __HERE____
# workDir = "/home/moe/Desktop/NewStudy/BugsInPy/repos/thefuck/bug3/buggy/thefuck"
# command = ["python", "-m", "pytest",
#            "tests",
#            "--src", "thefuck", "--family", "sbfl", "--granularity", "statement", "--top-n", "-1",
#            # "--timeout", "1"
#            ]
# runCommand(command, workDir)

# TO-DO: Find a way to reduce the number of tests during development.
# Parametrized, skipped, xpass, and xfailed, tests examples
# /home/moe/Desktop/NewStudy/BugsInPy/repos/pandas/bug61/buggy/pandas/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/pandas/bug61/buggy/pandas")
# retcode = pytest.main(["pandas/tests/extension", "--dir", "pandas"])
# retcode = pytest.main(["pandas/tests", "--dir", "pandas"])

# It has unittest tests.
# Problem: project files of this project are in the root.
# So, the AFL tool collects information about the python environment and lots of other
# irrelevant files. Adding a feature which takes also files and not just dir
# can be useful. This problem was not observed in the coverage.py version.
# /home/moe/Desktop/NewStudy/BugsInPy/repos/black/bug2/buggy/black/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/black/bug2/buggy/black")
# retcode = pytest.main(["--dir", "."])

# Error1: this one works on terminal when calling pytest. But does not work with the following.
# Error2: even on terminal, do not specify the name of the test directory.
# It works with --no-cov (not sure if it`s necessary).
# Note: this one has concurrency stuff.
# It works as plugin with - pytest --dir fastapi - command with the
# coverage.py version. The flag --no-cov is not needed.
# /home/moe/Desktop/NewStudy/BugsInPy/repos/fastapi/bug4/buggy/fastapi/env/bin/python
# pytest --dir fastapi
# Interesting observation: in test tests/test_custom_route_class.py::106::test_route_classes
# app.router.routes is a part of the localization dir but since it is filled
# in the script part of the test module, it is not collected in the execution trace of the test.
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/fastapi/bug4/buggy/fastapi")
# retcode = pytest.main(["--no-cov", "--dir", "fastapi"])
# retcode = pytest.main(["--dir", "fastapi"])

# /home/moe/Desktop/NewStudy/BugsInPy/repos/tornado/bug1/buggy/tornado/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/tornado/bug1/buggy/tornado")
# retcode = pytest.main(["tornado/test", "--dir", "tornado"])

# Special case: running the failing test produces a failing and an
# error result. Check if removing errors causes problems for a case like this.
# Problem: since the name of the test modules of this project start with tests (instead of test)
# pytest cannot collect them. I think the solution is to change the name of
# each test file to fix this problem. I made a new dir called tests_my with
# all the tests renamed to test_* (however, the two files tests_perf.py and tests_tqdm.py must
# exist in this folder).
# Note1: this project has tests with examples of concurrency (tests_concurrent.py).
# Note2: the structure of this project is not good. Tests are also reported
# in the execution trace files.
# /home/moe/Desktop/NewStudy/BugsInPy/repos/tqdm/bug1/buggy/tqdm/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/tqdm/bug1/buggy/tqdm")
# retcode = pytest.main(["tqdm/tests_my", "--src", "tqdm"])

# TO-DO: Find a way to reduce the number of tests during development.
# /home/moe/Desktop/NewStudy/BugsInPy/repos/youtube-dl/bug25/buggy/youtube-dl/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repos/youtube-dl/bug25/buggy/youtube-dl")
# retcode = pytest.main(["test/test_YoutubeDL.py", "--dir", "youtube_dl"])
# retcode = pytest.main(["test", "--dir", "youtube_dl"])

# Note: hypothesis tests are considered to be a single test by pytest.
# /home/moe/Desktop/NewStudy/annotest_replication/keras/DN/bug1/buggy/densenet/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/annotest_replication/keras/DN/bug1/buggy/densenet")
# retcode = pytest.main(["test_annotest", "--dir", "src"])


# CRASHING
# /home/moe/Desktop/NewStudy/BugsInPy/repcrash/spaCy/bug4/buggy/spacy/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repcrash/spaCy/bug4/buggy/spacy")
# retcode = pytest.main(["spacy/tests", "--src", "spacy", "--exclude", "['spacy/tests']", "--family", "stack"])
# pytest spacy/tests --src spacy --exclude "['spacy/tests']" --family sbfl --technique ochiai --granularity function --top-n 10

# Error (fixed): AttributeError: 'ReprExceptionInfo' object has no attribute 'chain'
# Fix: comment out addopts = --tb=native in pytest.ini-
# /home/moe/Desktop/NewStudy/BugsInPy/repcrash/httpie/bug3/buggy/httpie/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repcrash/httpie/bug3/buggy/httpie")
# pytest tests --src httpie --family stack
# retcode = pytest.main(["tests", "--src", "httpie", "--family", "sbfl", "--technique", "ochiai", "--top-n", "10", "--granularity", "function"])
# pytest tests --src httpie --family sbfl --technique ochiai --top-n 10 --granularity function

# Note: Takes time
# /home/moe/Desktop/NewStudy/BugsInPy/repcrash/keras/bug41/buggy/keras/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repcrash/keras/bug41/buggy/keras")
# retcode = pytest.main(["tests", "--src", "keras", "--family", "stack"])

# Note: Nothing for stack. The failing tests are assertion failures.
# The environment for the buggy version is not correct so reinstall. Use the env of the fixed version.
# Error (fixed): For sbfl statement, running only the failing test modules produces scores.
# But running all tests or tests/rules produces all 0 scores (fixed).
# /home/moe/Desktop/NewStudy/BugsInPy/repcrash/thefuck/bug8/buggy/thefuck/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repcrash/thefuck/bug8/buggy/thefuck")
# retcode = pytest.main(["tests", "--src", "thefuck", "--family", "sbfl", "--granularity", "function"])
# retcode = pytest.main(["tests/rules/test_dnf_no_such_command.py", "--src", "thefuck", "--family", "stack"])

# Note: Nothing for stack. The failing tests are assertion failures.
# /home/moe/Desktop/NewStudy/BugsInPy/repcrash/black/bug6/buggy/black/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repcrash/black/bug6/buggy/black")
# retcode = pytest.main(["tests", "--src", ".", "--exclude", "['env', 'tests']", "--family", "sbfl", "--granularity", "statement"])
# retcode = pytest.main(["tests", "--src", ".", "--exclude", "['env', 'tests']", "--family", "stack"])

# /home/moe/Desktop/NewStudy/BugsInPy/repcrash/tornado/bug10/buggy/tornado/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repcrash/tornado/bug10/buggy/tornado")
# retcode = pytest.main(["tornado/test", "--src", "tornado", "--exclude", "['tornado/test']", "--family", "sbfl", "--granularity", "statement"])
# retcode = pytest.main(["tornado/test", "--src", "tornado", "--exclude", "['tornado/test']", "--family", "stack"])

# Problem (fixed - only run it as a plugin): Works on the fixed version but for the buggy version the trace is empty.
# /home/moe/Desktop/NewStudy/BugsInPy/repcrash/tqdm/bug5/buggy/tqdm/env/bin/python
# os.chdir("/home/moe/Desktop/NewStudy/BugsInPy/repcrash/tqdm/bug5/buggy/tqdm")
# pytest tqdm/tests_my --src tqdm --exclude "['tqdm/tests', 'tqdm/tests_my']" --family sbfl --granularity statement
# retcode = pytest.main(["tqdm/tests_my", "--src", "tqdm", "--exclude", "['tqdm/tests', 'tqdm/tests_my']", "--family", "sbfl", "--granularity", "statement"])


# ------------------------------------------------------------------------------------------

# workDir = "/home/moe/Desktop/SI_SEMINAR/cookiecutter_bug1/cookiecutter"
# command = ["python", "-m", "pytest", "tests",
#            "--src", "cookiecutter", "--family", "sbfl", "--granularity", "function", "--top-n", "30",
#            # "--no-cov"
#            ]
# runCommand(command, workDir)


# workDir = "/home/moe/Desktop/SI_SEMINAR/si_example/example"
# command = ["python", "-m", "pytest", "test",
#            "--src", "my_code", "--family", "st", "--granularity", "statement", "--top-n", "30",
#            # "--no-cov"
#            ]
# runCommand(command, workDir)


# workDir = "/home/moe/BugsInPyExp/12.scrapy/bug34/buggy/scrapy"
# command = ["python", "-m", "pytest", "tests",
#            "--src", "scrapy", "--family", "sbfl", "--granularity", "statement",
#            # "--top-n", "30",
#            # "--no-cov"
#            ]
# runCommand(command, workDir)

# workDir = "/home/moe/BugsInPyExp/15.tornado/bug3/buggy/tornado"
# # command = 'python -m pytest tornado/test/httpclient_test.py --src tornado --granularity statement --family mbfl --exclude [tornado/test] --failing-file failing_file.txt'
# command = 'python -m pytest tornado/test --src tornado --granularity statement --family ps --exclude [tornado/test] --failing-file failing_file.txt'
# # command = 'python -m pytest tornado/test/httpclient_test.py --src tornado --granularity statement --family collectmbfl --exclude [tornado/test] --failing-file failing_file.txt'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/11.black/bug14/buggy/black"
# # command = 'python -m pytest tests --src . --exclude [env,tests] --granularity statement --family ps'
# command = 'python -m pytest tests/test_black.py::BlackTestCase::test_get_future_imports --src . --exclude [env,tests] --granularity statement --family ps --failing-list [tests/test_black.py::BlackTestCase::test_get_future_imports]'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/10.pandas/bug56/buggy/pandas"
# # command = 'python -m pytest pandas/tests/indexing/test_scalar.py pandas/tests/frame --src pandas --granularity statement --exclude [pandas/tests] --family mbfl'
# command = 'pytest'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/6.httpie/bug2/buggy/httpie"
# command = 'python -m pytest tests --src httpie --granularity statement --family mbfl'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/5.sanic/bug3/buggy/sanic"
# command = 'python -m pytest tests --src sanic --granularity statement --family ps'
# # command = 'python -m pytest tests/test_app.py tests/test_url_for.py --src sanic --granularity statement --family mbfl'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/12.scrapy/bug34/buggy/scrapy"
# command = 'python -m pytest tests --src scrapy --granularity statement --family mbfl'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/2.cookiecutter/bug3/buggy/cookiecutter"
# command = 'python -m pytest tests/test_read_user_choice.py::test_click_invocation --src cookiecutter --granularity statement --family sbfl --failing-list [tests/test_read_user_choice.py::test_click_invocation]'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/4.spacy/bug5/buggy/spacy"
# command = 'python -m pytest spacy/tests/test_language.py --src spacy --exclude [spacy/tests] --granularity statement --family sbfl --failing-list [spacy/tests/test_language.py::test_evaluate_no_pipe]'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/17.youtube-dl/bug13/buggy/youtube-dl"
# command = 'python -m pytest test/test_utils.py::TestUtil::test_urljoin --src youtube_dl --granularity function --family ps --failing-list [test/test_utils.py::TestUtil::test_urljoin]'
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/pandas/bug54/buggy/pandas"
# command = ("python -m pytest "
#            " pandas/tests/arrays/categorical/test_constructors.py"
#            " pandas/tests/arrays/categorical/test_dtypes.py"
#            " pandas/tests/arrays/categorical/test_missing.py"
#            " pandas/tests/arrays/test_array.py"
#            " pandas/tests/arrays/test_datetimes.py"
#            " pandas/tests/arrays/test_period.py"
#            " pandas/tests/dtypes/cast/test_construct_from_scalar.py"
#            " pandas/tests/dtypes/cast/test_find_common_type.py"
#            " pandas/tests/dtypes/cast/test_promote.py"
#            " pandas/tests/dtypes/test_common.py"
#            " pandas/tests/dtypes/test_dtypes.py"
#            " pandas/tests/dtypes/test_missing.py"
#            " pandas/tests/extension/test_common.py"
#            " pandas/tests/extension/test_datetime.py"
#            " pandas/tests/extension/test_interval.py"
#            " pandas/tests/extension/test_period.py"
#            " pandas/tests/frame/indexing/test_categorical.py"
#            " pandas/tests/frame/test_dtypes.py"
#            " pandas/tests/frame/test_timezones.py"
#            " pandas/tests/indexes/categorical/test_category.py"
#            " pandas/tests/indexes/interval/test_astype.py"
#            " pandas/tests/indexes/interval/test_constructors.py"
#            " pandas/tests/indexes/multi/test_astype.py"
#            " pandas/tests/indexes/period/test_constructors.py"
#            " pandas/tests/indexing/test_categorical.py"
#            " pandas/tests/io/json/test_json_table_schema.py"
#            " pandas/tests/io/parser/test_dtypes.py"
#            " pandas/tests/reshape/merge/test_merge.py"
#            " pandas/tests/reshape/test_concat.py"
#            " pandas/tests/series/test_constructors.py"
#            " pandas/tests/series/test_dtypes.py"
#            " pandas/tests/test_algos.py"
#            " --src pandas --exclude [pandas/tests] --granularity statement --family sbfl --failing-list [pandas/tests/dtypes/test_dtypes.py::TestCategoricalDtype::test_from_values_or_dtype_invalid_dtype]")
# print(command)
# runCommandScript(command, workDir)


# workDir = "/home/moe/Desktop/SI_SEMINAR/si_example/example"
# command = ["python", "-m", "pytest", "test",
#            "--src", "my_code", "--family", "sbfl", "--granularity", "statement", "--top-n", "30",
#            # "--no-cov"
#            ]
# runCommand(command, workDir)


# workDir = "/home/moe/BugsInPyExp/cookiecutter/bug4/buggy/cookiecutter"
# command = 'python -m pytest tests/test_hooks.py::TestExternalHooks::test_run_failing_hook --src cookiecutter --granularity statement --family ps'
# print(command)
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/keras/bug5/buggy/keras"
# command = 'python -m pytest tests/keras/layers/merge_test.py tests/keras/utils/data_utils_test.py --src . --exclude [env,tests] --granularity statement --family mbfl --failing-list [tests/keras/utils/data_utils_test.py::test_data_utils]'
# print(command)
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/sanic/bug5/buggy/sanic"
# command = 'python -m pytest tests/test_logging.py --src . --granularity statement --family mbfl --exclude [env,tests]'
# print(command)
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/fastapi/bug3/buggy/fastapi"
# command = ("python -m pytest "
#            " tests/test_serialize_response_model.py"
#            " tests/test_additional_response_extra.py"
#            " tests/test_additional_responses_router.py"
#            " tests/test_custom_route_class.py"
#            " tests/test_default_response_class.py"
#            " tests/test_default_response_class_router.py"
#            " tests/test_dependency_overrides.py"
#            " tests/test_empty_router.py"
#            " tests/test_include_route.py"
#            " tests/test_infer_param_optionality.py"
#            " tests/test_router_events.py"
#            " tests/test_router_prefix_with_template.py"
#            " tests/test_sub_callbacks.py"
#            " tests/test_ws_router.py"
#            " --src fastapi --granularity function --family st")
# print(command)
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/pandas/bug12/buggy/pandas"
# command = ("python -m pytest pandas/tests/frame/methods/test_cov_corr.py::TestDataFrameCov::test_cov_nullable_integer "
#            " --src pandas --granularity statement --family ps --failing-list [pandas/tests/frame/methods/test_cov_corr.py::TestDataFrameCov::test_cov_nullable_integer]")
# print(command)
# runCommandScript(command, workDir)


# workDir = "/home/moe/BugsInPyExp/fastapi/bug11/buggy/fastapi"
# command = ("python -m pytest "
#            " tests/test_union_inherited_body.py"
#            " tests/test_union_body.py"
#            " --src fastapi --granularity statement --family ps --failing-list ["
#            "tests/test_union_body.py::test_item_openapi_schema,"
#            "tests/test_union_body.py::test_post_other_item,"
#            "tests/test_union_body.py::test_post_item,"
#            "tests/test_union_inherited_body.py::test_inherited_item_openapi_schema,"
#            "tests/test_union_inherited_body.py::test_post_extended_item,"
#            "tests/test_union_inherited_body.py::test_post_item"
#            "]")
# print(command)
# runCommandScript(command, workDir)


workDir = "/home/moe/BugsInPyExp/pandas/bug141/buggy/pandas"
command = ("python -m pytest "
           " pandas/tests/indexes/test_range.py::TestRangeIndex::test_get_indexer_decreasing"
           " --src pandas --granularity statement --family ps "
           "--failing-list ["
           "pandas/tests/indexes/test_range.py::TestRangeIndex::test_get_indexer_decreasing"
           "]"
           )
print(command)
runCommandScript(command, workDir)
