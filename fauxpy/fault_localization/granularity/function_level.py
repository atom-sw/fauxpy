import ast
from typing import Tuple, Optional, List

from fauxpy import common
from fauxpy.fault_localization.granularity.ast_lib import FunctionVisitor
from fauxpy.fault_localization.granularity.db_manager import FunctionLevelDbManager


class FunctionLevelGranularity:
    def __init__(self, db_manager: FunctionLevelDbManager):
        self._db_manager = db_manager

    @staticmethod
    def _find_all_function_ranges(file_path: str) -> List[Tuple[str, int, int]]:
        with open(file_path, "r") as source:
            try:
                tree = ast.parse(source.read())
            except Exception as exp:
                common.Logger.warning(
                    f"Due to the following error, the following module is removed form fault localization."
                    f"To include it, fix the error, and run the tool again.\r\n"
                    f"Error: {exp}.\r\n"
                    f"Module: {file_path}"
                )
                return []

        analyzer = FunctionVisitor()
        analyzer.visit(tree)

        return analyzer.function_range_list

    def get_covered_function(
        self, file_path: str, line_number: int
    ) -> Optional[Tuple[str, str, int, int]]:
        function_range_list = self._db_manager.select_function_ranges(
            file_path, line_number
        )

        if len(function_range_list) == 0:
            if self._db_manager.is_file_path_covered(file_path):
                return None
            else:
                function_range_list = self._find_all_function_ranges(file_path)
                for functionRange in function_range_list:
                    self._db_manager.insert_function_information(
                        file_path, functionRange[0], functionRange[1], functionRange[2]
                    )

                if len(function_range_list) == 0:
                    return None
                else:
                    function_range_list = self._db_manager.select_function_ranges(
                        file_path, line_number
                    )
                    if len(function_range_list) == 0:
                        return None

                    function_range_list.sort(key=lambda x: x[2] - x[1])
                    return (
                        file_path,
                        function_range_list[0][0],
                        function_range_list[0][1],
                        function_range_list[0][2],
                    )
        else:
            function_range_list.sort(key=lambda x: x[2] - x[1])
            return (
                file_path,
                function_range_list[0][0],
                function_range_list[0][1],
                function_range_list[0][2],
            )
