import shutil
from pathlib import Path
from typing import List, Tuple, Optional

from fauxpy.fault_localization.collect_ps_info.api_lib import CollectPsInfoApi
from fauxpy.fault_localization.collect_ps_run.api_lib import CollectPsRunApi
from fauxpy.fault_localization.granularity.db_manager import FunctionLevelDbManager
from fauxpy.fault_localization.granularity.function_level import (
    FunctionLevelGranularity,
)
from fauxpy.fault_localization.ps.ast_lib.instrumentation_manager import (
    InstrumentationManager,
)
from fauxpy.fault_localization.ps.db_manager import PsDbManager
from fauxpy.fault_localization.ps.predicate_instance_manager import (
    PredicateInstanceManager,
)
from fauxpy.fault_localization.ps.seen_exception_manager import SeenExceptionManager
from fauxpy.fault_localization.util.path_util import PathUtil
from fauxpy.fault_localization.util.temp_lib import TempManager
from fauxpy.session_lib import naming_lib
from fauxpy.session_lib.target_tsts import TargetFailingTests


class AlgorithmManager:
    def __init__(
        self,
        db_manager: PsDbManager,
        function_level_db_manager: FunctionLevelDbManager,
        project_working_directory: Path,
    ):
        self._db_manager = db_manager
        self._seen_exception_manager = SeenExceptionManager(self._db_manager)
        self._predicate_instance_manager = PredicateInstanceManager(self._db_manager)
        self._instrumentation_manager = InstrumentationManager()
        self._collect_ps_info_api = CollectPsInfoApi()
        self._collect_ps_run_api = CollectPsRunApi()
        self._function_level_granularity_manager = FunctionLevelGranularity(
            function_level_db_manager
        )
        self._temp_manager = TempManager(project_working_directory)
        self._path_util = PathUtil(project_working_directory)

    def _get_instrumented_module_list(self) -> List[Tuple[str, str]]:
        """
        Returns a list of tuples of modules paths (having at least one candidate
        predicate or a seen exception) and their instrumented content.
        """
        inst_file_paths_content: List[Tuple[str, str]] = []
        file_paths_with_candidate_predicate = (
            self._db_manager.select_distinct_candidate_predicate_file_paths()
        )
        file_paths_with_seen_exceptions = (
            self._db_manager.select_distinct_seen_exceptions_file_paths()
        )
        inst_file_paths = set(
            file_paths_with_candidate_predicate + file_paths_with_seen_exceptions
        )
        for filePath in inst_file_paths:
            candidate_predicates = (
                self._db_manager.select_candidate_predicates_for_file_path(filePath)
            )
            seen_exception_list = self._db_manager.select_seen_exceptions_for_file_path(
                filePath
            )
            inst_file_content = (
                self._instrumentation_manager.instrument_current_file_path(
                    filePath, candidate_predicates, seen_exception_list
                )
            )
            if inst_file_content is None:
                # For cases that astor cannot perform correctly
                for item in candidate_predicates:
                    line_start, line_end, predicate_name = item
                    self._db_manager.insert_astor_assert_error_info(
                        filePath, line_start, line_end, predicate_name
                    )
            else:
                inst_file_paths_content.append((filePath, inst_file_content))

        return inst_file_paths_content

    def _inject_instrumented_content_in_project(
        self, temp_project_path: str, instrumented_modules: List[Tuple[str, str]]
    ):
        """
        Replaces modules to be instrumented with their instrumented versions.
        """
        for modulePath, moduleContent in instrumented_modules:
            relative_module_path = self._path_util.absolute_path_to_relative_path(
                modulePath
            )
            absolute_temp_module_path = Path(temp_project_path) / relative_module_path
            with open(absolute_temp_module_path, "w") as file:
                file.write(moduleContent)

    @staticmethod
    def _remove_temp_project(temp_project_path):
        shutil.rmtree(temp_project_path)

    def _instrument_project(self) -> str:
        """
        Makes a copy of the project in a temporary directory, instruments it, and
         returns the path of the project copy.
        """
        inst_file_paths_content = self._get_instrumented_module_list()
        tmp_project_path = self._temp_manager.make_project_copy_in_temp()
        self._inject_instrumented_content_in_project(
            tmp_project_path, inst_file_paths_content
        )
        return tmp_project_path

    def _get_predicate_sequences(
        self, project_path: str, src: str, exclude: List[str], failed_test_paths
    ):
        """
        Runs the project in Collect mode and stores a list of tuples
        (test_name, Predicate sequence).
        @param project_path: path to the project subject to fault localization.
        """

        # TODO: Optimize the failing tests to run. Maybe running it on arg_min(failedTestPaths, fileOrDir).

        predicate_sequences = []
        indexed_predicate_sequences = (
            self._collect_ps_info_api.run_ps_collect_mode_info(
                src=src,
                exclude=exclude,
                project_path=project_path,
                file_or_dir=failed_test_paths,
            )
        )
        # exeResultData = collect_mode.getRunResult(projectPath)
        for r in indexed_predicate_sequences:
            test_name, predicate_sequence, ind_pred_seq = r
            predicate_sequences.append((test_name, ind_pred_seq))

            # Not needed.
            self._db_manager.insert_predicate_sequence_for_test(
                test_name, predicate_sequence, ind_pred_seq
            )

        return predicate_sequences

    def _get_generalized_failed_test_function_paths(self):
        """
        Returns failed test paths (i.e., TEST_FILE_PATH::TEST_FUNCTION_NAME).
        For parametrized tests, returns generalized path
         (i.e., parameters excluded).
        """
        generalized_test_names = []
        failed_test_case_names = self._db_manager.select_test_case_failed()
        for testName in failed_test_case_names:
            # generalized_test_name = _getGeneralizedTestName(testName)
            file_path, _, function_name = naming_lib.convert_test_name_to_components(
                testName
            )
            generalized_test_name = naming_lib.get_generalized_test_name(
                file_path, function_name
            )
            generalized_test_names.append(generalized_test_name)
        return generalized_test_names

    def _run_switched_predicate_instance(
        self,
        project_path: str,
        test_name: str,
        predicate_name: str,
        instance_number: int,
        src: str,
        exclude: List[str],
        timeout_limit: float,
    ) -> Tuple[Optional[str], Optional[List[str]], Optional[float], bool]:
        """
        Runs the instrumented project in temp directory on the given test name.
        In the execution, the given predicate instance is switched.
        Returns True if the given test passes, and False, if it does not.
        """

        # generalized_test_path = _getGeneralizedTestName(testName)
        file_path, _, function_name = naming_lib.convert_test_name_to_components(
            test_name
        )
        generalized_test_path = naming_lib.get_generalized_test_name(
            file_path, function_name
        )
        exe_result_data = self._collect_ps_run_api.run_ps_collect_mode_run(
            src=src,
            exclude=exclude,
            project_path=project_path,
            file_or_dir=[generalized_test_path],
            predicate_name=predicate_name,
            instance_number=instance_number,
            timeout=timeout_limit,
        )

        exec_stat_error = exe_result_data.is_test_case_table_empty_or_none()
        if exec_stat_error:
            print("Bad execution")
            return None, None, None, exec_stat_error

        test_result, timeout_stat = exe_result_data.get_test_result(test_name)
        if test_result is None and timeout_stat is None:
            # The parametrized tests might be executed with different parameters in the
            # main mode and the collect mode. In this situation, the test name from
            # main cannot be found in the tests executed in collect mode. Found by pandas 141.
            print("Non-deterministic execution")
            return None, None, None, False

        seen_exception_list_str = exe_result_data.get_test_seen_exception_list(
            test_name
        )
        seen_exception_list = self.csv_row_to_list(seen_exception_list_str)

        return test_result, seen_exception_list, timeout_stat, exec_stat_error

    @staticmethod
    def csv_row_to_list(csv_row: str) -> List[str]:
        csv_comps = csv_row.split(",")
        return csv_comps

    def _run_predicate_sequence(
        self,
        project_path: str,
        test_name: str,
        indexed_pred_seq_str: str,
        src: str,
        exclude: List[str],
        expected_exception_seen_name: str,
        timeout_limit: float,
    ):
        """
        Runs the given ordered predicate instances for the given predicate test name.
        Returns an ordered sequence of predicate instances that can pass the given test if switched.
        """

        ind_pred_seq = self.csv_row_to_list(indexed_pred_seq_str)
        ind_pred_seq.reverse()  # Predicate instances are executed from last to first

        number_of_predicate_instances_for_test = len(ind_pred_seq)

        passing_predicate_instances = []
        for ind, predInst in enumerate(ind_pred_seq):
            pred_name, inst_num = predInst.split("::")

            print(
                f"-----RUNNING Predicate Instance "
                f"{pred_name}::{inst_num} - {ind} / {number_of_predicate_instances_for_test} "
                f"----- on test {test_name}-----"
            )

            (
                test_result,
                seen_exception_list,
                timeout_stat,
                exec_stat_error,
            ) = self._run_switched_predicate_instance(
                project_path=project_path,
                test_name=test_name,
                predicate_name=pred_name,
                instance_number=int(inst_num),
                src=src,
                exclude=exclude,
                timeout_limit=timeout_limit,
            )

            if exec_stat_error:
                self._db_manager.insert_bad_execution_predicate_instance(
                    test_name, pred_name, inst_num
                )
                print("Execution error for: ", test_name, pred_name, inst_num)
                continue

            # Not needed. Just to collect info for further analysis.
            if timeout_stat == 1:
                self._db_manager.insert_timeout_predicate_instance(
                    test_name, pred_name, inst_num
                )
                print("Timeout for: ", test_name, pred_name, inst_num)
                continue

            if test_result == "passed":
                # For crashing bugs, if switching prevents the program from crashing
                # but the crash location is not executed, the predicate is not critical.
                if (expected_exception_seen_name is None) or (
                    expected_exception_seen_name in seen_exception_list
                ):
                    passing_predicate_instances.append(predInst)

        return passing_predicate_instances

    def _get_test_scored_entity_store_db(
        self,
        test_name: str,
        passing_predicate_instance_sequence: List[str],
        granularity: str,
    ):
        score = 1
        for predicateInstance in passing_predicate_instance_sequence:
            predicate_name, instance_number = predicateInstance.split("::")
            file_path, line_start, line_end = (
                self._db_manager.select_candidate_predicate(predicate_name)
            )

            if granularity == "statement":
                entity = f"{file_path}::{line_start}::{line_end}"
            elif granularity == "function":
                cfi = self._function_level_granularity_manager.get_covered_function(
                    file_path, line_start
                )
                if cfi is None:
                    entity = f"{file_path}::GLOBAL"
                else:
                    (
                        function_file_path,
                        function_name,
                        function_line_start,
                        function_line_end,
                    ) = cfi
                    entity = naming_lib.get_covered_function_name(
                        function_file_path,
                        function_name,
                        function_line_start,
                        function_line_end,
                    )
            else:
                raise Exception(f"The granularity {granularity} is not supported.")

            # For function granularity it can happen.
            # In this case, only one should be stored.
            # Found in youtube_dl13
            if self._db_manager.scored_entity_exists_for_test(test_name, entity):
                continue

            self._db_manager.insert_scored_entity(test_name, entity, score)

            # Critical predicate closer to the failure location is more suspicious to be buggy.
            # Predicate instance closer to the failure locations is more suspicious to be buggy.
            score = score / 1.1

    def _get_all_tests_top_n_scored_entities(self, top_n):
        all_tests_top_n_scored_entities = {}

        final_failing_test_names = self._db_manager.select_scored_entity_test_names()

        for testName in final_failing_test_names:
            test_name_as_file_path = naming_lib.test_name_to_file_name(testName)

            if top_n == -1:
                test_top_n_scored_entities = (
                    self._db_manager.select_test_all_scored_entities(testName)
                )
            elif top_n >= 0:
                test_top_n_scored_entities = (
                    self._db_manager.select_test_top_n_scored_entities(testName, top_n)
                )
            else:
                raise Exception(f"TopN {top_n} is not supported.")

            all_tests_top_n_scored_entities[test_name_as_file_path] = (
                test_top_n_scored_entities
            )

        if len(all_tests_top_n_scored_entities) == 0:
            all_tests_top_n_scored_entities = {"fauxpy_no_swapped_instances": []}

        return all_tests_top_n_scored_entities

    def run_predicate_switching(
        self,
        src: str,
        exclude: List[str],
        granularity: str,
        timeout_limit: float,
        top_n: int,
        target_failing_tests: TargetFailingTests,
    ):
        """
        Runs the whole predicate switching algorithm.
        """

        self._predicate_instance_manager.get_candidate_predicates_store_db()

        if self._db_manager.number_of_candidate_predicates() == 0:
            return {"fauxpy_no_candidate_predicates": []}

        self._seen_exception_manager.get_seen_exceptions_store_db()
        temp_project_path = self._instrument_project()

        if target_failing_tests is None:
            failing_tests = self._get_generalized_failed_test_function_paths()
        else:
            failing_tests = target_failing_tests.get_failing_tests()

        predicate_sequences = self._get_predicate_sequences(
            temp_project_path, src, exclude, failing_tests
        )

        for pred_seq_item in predicate_sequences:
            test_name, indexed_pred_seq_str = pred_seq_item
            original_test_type = self._db_manager.select_test_type(test_name)
            if original_test_type == "passed":
                continue

            seen_exception_name = self._db_manager.select_seen_exception_for_test_name(
                test_name
            )
            passing_predicate_instance_sequence = self._run_predicate_sequence(
                temp_project_path,
                test_name,
                indexed_pred_seq_str,
                src,
                exclude,
                seen_exception_name,
                timeout_limit,
            )

            self._get_test_scored_entity_store_db(
                test_name, passing_predicate_instance_sequence, granularity
            )

        self._remove_temp_project(temp_project_path)

        all_tests_scored_entities = self._get_all_tests_top_n_scored_entities(top_n)

        return all_tests_scored_entities
