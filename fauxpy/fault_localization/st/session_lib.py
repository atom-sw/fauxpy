from pathlib import Path
from typing import List

from fauxpy.command_line.pytest_mode import legacy_input
from fauxpy.fault_localization.granularity.db_manager import FunctionLevelDbManager
from fauxpy.fault_localization.granularity.function_level import (
    FunctionLevelGranularity,
)
from fauxpy.fault_localization.st.db_manager import StDbManager
from fauxpy.fault_localization.st.rank_manager import RankManager
from fauxpy.fault_localization.st.traceback_parser import TracebackParser
from fauxpy.session_lib.fl_session import FlSession
from fauxpy.session_lib.path_lib import PythonPath
from fauxpy.session_lib.ts_lib import TargetedFailingTst
from fauxpy.session_lib.pytest_tst_item import PytestTstItem


class StSession(FlSession):
    def __init__(
        self,
        target_src: PythonPath,
        exclude_list: List[PythonPath],
        top_n: int,
        targeted_failing_test_list: List[TargetedFailingTst],
        report_directory_path: Path,
        project_working_directory: Path,
    ):
        self._target_src = target_src
        self._exclude_list = exclude_list
        self._top_n = top_n
        self._targeted_failing_test_list = targeted_failing_test_list

        self._current_test_name = None
        self._db_manager = StDbManager(report_directory_path)
        self._function_level_db_manager = FunctionLevelDbManager(report_directory_path)
        self._function_level_granularity_manager = FunctionLevelGranularity(
            self._function_level_db_manager
        )
        self._traceback_parser = TracebackParser(
            self._function_level_granularity_manager, project_working_directory
        )
        self._rank_manager = RankManager(self._db_manager)

    @staticmethod
    def __pretty_representation():
        return "ST family"

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
                    f"Starting coverage for {self._current_test_name}. But closing coverage for {test_name}."
                )

    def terminal_summary(self, terminal_reporter, exit_status):
        for key, value in terminal_reporter.stats.items():
            if key in ["failed"]:
                for test_report in value:
                    test_information = PytestTstItem(test_report)
                    test_path = test_information.get_path()
                    test_method_name = test_information.get_method_name()

                    if (
                        legacy_input.get_targeted_failing_test_list_legacy(
                            self._targeted_failing_test_list
                        )
                        is not None
                        and legacy_input.get_targeted_failing_test_list_legacy(
                            self._targeted_failing_test_list
                        ).is_target_test(test_path, test_method_name)
                    ) or legacy_input.get_targeted_failing_test_list_legacy(
                        self._targeted_failing_test_list
                    ) is None:
                        current_test = test_information.get_test_name()
                        repr_traceback = test_report.longrepr.reprtraceback
                        traceback_function_name_list = self._traceback_parser.get_ordered_traceback_function_name_list(
                            legacy_input.get_src_legacy(self._target_src),
                            legacy_input.get_exclude_legacy(self._exclude_list),
                            repr_traceback,
                        )
                        current_test_score_list = self._rank_manager.compute_score_list(
                            traceback_function_name_list
                        )
                        self._db_manager.insert_traceback_scores(
                            current_test, current_test_score_list
                        )

        scored_entity_list = self._rank_manager.get_sorted_score_list(self._top_n)

        self._db_manager.end()
        self._function_level_db_manager.end()

        return {"default": scored_entity_list}
