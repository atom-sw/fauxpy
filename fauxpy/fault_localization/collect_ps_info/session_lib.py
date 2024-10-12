from pathlib import Path

from fauxpy.fault_localization.collect_ps_info.db_manager import (
    CollectPsInfoDbManager,
)
from fauxpy.fault_localization.collect_ps_info.reporter_lib import CollectPsInfoReporter
from fauxpy.fault_localization.collect_ps_info.session_file import (
    CollectPsInfoSessionFileManager,
)
from fauxpy.session_lib.fl_session import FlSession
from fauxpy.session_lib.pytest_tst_item import PytestTstItem


class CollectPsInfoSession(FlSession):
    def __init__(self, report_directory_path: Path, project_working_directory: Path):
        self._current_test_name = None
        self._db_manager = CollectPsInfoDbManager(report_directory_path)
        self._reporter = CollectPsInfoReporter(self._db_manager)
        self._session_file_manager = CollectPsInfoSessionFileManager(
            report_directory_path, project_working_directory
        )

    @staticmethod
    def __pretty_representation():
        return "Collect PS Info Mode"

    def __str__(self):
        return self.__pretty_representation()

    def __repr__(self):
        return self.__pretty_representation()

    def run_test_call(self, item):
        self._current_test_name = PytestTstItem(item).get_test_name()

    def run_test_make_report(self, item, call):
        if call.when == "call":
            test_name = PytestTstItem(item).get_test_name()
            if test_name != self._current_test_name:
                raise Exception(
                    f"Starting with {self._current_test_name}, but ending with {test_name}."
                )

            predicate_sequence = (
                self._session_file_manager.load_executed_predicate_sequence_and_remove_file()
            )
            if predicate_sequence is not None:
                self._db_manager.insert_predicate_sequence(
                    test_name, predicate_sequence
                )

    def terminal_summary(self, terminal_reporter, exit_status):
        predicate_sequence_table = (
            self._reporter.get_json_test_predicate_sequence_table()
        )
        self._session_file_manager.save_predicate_sequence_table(
            predicate_sequence_table
        )
        self._db_manager.end()
        return {"Default": []}
