from pathlib import Path
from typing import List

from fauxpy.fault_localization.granularity.function_level import (
    FunctionLevelGranularity,
)
from fauxpy.fault_localization.util.path_util import PathUtil
from fauxpy.session_lib import naming_lib


class TracebackParser:
    def __init__(
        self,
        function_level_granularity_manager: FunctionLevelGranularity,
        project_working_directory: Path,
    ):
        self._function_level_granularity_manager = function_level_granularity_manager
        self._path_util = PathUtil(project_working_directory)

    @staticmethod
    def _is_python_module(path: str):
        return path.endswith(".py")

    # TODO: Move to traceback_utils.py
    def get_ordered_traceback_function_name_list(
        self, src, exclude, repr_traceback
    ) -> List[str]:
        traceback_name_list = []

        for repr_ent in repr_traceback.reprentries:
            path = repr_ent.reprfileloc.path
            line_number = repr_ent.reprfileloc.lineno
            absolute_path = self._path_util.relative_path_to_abs_path(path)

            if not self._is_python_module(path):
                continue

            if self._path_util.path_should_be_localized(src, exclude, absolute_path):
                covered_function = (
                    self._function_level_granularity_manager.get_covered_function(
                        absolute_path, line_number
                    )
                )

                # Bug fix - found by cnn_text_classification_tf_b1
                if covered_function is None:
                    continue

                covered_function_name = naming_lib.get_covered_function_name(
                    covered_function[0],
                    covered_function[1],
                    covered_function[2],
                    covered_function[3],
                )
                traceback_name_list.append(covered_function_name)
        traceback_name_list.reverse()

        return traceback_name_list
