from typing import List, Tuple

from fauxpy.fault_localization.granularity.function_level import (
    FunctionLevelGranularity,
)
from fauxpy.session_lib import naming_lib


class CoveredFunctionManager:
    def __init__(self, function_level_granularity_manager: FunctionLevelGranularity):
        self._function_level_granularity_manager = function_level_granularity_manager

    def get_covered_function_names(
        self, covered_statements: List[Tuple[str, int]]
    ) -> List[str]:
        covered_function_set = set()
        for cov_stmt in covered_statements:
            covered_function = (
                self._function_level_granularity_manager.get_covered_function(
                    cov_stmt[0], cov_stmt[1]
                )
            )
            if covered_function is not None:
                covered_function_name = naming_lib.get_covered_function_name(
                    covered_function[0],
                    covered_function[1],
                    covered_function[2],
                    covered_function[3],
                )
                covered_function_set.add(covered_function_name)

        return list(covered_function_set)
