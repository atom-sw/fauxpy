from pathlib import Path
from typing import List

import coverage

from fauxpy import program_tracer
from fauxpy.command_line.pytest_mode import legacy_input
from fauxpy.fault_localization.granularity.db_manager import FunctionLevelDbManager
from fauxpy.fault_localization.mbfl.db_manager import MbflDbManager
from fauxpy.fault_localization.mbfl.entity_score_manager import EntityScoreManager
from fauxpy.fault_localization.mbfl.mutant_score_manager import MutantScoreManager
from fauxpy.fault_localization.mbfl.mutation_manager import MutationManager
from fauxpy.fault_localization.mbfl.run_manager import RunManager
from fauxpy.fault_localization.util import timeout
from fauxpy.fault_localization.util.path_util import PathUtil
from fauxpy.fault_localization.util.traceback_lib import TracebackParser
from fauxpy.session_lib import naming_lib
from fauxpy.session_lib.fl_session import FlSession
from fauxpy.session_lib.fl_type import FlGranularity
from fauxpy.session_lib.path_lib import PythonPath
from fauxpy.session_lib.timer import Timer
from fauxpy.session_lib.ts_lib import TargetedFailingTst
from fauxpy.session_lib.pytest_tst_item import PytestTstItem


class MbflSession(FlSession):

    # TODO: Program tracer does not work right now.
    _Use_coverage_lib = True

    def __init__(
        self,
        target_src: PythonPath,
        exclude_list: List[PythonPath],
        fl_granularity: FlGranularity,
        top_n: int,
        targeted_failing_test_list: List[TargetedFailingTst],
        file_or_dir,
        report_directory_path: Path,
        project_working_directory: Path,
    ):
        self._target_src = target_src
        self._exclude_list = exclude_list
        self._fl_granularity = fl_granularity
        self._top_n = top_n
        self._targeted_failing_test_list = targeted_failing_test_list
        self._file_or_dir = file_or_dir

        self._coverage_manager = coverage.Coverage()
        self._current_test_name = None
        self._db_manager = MbflDbManager(report_directory_path)
        self._current_test_timer = Timer()
        self._function_level_db_manager = FunctionLevelDbManager(report_directory_path)
        self._run_manager = RunManager(
            self._db_manager, self._function_level_db_manager, project_working_directory
        )
        self._mutant_score_manager = MutantScoreManager(self._db_manager)
        self._entity_score_manager = EntityScoreManager(self._db_manager)
        self._mutation_manager = MutationManager(self._db_manager)
        self._traceback_parser = TracebackParser(project_working_directory)
        self._path_util = PathUtil(project_working_directory)

    @staticmethod
    def __pretty_representation():
        return "MBFL family"

    def __str__(self):
        return self.__pretty_representation()

    def __repr__(self):
        return self.__pretty_representation()

    def run_test_call(self, item):
        self._current_test_timer.start_timer()

        self._current_test_name = PytestTstItem(item).get_test_name()
        if self._Use_coverage_lib:
            self._coverage_manager.start()
        else:
            program_tracer.start(
                isWanted=lambda x: self._path_util.path_should_be_localized(
                    legacy_input.get_src_legacy(self._target_src),
                    legacy_input.get_exclude_legacy(self._exclude_list),
                    x,
                )
            )

    def run_test_make_report(self, item, call):
        # TODO: Replace custom tracer with coverage library (commented code). Coverage tool does not
        #  work on cookiecutter project. Not found the reason. Probably timeout is the problem
        #  and the project having only one mutant. Increasing the
        #  timeout solved the problem for now.

        if call.when == "call":
            test_name = PytestTstItem(item).get_test_name()
            if test_name != self._current_test_name:
                raise Exception(
                    f"Starting coverage for {self._current_test_name}. But closing coverage for {test_name}."
                )

            if self._Use_coverage_lib:
                self._coverage_manager.stop()
                coverage_data = self._coverage_manager.get_data()
                covered_statement_list = []
                covered_file_list = coverage_data.measured_files()
                for file in covered_file_list:
                    if self._path_util.path_should_be_localized(
                        legacy_input.get_src_legacy(self._target_src),
                        legacy_input.get_exclude_legacy(self._exclude_list),
                        file,
                    ):
                        lines = coverage_data.lines(file)
                        for line in lines:
                            covered_statement_list.append((file, line))
                self._coverage_manager.erase()
            else:
                program_tracer.stop()
                execution_trace = program_tracer.getExecutionTrace()
                covered_statement_list = execution_trace.getExecutedLinesNoOrder()

            if len(covered_statement_list) == 0:
                self._db_manager.insert_empty_test(test_name)
            else:
                covered_statement_names = [
                    naming_lib.get_statement_name(x[0], x[1])
                    for x in covered_statement_list
                ]
                self._db_manager.insert_execution_trace(
                    test_name, covered_statement_names
                )

            # # Let's give more time to mutants by putting these lines after
            current_test_time = self._current_test_timer.end_timer()
            self._db_manager.insert_test_time(test_name, current_test_time)

    def terminal_summary(self, terminal_reporter, exit_status):
        for key, value in terminal_reporter.stats.items():
            if key in ["passed", "failed"]:
                for test_report in value:
                    test_information = PytestTstItem(test_report)
                    test_path = test_information.get_path()
                    test_method_name = test_information.get_method_name()

                    test_name = test_information.get_test_name()
                    test_trace_back = ""
                    timeout_stat = -1
                    target = False
                    if key == "failed":
                        if (
                            legacy_input.get_targeted_failing_test_list_legacy(
                                self._targeted_failing_test_list
                            )
                            is not None
                        ):
                            target = legacy_input.get_targeted_failing_test_list_legacy(
                                self._targeted_failing_test_list
                            ).is_target_test(test_path, test_method_name)
                        elif (
                            legacy_input.get_targeted_failing_test_list_legacy(
                                self._targeted_failing_test_list
                            )
                            is None
                        ):
                            target = True
                        repr_traceback = test_report.longrepr.reprtraceback
                        test_trace_back = (
                            self._traceback_parser.get_short_trace_back_info(
                                repr_traceback
                            )
                        )
                        if self._traceback_parser.has_timeout_happened(
                            test_report.longreprtext
                        ):
                            timeout_stat = 1

                    self._db_manager.insert_test_case_run(
                        test_name, key, test_trace_back, timeout_stat, target
                    )

        failing_line_numbers = (
            self._db_manager.select_distinct_line_numbers_covered_by_failing_tests()
        )
        mutant_list = (
            self._mutation_manager.get_all_mutants_for_failing_line_number_list(
                failing_line_numbers
            )
        )

        # Storing mutants for possible further analysis (can be removed)
        for mutant in mutant_list:
            self._db_manager.insert_mutant(
                mutant.get_id(),
                mutant.get_module_path(),
                mutant.get_line_number(),
                mutant.get_module_operator(),
                mutant.get_module_diff_as_text(),
                mutant.get_start_pos(),
                mutant.get_end_pos(),
            )

        # TODO: Get time from passing tests and target failing tests.
        max_test_time = self._db_manager.select_max_test_time()
        timeout_limit = timeout.get_timeout(max_test_time)
        num_passed, num_failed = self._db_manager.select_number_of_tests()
        num_all_tests = num_passed + num_failed
        process_timeout = timeout.get_process_timeout(num_all_tests, timeout_limit)
        self._run_manager.run_all_mutants_store_db(
            mutant_list,
            self._file_or_dir,
            legacy_input.get_granularity_legacy(self._fl_granularity),
            legacy_input.get_src_legacy(self._target_src),
            legacy_input.get_exclude_legacy(self._exclude_list),
            timeout_limit,
            num_all_tests,
            process_timeout,
        )
        self._mutant_score_manager.compute_mutant_scores_store_db()
        scored_entity_list = self._entity_score_manager.compute_entity_scores_store_db(
            self._top_n
        )

        self._db_manager.end()
        self._function_level_db_manager.end()

        return scored_entity_list
