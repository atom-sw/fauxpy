import shutil
from enum import Enum
from pathlib import Path
from typing import Tuple, List

from fauxpy.fault_localization.collect_mbfl.api_lib import CollectMbflApi
from fauxpy.fault_localization.granularity.db_manager import FunctionLevelDbManager
from fauxpy.fault_localization.granularity.function_level import (
    FunctionLevelGranularity,
)
from fauxpy.fault_localization.mbfl.cosmicray_mutant_generator.mutant import Mutant
from fauxpy.fault_localization.mbfl.db_manager import MbflDbManager
from fauxpy.fault_localization.util.path_util import PathUtil
from fauxpy.fault_localization.util.temp_lib import TempManager
from fauxpy.session_lib import naming_lib


class TestComparisonState(Enum):
    Normal = 0
    BadTest = 1
    BadMutant = 2
    NotTarget = 3


class RunManager:
    def __init__(
        self,
        db_manager: MbflDbManager,
        function_level_db_manager: FunctionLevelDbManager,
        project_working_directory: Path,
    ):
        self._db_manager = db_manager
        self._collect_mbfl_api = CollectMbflApi()
        self._function_level_granularity_manager = FunctionLevelGranularity(
            function_level_db_manager
        )
        self._temp_manager = TempManager(project_working_directory)
        self._path_util = PathUtil(project_working_directory)

    @staticmethod
    def _backup_file(file_path: Path):
        new_path = f"{str(file_path.resolve())}.bak"
        file_path.rename(new_path)

    @staticmethod
    def _un_backup_file(file_path: Path):
        assert file_path.exists()
        backup_path_str = f"{str(file_path.resolve())}.bak"
        backup_path = Path(backup_path_str)
        assert backup_path.exists()
        file_path.unlink()
        assert not file_path.exists()
        file_path_str = str(file_path.resolve())
        backup_path.rename(file_path_str)
        assert file_path.exists()
        assert not backup_path.exists()

    @staticmethod
    def _insert_mutation_module(module_path: str, module_content: str):
        with open(module_path, "w") as file:
            file.write(module_content)

    def _mutate_temp_project(
        self,
        temp_project_path: str,
        mutating_module_path: str,
        mutating_module_content: str,
    ):
        relative_path_of_mutating_module = (
            self._path_util.absolute_path_to_relative_path(mutating_module_path)
        )
        absolute_temp_path_of_mutating_module = (
            Path(temp_project_path) / relative_path_of_mutating_module
        )
        self._backup_file(absolute_temp_path_of_mutating_module)
        self._insert_mutation_module(
            str(absolute_temp_path_of_mutating_module.resolve()),
            mutating_module_content,
        )

    def _un_mutate_temp_project(
        self, temp_project_path: str, mutating_module_path: str
    ):
        relative_path_of_mutating_module = (
            self._path_util.absolute_path_to_relative_path(mutating_module_path)
        )
        absolute_temp_path_of_mutating_module = (
            Path(temp_project_path) / relative_path_of_mutating_module
        )
        self._un_backup_file(absolute_temp_path_of_mutating_module)

    # TODO: probably, the timeout computation is not need. If timeout happens,
    #  the test cases jason file does not get generated, which is
    #  something that needs to be checked to see if timeout happened or not.
    @staticmethod
    def _compare_two_test_case_results(
        normal_test_case, mutant_test_case
    ) -> Tuple[int, int, int, TestComparisonState]:
        failed_to_passed = 0
        passed_to_failed = 0
        failed_changed = 0

        mutant_test_case_timeout_stat = mutant_test_case[3]

        normal_test_type = normal_test_case[1]
        normal_test_timeout_stat = normal_test_case[3]
        normal_test_target_stat = normal_test_case[4]
        normal_test_included = (normal_test_type == "passed") or (
            normal_test_type == "failed" and normal_test_target_stat == 1
        )

        # ToDo: use the condition inside the if. Not as a boolean variable.
        if not normal_test_included:
            # The failing test is not a target failing test. Discard the current test.
            test_comparison_state = TestComparisonState.NotTarget
        else:
            if normal_test_timeout_stat == -1 and mutant_test_case_timeout_stat == -1:
                # It's OK! Compute the terms.
                test_comparison_state = TestComparisonState.Normal
            elif normal_test_timeout_stat == -1 and mutant_test_case_timeout_stat == 1:
                # Infinite loop. Do not compute the terms. Discard current mutant.
                test_comparison_state = TestComparisonState.BadMutant
            elif normal_test_timeout_stat == 1 and mutant_test_case_timeout_stat == -1:
                # Weired case. Do not compute the terms. Discard current test.
                test_comparison_state = TestComparisonState.BadTest
            elif normal_test_timeout_stat == 1 and mutant_test_case_timeout_stat == 1:
                # Bad initial test. Do not compute the terms. Discard current test.
                test_comparison_state = TestComparisonState.BadTest
            else:
                raise Exception("This one must never happen.")

        if test_comparison_state == TestComparisonState.Normal:
            if normal_test_case[1] == "passed" and mutant_test_case[1] == "failed":
                passed_to_failed = 1
            elif normal_test_case[1] == "failed" and mutant_test_case[1] == "passed":
                failed_to_passed = 1
            elif normal_test_case[1] == "failed" and mutant_test_case[1] == "failed":
                if normal_test_case[2] != mutant_test_case[2]:
                    failed_changed = 1

        return failed_to_passed, passed_to_failed, failed_changed, test_comparison_state

    @staticmethod
    def _remove_temp_project(temp_project_path):
        shutil.rmtree(temp_project_path)

    def _get_mutant_score_terms(self, mutant_test_case_run_result_table):
        """
        Bad tests are removed from computation.
        In case of timeout_happened = True, the terms failed_to_passed, passed_to_failed, failed_changed are not valid.
        """
        failed_to_passed = 0
        passed_to_failed = 0
        failed_changed = 0
        timeout_happened = False

        for mutantTestCaseResult in mutant_test_case_run_result_table:
            normal_test_case_result = self._db_manager.select_test_case(
                mutantTestCaseResult[0]
            )

            if normal_test_case_result is None:
                # In pandas 47, one of the parametrized tests can have names
                # generated randomly (a very rare case). Thus, the collect mode
                # can return test names that do not exist in the main execution of the
                # MBFL method. In these cases, let's just ignore that test
                # and continue the score terms computation using the remaining tests.
                continue

            f2p, p2f, fc, test_comp_state = self._compare_two_test_case_results(
                normal_test_case_result, mutantTestCaseResult
            )
            if test_comp_state == TestComparisonState.Normal:
                failed_to_passed += f2p
                passed_to_failed += p2f
                failed_changed += fc
            elif (
                test_comp_state == TestComparisonState.BadTest
                or TestComparisonState.NotTarget
            ):
                continue
            elif test_comp_state == TestComparisonState.BadMutant:
                timeout_happened = True
                break

        return failed_to_passed, passed_to_failed, failed_changed, timeout_happened

    def run_all_mutants_store_db(
        self,
        mutants: List[Mutant],
        file_or_dir: List[str],
        granularity: str,
        src: str,
        exclude: List[str],
        timeout_limit: float,
        number_all_tests,
        process_timeout,
    ):
        temp_project_path = self._temp_manager.make_project_copy_in_temp()

        number_of_all_mutants = len(mutants)

        print(f"-------------- Running {number_of_all_mutants} Mutants --------------")
        for mutant in mutants:
            print(
                f"------------ Running Mutant ID ----->>>>> {mutant.get_id()} / {number_of_all_mutants} ------------"
            )

            self._mutate_temp_project(
                temp_project_path, mutant.get_module_path(), mutant.get_module_content()
            )
            mutant_test_case_run_result_table = (
                self._collect_mbfl_api.run_mbfl_collect_mode(
                    src,
                    exclude,
                    temp_project_path,
                    file_or_dir,
                    timeout=timeout_limit,
                    process_timeout=process_timeout,
                )
            )

            if (
                mutant_test_case_run_result_table is None
                or len(mutant_test_case_run_result_table) == 0
            ):
                # Timeout happened
                print("Timeout or bad mutant")
                self._db_manager.update_mutant_as_timeout(mutant.get_id())
                self._un_mutate_temp_project(
                    temp_project_path, mutant.get_module_path()
                )
                continue

            # For some reason, some mutant executions might return fewer
            # number of test cases. For now I remove them.
            # TODO: Find the reason. Found in sonic3. Takes around three hours.
            if number_all_tests != len(mutant_test_case_run_result_table):
                print("Missing tests mutant")
                self._db_manager.update_mutant_as_having_missing_tests(mutant.get_id())
                self._un_mutate_temp_project(
                    temp_project_path, mutant.get_module_path()
                )
                continue

            (
                failed_to_passed,
                passed_to_failed,
                failed_changed,
                timeout_happened,
            ) = self._get_mutant_score_terms(mutant_test_case_run_result_table)

            # In case of timeout, the mutant is thrown away and
            # its status is updated in the database
            # TODO: most probably this part is not needed
            if timeout_happened:
                self._db_manager.update_mutant_as_timeout(mutant.get_id())
            else:
                if granularity == "statement":
                    entity_name = naming_lib.get_statement_name(
                        mutant.get_module_path(), mutant.get_line_number()
                    )
                elif granularity == "function":
                    covered_function = (
                        self._function_level_granularity_manager.get_covered_function(
                            mutant.get_module_path(), mutant.get_line_number()
                        )
                    )
                    entity_name = naming_lib.get_covered_function_name(
                        covered_function[0],
                        covered_function[1],
                        covered_function[2],
                        covered_function[3],
                    )
                else:
                    raise Exception(f"Granularity {granularity} is not supported.")

                self._db_manager.insert_mutant_score_terms(
                    mutant.get_id(),
                    entity_name,
                    failed_to_passed,
                    passed_to_failed,
                    failed_changed,
                )

            self._un_mutate_temp_project(temp_project_path, mutant.get_module_path())
        self._remove_temp_project(temp_project_path)
