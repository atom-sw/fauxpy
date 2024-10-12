from pathlib import Path
from typing import List

import coverage

from fauxpy import constants
from fauxpy.command_line.pytest_mode import legacy_input
from fauxpy.fault_localization.granularity.db_manager import FunctionLevelDbManager
from fauxpy.fault_localization.granularity.function_level import (
    FunctionLevelGranularity,
)
from fauxpy.fault_localization.sbfl.covered_function_manager import (
    CoveredFunctionManager,
)
from fauxpy.fault_localization.sbfl.db_manager import SbflDbManager
from fauxpy.fault_localization.sbfl.ranking_metric_manager import RankingMetricManager
from fauxpy.fault_localization.util.path_util import PathUtil
from fauxpy.session_lib import naming_lib
from fauxpy.session_lib.fl_session import FlSession
from fauxpy.session_lib.fl_type import FlGranularity
from fauxpy.session_lib.path_lib import PythonPath
from fauxpy.session_lib.ts_lib import TargetedFailingTst
from fauxpy.session_lib.pytest_tst_item import PytestTstItem


class SbflSession(FlSession):
    def __init__(
        self,
        target_src: PythonPath,
        exclude_list: List[PythonPath],
        fl_granularity: FlGranularity,
        top_n: int,
        targeted_failing_test_list: List[TargetedFailingTst],
        report_directory_path: Path,
        project_working_directory: Path,
    ):

        self._target_src = target_src
        self._exclude_list = exclude_list
        self._fl_granularity = fl_granularity
        self._top_n = top_n
        self._targeted_failing_test_list = targeted_failing_test_list

        # TODO: Good idea to change the data base file name
        #  like this _Cov = coverage.Coverage(data_suffix="fauxpy").
        #  Apply it to MBFL and PS as well.
        #  Test it for Python 3.6, 3.7, and 3.8.
        #  The API of Coverage.py changes in different version.
        self._coverage_manager = coverage.Coverage()

        self._current_test_name = None
        self._db_manager = SbflDbManager(report_directory_path)
        self._ranking_metric_manager = RankingMetricManager(self._db_manager)
        self._function_level_db_manager = FunctionLevelDbManager(report_directory_path)
        self._function_level_granularity_manager = FunctionLevelGranularity(
            self._function_level_db_manager
        )
        self._covered_function_manager = CoveredFunctionManager(
            self._function_level_granularity_manager
        )
        self._path_util = PathUtil(project_working_directory)

    def __str__(self):
        return "SBFL session object"

    def run_test_call(self, item):
        self._current_test_name = PytestTstItem(item).get_test_name()
        self._coverage_manager.start()

    def run_test_make_report(self, item, call):
        if call.when == constants.PYTEST_CALL:
            test_name = PytestTstItem(item).get_test_name()
            if test_name != self._current_test_name:
                raise Exception(
                    f"Expected to stop coverage for '{self._current_test_name}', but found '{test_name}' instead."
                )
            self._coverage_manager.stop()
            coverage_data = self._coverage_manager.get_data()
            files_covered = coverage_data.measured_files()

            covered_statement_list = []
            for file in files_covered:
                if self._path_util.path_should_be_localized(
                    legacy_input.get_src_legacy(self._target_src),
                    legacy_input.get_exclude_legacy(self._exclude_list),
                    file,
                ):
                    line_list = coverage_data.lines(file)
                    for line in line_list:
                        covered_statement_list.append((file, line))
            if len(covered_statement_list) == 0:
                self._db_manager.insert_empty_test(test_name)
            else:
                if self._fl_granularity == FlGranularity.Statement:
                    covered_statement_name_list = [
                        naming_lib.get_statement_name(x[0], x[1])
                        for x in covered_statement_list
                    ]
                    self._db_manager.insert_execution_trace(
                        test_name, covered_statement_name_list
                    )
                elif self._fl_granularity == FlGranularity.Function:
                    covered_function_name_list = (
                        self._covered_function_manager.get_covered_function_names(
                            covered_statement_list
                        )
                    )
                    self._db_manager.insert_execution_trace(
                        test_name, covered_function_name_list
                    )
                else:
                    # TODO: Probably can be removed. We have input validation now.
                    raise Exception(
                        f"Granularity '{self._fl_granularity.name.lower()}' is not supported."
                    )

            self._coverage_manager.erase()

    def terminal_summary(self, terminal_reporter, exit_status):
        for key, value in terminal_reporter.stats.items():
            if key in [constants.PYTEST_PASSED, constants.PYTEST_FAILED]:
                for test_report in value:
                    test_information = PytestTstItem(test_report)
                    test_path = test_information.get_path()
                    test_method_name = test_information.get_method_name()

                    target = False
                    if (
                        legacy_input.get_targeted_failing_test_list_legacy(
                            self._targeted_failing_test_list
                        )
                        is not None
                        and key == constants.PYTEST_FAILED
                    ):
                        target = legacy_input.get_targeted_failing_test_list_legacy(
                            self._targeted_failing_test_list
                        ).is_target_test(test_path, test_method_name)
                    elif (
                        legacy_input.get_targeted_failing_test_list_legacy(
                            self._targeted_failing_test_list
                        )
                        is None
                        and key == constants.PYTEST_FAILED
                    ):
                        target = True

                    test_name = test_information.get_test_name()
                    self._db_manager.insert_test_case(test_name, key, target)

        score_entity_list = self._ranking_metric_manager.compute_sorted_scores(
            self._top_n
        )

        self._db_manager.end()
        self._function_level_db_manager.end()

        return score_entity_list
