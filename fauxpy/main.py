from fauxpy.command_line.analysis_mode.handler import FauxpyAnalysisModeHandler
from fauxpy.command_line.pytest_mode.handler import FauxpyPytestModeHandler

_Fauxpy_pytest_mode_handler = FauxpyPytestModeHandler()


def pytest_addoption(parser):
    """
    This hook is called by Pytest, allowing plugins such as FauxPy to
    add custom options.

    Args:
        parser: The Pytest parser object.
    """
    global _Fauxpy_pytest_mode_handler

    _Fauxpy_pytest_mode_handler.add_option(parser)


def pytest_configure(config):
    """
    This hook is called by Pytest to allow FauxPy to initialize and configure
    itself before test execution begins.

    Args:
        config: The Pytest configuration object, which holds configuration options
        and settings for the current test session.
    """
    global _Fauxpy_pytest_mode_handler

    _Fauxpy_pytest_mode_handler.configure(config)


def pytest_runtest_call(item):
    """
    This hook is called by Pytest just before running a test.

    Args:
        item: The test item (or node) being executed.
    """
    global _Fauxpy_pytest_mode_handler

    _Fauxpy_pytest_mode_handler.runtest_call(item)


def pytest_runtest_makereport(item, call):
    """
    This hook is called by Pytest after each test.

    Args:
        item: The test item that was executed.
        call: The test phase object representing the test's setup, call, or teardown phase.
    """
    global _Fauxpy_pytest_mode_handler

    _Fauxpy_pytest_mode_handler.runtest_make_report(item, call)


def pytest_terminal_summary(terminalreporter, exitstatus):
    """
    This hook is called by Pytest after all tests are completed.

    Args:
        terminalreporter: The Pytest terminal reporter object, used to output results.
        exitstatus: The final exit status of the Pytest session, indicating success or failure.
    """
    global _Fauxpy_pytest_mode_handler

    _Fauxpy_pytest_mode_handler.terminal_summary(terminalreporter, exitstatus)


def fauxpy_analysis_mode():
    """
    Entry point for FauxPy's Analysis Mode.

    This function is called when FauxPy is invoked in Analysis Mode.
    """
    fauxpy_command_mode_handler = FauxpyAnalysisModeHandler()
    fauxpy_command_mode_handler.main()
