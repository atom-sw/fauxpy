import os

from fauxpy.command_line.pytest_mode.fl_option_manager import FlOptionManager
from fauxpy.session_lib.fauxpy_session_type import FauxpySessionType
from fauxpy.version import __version__


class PytestOptionManager:
    """
    Manages the command-line options for FauxPy in pytest.
    """

    def __init__(self):
        """
        Initializes the PytestOptionManager with the project working directory.
        """
        self._project_working_directory = os.getcwd()

    @staticmethod
    def add_fauxpy_options(pytest_option_parser):
        """
        Adds FauxPy-specific command-line options to the pytest option parser.

        Args:
            pytest_option_parser: The pytest parser object.
        """
        group = pytest_option_parser.getgroup(
            "fauxpy",
            description="FauxPy " + __version__ + " - A tool for automated fault localization in Python programs"
        )
        group.addoption(
            "--src",
            help="Specify the source directory for fault localization. If not provided, FauxPy will be disabled, and pytest will run normally."
        )
        group.addoption(
            "--exclude",
            default="[]",
            help="Provide a list of paths to be excluded from analysis. Default is an empty list."
        )
        group.addoption(
            "--family",
            default="sbfl",
            help="Select the fault localization family to use. Options are: "
                 "sbfl (Spectrum-Based Fault Localization), "
                 "mbfl (Mutation-Based Fault Localization), "
                 "ps (Predicate Switching), "
                 "st (Stack-Trace). Default is sbfl."
        )
        group.addoption(
            "--mutation",
            default="t",
            help="Specify the mutation generation strategy for Mutation-Based Fault Localization (MBFL). Options: "
                 "t - Use Cosmic Ray with traditional mutation operators (default), "
                 "tgpt4ominiapi - Use Cosmic Ray, and when it cannot generate a mutant for a statement, fall back to GPT-4o-mini via its API, "
                 "gpt4ominiapi - Use only GPT-4o-mini via its API for mutant generation, without Cosmic Ray, "
                 "tgpt4oapi - Use Cosmic Ray, and when it cannot generate a mutant for a statement, fall back to GPT-4o via its API, "
                 "gpt4oapi - Use only GPT-4o via its API for mutant generation, without Cosmic Ray."
        )
        group.addoption(
            "--granularity",
            default="statement",
            help="Set the granularity level for fault localization. Options are: "
                 "statement (or s) for statement-level analysis, "
                 "function (or f) for function-level analysis. Default is statement."
        )
        group.addoption(
            "--top-n",
            default="-1",
            help="Specify the number of top suspicious code elements to report. "
                 "Provide a positive integer to limit the results, or -1 to include all elements. Default is -1."
        )
        group.addoption(
            "--failing-file",
            default=None,
            help="Path to a file containing the list of targeted failing tests. Each line should represent a test identifier. Default is None."
        )
        group.addoption(
            "--failing-list",
            default=None,
            help="Provide a list of targeted failing tests. Default is None."
        )

    def get_fl_option_manager(self, pytest_config) -> FlOptionManager:
        """
        Retrieves a FlOptionManager configured with the options from pytest.

        Args:
            pytest_config: The pytest configuration object.

        Returns:
            FlOptionManager: An instance of FlOptionManager configured with the current pytest options.
        """
        target_src_opt = pytest_config.getoption("--src")
        exclude_list_opt = pytest_config.getoption("--exclude")
        fl_family_opt = pytest_config.getoption("--family")
        mutation_strategy_opt = pytest_config.getoption("--mutation")
        fl_granularity_opt = pytest_config.getoption("--granularity")
        top_n_opt = pytest_config.getoption("--top-n")
        failing_file_opt = pytest_config.getoption("--failing-file")
        failing_list_opt = pytest_config.getoption("--failing-list")
        file_or_dir = pytest_config.getoption("file_or_dir")

        fl_option_manager = FlOptionManager(
            self._project_working_directory,
            target_src_opt,
            exclude_list_opt,
            fl_family_opt,
            mutation_strategy_opt,
            fl_granularity_opt,
            top_n_opt,
            failing_file_opt,
            failing_list_opt,
            file_or_dir,
        )

        return fl_option_manager

    @staticmethod
    def get_fauxpy_session_type(pytest_config):
        """
        Determines the type of FauxPy session based on pytest options.

        Args:
            pytest_config: The pytest configuration object.

        Returns:
            FauxpySessionType: The type of FauxPy session.
        """
        if pytest_config.getoption("--src") is not None:
            return FauxpySessionType.FaultLocalization
        else:
            return FauxpySessionType.FauxpyNotCalled
