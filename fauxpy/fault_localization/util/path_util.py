import os
import pathlib
from typing import List


class PathUtil:
    def __init__(self, project_working_directory: pathlib.Path):
        self._project_working_directory = project_working_directory

    def _not_starts_with(self, exclude_list: List[str], path: str):
        for exclude_item in exclude_list:
            absolute_path_exclude = self.relative_path_to_abs_path(exclude_item)
            if path.startswith(absolute_path_exclude):
                return False
        return True

    def path_should_be_localized(self, src: str, exclude_list: List[str], path: str):
        """
        The parameter src is a relative path.
        The parameter path is an absolute path.
        """
        abs_src = self.relative_path_to_abs_path(src)
        if path.startswith(abs_src) and self._not_starts_with(exclude_list, path):
            return True
        else:
            return False

    def relative_path_to_abs_path(self, rel_path):
        abs_src = self._project_working_directory / rel_path
        return str(abs_src.resolve())

    def absolute_path_to_relative_path(self, abs_path: str) -> str:
        project_working_directory_str = str(
            self._project_working_directory.absolute().resolve()
        )
        rel_path = os.path.relpath(abs_path, project_working_directory_str)
        return rel_path
