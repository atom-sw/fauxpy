from typing import List, Tuple

from fauxpy.fault_localization.ps.ast_lib.predicate_info_manager import (
    PredicateInfoManager,
)
from fauxpy.fault_localization.ps.db_manager import PsDbManager


class PredicateInstanceManager:
    def __init__(self, sb_manager: PsDbManager):
        self._db_manager = sb_manager
        self._predicate_info_manager = PredicateInfoManager()

    def _get_shadowed_covered_predicates_for_covered_lines_store_db(
        self, executed_line_list: List[Tuple[str, int]]
    ):
        for test_name, file_path, line_number, test_type in executed_line_list:
            assert test_type == "failed"
            line_start, line_end = (
                self._predicate_info_manager.get_predicate_instance_range_for_program_line(
                    file_path, line_number
                )
            )
            if not line_start == line_end == -1:
                self._db_manager.insert_shadowed_covered_predicate(
                    test_name, file_path, line_number, line_start, line_end
                )

    def _name_executed_predicates_store_db(self, executed_predicates):
        for i, exe_pred in enumerate(executed_predicates):
            file_path, line_start, line_end = exe_pred
            predicate_name = f"Pred_{i}"

            self._db_manager.insert_candidate_predicate(
                file_path=file_path,
                line_start=line_start,
                line_end=line_end,
                predicate_name=predicate_name,
            )

    def get_candidate_predicates_store_db(self):
        covered_lines = (
            self._db_manager.select_covered_lines_with_test_types_for_all_failed_tests()
        )
        self._get_shadowed_covered_predicates_for_covered_lines_store_db(covered_lines)
        distinct_executed_predicates = (
            self._db_manager.select_distinct_executed_source_code_predicates()
        )
        self._name_executed_predicates_store_db(distinct_executed_predicates)
