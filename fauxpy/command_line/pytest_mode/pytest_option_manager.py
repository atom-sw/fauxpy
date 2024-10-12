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
            f"fauxpy", description=f"FauxPy {__version__}"
        )
        group.addoption("--src", help="Directory to perform fault localization on.")
        group.addoption("--exclude", default="[]", help="List of paths to be excluded.")
        group.addoption("--family", default="sbfl", help="Options: sbfl/mbfl/ps/st")
        group.addoption(
            "--granularity", default="statement", help="Options: statement/function"
        )
        group.addoption("--top-n", default="-1", help="Options: int[1,]]/-1(all).")
        group.addoption(
            "--failing-file",
            default=None,
            help="Path to the file containing the targeted failing tests.",
        )
        group.addoption(
            "--failing-list",
            default=None,
            help="A list containing the targeted failing tests.",
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
