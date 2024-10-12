from typing import List

from fauxpy.fault_localization.mbfl.cosmicray_mutant_generator.mutant_generator import (
    MutantGenerator,
)
from fauxpy.fault_localization.mbfl.db_manager import MbflDbManager
from fauxpy.session_lib import naming_lib


class MutationManager:
    def __init__(self, db_manager: MbflDbManager):
        self._db_manager = db_manager
        self._mutant_generator = MutantGenerator()

    @staticmethod
    def _set_mutant_ids(mutant_list):
        for i in range(len(mutant_list)):
            mutant_list[i].set_id(f"M{i}")

    def get_all_mutants_for_failing_line_number_list(
        self, failing_line_number_list
    ) -> List:
        mutant_list = []

        for statement_name in failing_line_number_list:
            path, line_number = naming_lib.convert_statement_name_to_components(
                statement_name
            )
            self._db_manager.insert_failing_line_number_components(path, line_number)

        failing_module_path_list = (
            self._db_manager.select_distinct_failing_module_paths()
        )
        for module_path in failing_module_path_list:
            line_numbers = self._db_manager.select_failing_line_numbers_for_module_path(
                module_path
            )
            current_module_mutant_list = (
                self._mutant_generator.get_mutants_for_module_and_lines(
                    module_path=module_path,
                    line_numbers=line_numbers,
                    operator_mutation_target_unique=True,
                )
            )
            mutant_list += current_module_mutant_list

        self._set_mutant_ids(mutant_list)

        return mutant_list
