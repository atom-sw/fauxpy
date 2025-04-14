import os
import pathlib
from typing import List

from fauxpy.session_lib.fauxpy_path import FauxpyPath


class PathUtil:
    """
    Utility class for determining whether file paths should be included in fault localization
    and for converting between absolute and relative paths.

    The primary responsibility of this class is to evaluate whether a given path is relevant
    for fault localization based on a target source and an exclusion list.

    It also provides helper methods to convert between relative and absolute paths based on
    the project's working directory.
    """

    def __init__(
            self,
            project_working_directory: pathlib.Path
    ):
        """
        Initializes the PathUtil with the project's working directory.

        Args:
            project_working_directory (pathlib.Path): The base working directory of the project.
        """
        self._project_working_directory = project_working_directory

    @staticmethod
    def _not_starts_with(exclude_list: List[FauxpyPath], path: str) -> bool:
        """
        Checks whether a given path does not start with any of the excluded paths.

        Args:
            exclude_list (List[FauxpyPath]): List of FauxpyPaths to exclude.
            path (str): Absolute path to check.

        Returns:
            bool: True if the path does not start with any excluded path, False otherwise.
        """
        for exclude_item in exclude_list:
            absolute_path_exclude = exclude_item.get_absolute()
            if path.startswith(absolute_path_exclude):
                return False
        return True

    def path_should_be_localized(
            self,
            target_src: FauxpyPath,
            exclude_list: List[FauxpyPath],
            abs_path: str
    ) -> bool:
        """
        Determines whether a given absolute path should be considered for fault localization.

        The path must be within the target source directory and must not be part of any excluded path.

        Args:
            target_src (FauxpyPath): The source directory that should be included.
            exclude_list (List[FauxpyPath]): List of FauxpyPaths to exclude from consideration.
            abs_path (str): Absolute path to evaluate.

        Returns:
            bool: True if the path should be localized, False otherwise.
        """
        abs_src = target_src.get_absolute()
        if abs_path.startswith(abs_src) and self._not_starts_with(exclude_list, abs_path):
            return True
        else:
            return False

    def relative_path_to_abs_path(self, rel_path: str) -> str:
        """
        Converts a relative path (from the project root) to an absolute path.

        Args:
            rel_path (str): The relative path to convert.

        Returns:
            str: The resolved absolute path.
        """
        abs_src = self._project_working_directory / rel_path
        return str(abs_src.resolve())

    def absolute_path_to_relative_path(self, abs_path: str) -> str:
        """
        Converts an absolute path to a relative path from the project root.

        Args:
            abs_path (str): The absolute path to convert.

        Returns:
            str: The relative path from the project working directory.
        """
        project_working_directory_str = str(
            self._project_working_directory.absolute().resolve()
        )
        rel_path = os.path.relpath(abs_path, project_working_directory_str)
        return rel_path
