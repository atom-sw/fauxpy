import logging
from typing import Optional

from fauxpy.command_line.pytest_mode.pytest_option_manager import PytestOptionManager
from fauxpy.session_lib.fauxpy_printer import fl_print
from fauxpy.session_lib.fauxpy_session_type import FauxpySessionType
from fauxpy.session_lib.fl_family_session import FlFamilySession
from fauxpy.session_lib.fl_session import FlSession
from fauxpy.session_lib.fl_session_report import FlSessionReport
from fauxpy.session_lib.timer import Timer


class FauxpyPytestModeHandler:
    """
    Handles Pytest Mode by interacting with Pytest through various hooks.
    """

    def __init__(self):
        self._session_timer = Timer()
        self._pytest_option_manager = PytestOptionManager()
        self._fauxpy_session_type = FauxpySessionType.FauxpyNotCalled
        self._session_object: Optional[FlSession] = None
        self._session_file_manager = None

    def add_option(self, pytest_parser):
        """
        Adds FauxPy-specific command-line options to the pytest parser.

        Args:
            pytest_parser: The Pytest parser object to which FauxPy options should be added.
        """
        self._pytest_option_manager.add_fauxpy_options(pytest_parser)

    def configure(self, pytest_config):
        """
        Configures the FauxPy session.

        Args:
            pytest_config: The Pytest configuration object used to determine the session type
            and options.
        """
        self._fauxpy_session_type = self._pytest_option_manager.get_fauxpy_session_type(
            pytest_config
        )
        if self._fauxpy_session_type == FauxpySessionType.FaultLocalization:
            self._session_timer.start()

            fl_option_manager = self._pytest_option_manager.get_fl_option_manager(
                pytest_config
            )

            self._session_object = fl_option_manager.get_fl_session()
            self._session_file_manager = fl_option_manager.get_session_file_manager()

            logging.basicConfig(
                filename=self._session_file_manager.get_log_file_path(),
                level=logging.DEBUG,
                format="%(asctime)s %(message)s",
                filemode="w",
            )

            if isinstance(self._session_object, FlFamilySession):
                self._session_file_manager.save_config_to_file(
                    target_src=fl_option_manager.get_target_src(),
                    exclude_list=fl_option_manager.get_exclude_list(),
                    fl_family=fl_option_manager.get_fl_family(),
                    fl_granularity=fl_option_manager.get_fl_granularity(),
                    top_n=fl_option_manager.get_top_n(),
                    targeted_failing_test_list=fl_option_manager.get_targeted_failing_test_list(),
                    mutation_strategy=fl_option_manager.get_mutation_strategy()
                )

    def runtest_call(self, item):
        """
        Handles the test call event during test execution.

        Args:
            item: The pytest item representing the test being executed.
        """
        if self._fauxpy_session_type == FauxpySessionType.FaultLocalization:
            self._session_object.run_test_call(item)

    def runtest_make_report(self, item, call):
        """
        Gathers the test results and generates reports after a test call is executed.

        Args:
            item: The Pytest item representing the test that was executed.
            call: The Pytest call object containing the results of the test (setup, call, teardown).
        """
        if self._fauxpy_session_type == FauxpySessionType.FaultLocalization:
            self._session_object.run_test_make_report(item, call)

    def terminal_summary(self, terminal_reporter, exitstatus):
        """
        Generates final results after all tests have completed.

        Args:
            terminal_reporter: The Pytest terminal reporter object used for output.
            exitstatus: The exit status of Pytest, indicating success or failure.
        """
        if self._fauxpy_session_type == FauxpySessionType.FaultLocalization:
            banner_start = (
                "***************************************************\n"
                "                FauxPy Started!                    \n"
                "***************************************************\n"
            )
            print("\n")
            print(banner_start)

            fl_print.normal(f"Running {self._session_object}")

            if (isinstance(self._session_object, FlFamilySession) and
                    len(self._session_object.get_targeted_failing_test_list()) > 0):
                fl_print.normal("Targeted failing tests:")
                for index, item in enumerate(self._session_object.get_targeted_failing_test_list()):
                    fl_print.normal(f"  {index + 1}. {item}")

            print("\n")
            banner_dynamic_analysis = (
                               "==============================\n"
                               " Dynamic Analysis in Progress \n"
                               "==============================\n"
            )
            print(banner_dynamic_analysis)

            score_entity_list = self._session_object.terminal_summary(
                terminal_reporter, exitstatus
            )

            print("\n")
            print("--- Dynamic Analysis Complete ---")

            session_time = self._session_timer.end()
            self._session_file_manager.save_delta_time_to_file(session_time)

            for technique, score_list in score_entity_list.items():
                self._session_file_manager.save_scores_to_file(technique, score_list)

            if isinstance(self._session_object, FlFamilySession):
                fl_session_report = FlSessionReport(
                    score_entity_list,
                    session_time,
                    self._session_object.get_fl_granularity(),
                    self._session_object.get_project_working_directory()
                )
                report_string = fl_session_report.generate_report()
                print(report_string)

            banner_end = (
                "**************************************************\n"
                "                FauxPy Ended!                     \n"
                "**************************************************\n"
            )
            print(banner_end)
