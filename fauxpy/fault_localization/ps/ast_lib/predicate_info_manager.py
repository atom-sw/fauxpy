import ast
from typing import Tuple

from fauxpy import common
from fauxpy.fault_localization.ps.ast_lib.analyzer import Analyzer


class PredicateInfoManager:
    @staticmethod
    def get_predicate_instance_range_for_program_line(
        file_path: str, line_number: int
    ) -> Tuple[int, int]:
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
                return -1, -1

        analyzer = Analyzer(line_number)
        analyzer.visit(tree)
        line_start = analyzer.get_line_start()
        line_end = analyzer.get_line_end()

        return line_start, line_end
