import logging

from fauxpy.command_line.pytest_mode import legacy_input
from fauxpy.command_line.pytest_mode.pytest_option_manager import PytestOptionManager
from fauxpy.session_lib.fauxpy_session_type import FauxpySessionType
from fauxpy.session_lib.timer import Timer

Logger = logging.getLogger()


class FauxpyPytestModeHandler:
    """
    Handles Pytest Mode by interacting with Pytest through various hooks.
    """

    def __init__(self):
        self._ex_timer = Timer()
        self._pytest_option_manager = PytestOptionManager()
        self._fauxpy_session_type = FauxpySessionType.FauxpyNotCalled
        self._session_object = None
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
            self._ex_timer.start_timer()

            fl_option_manager = self._pytest_option_manager.get_fl_option_manager(
                pytest_config
            )

            targeted_failing_test_list_legacy = (
                legacy_input.get_targeted_failing_test_list_legacy(
                    fl_option_manager.get_targeted_failing_test_list()
                )
            )

            self._session_file_manager = fl_option_manager.get_session_file_manager()

            logging.basicConfig(
                filename=self._session_file_manager.get_log_file_path(),
                format="%(asctime)s %(message)s",
                filemode="w",
            )

            self._session_object = fl_option_manager.get_fl_session()

            if targeted_failing_test_list_legacy is not None:
                print("----------- TARGET FAILING TESTS -----------")
                for item in targeted_failing_test_list_legacy.get_failing_tests():
                    print(item)
                print("----------- TARGET FAILING TEST -----------")

            legacy_input.save_config_info_legacy(
                pytest_config, self._session_file_manager
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
            score_entities = self._session_object.terminal_summary(
                terminal_reporter, exitstatus
            )

            for technique, scores in score_entities.items():
                self._session_file_manager.save_scores_to_file(technique, scores)
                print(f" ----- Scores for {technique} ----- ")
                for score in scores:
                    print(score)

            delta_time = self._ex_timer.end_timer()
            self._session_file_manager.save_delta_time_to_file(delta_time)
            print("DeltaTime: ", delta_time)
