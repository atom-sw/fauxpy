import os


class FauxpyPath:
    """Represents a file or directory path relative to a project working directory."""

    def __init__(self):
        """Private constructor to prevent direct instantiation.

        Raises:
            NotImplementedError: Always raised to enforce the use of factory methods.
        """
        self._project_working_directory: str = ""
        self._relative_path: str = ""
        self._absolute_path: str = ""
        raise NotImplementedError("Use from_absolute_path or from_relative_path to instantiate this class.")

    @staticmethod
    def __create(
            project_working_directory: str,
            relative_path: str
    ) -> "FauxpyPath":
        """Creates an instance of the object.

        Args:
            project_working_directory (str): The root directory of the project.
            relative_path (str): The relative path within the project.

        Returns:
            FauxpyPath: A new instance of FauxpyPath.
        """
        obj = object.__new__(FauxpyPath)
        obj._project_working_directory = os.path.normpath(project_working_directory)
        obj._relative_path = os.path.normpath(relative_path)
        obj._absolute_path = os.path.normpath(
            os.path.join(obj._project_working_directory, obj._relative_path)
        )
        return obj

    def __str__(self) -> str:
        """
        Returns the absolute path as a string.

        Returns:
            str: The absolute path.
        """
        return self._absolute_path

    @staticmethod
    def from_absolute_path(
            project_working_directory: str,
            absolute_path: str
    ) -> "FauxpyPath":
        """
        Creates an object instance from an absolute path.

        Args:
            project_working_directory (str): The root directory of the project.
            absolute_path (str): The absolute path.

        Returns:
            FauxpyPath: An instance representing the given path.
        """
        relative_path = os.path.relpath(absolute_path, project_working_directory)
        return FauxpyPath.__create(project_working_directory, relative_path)

    @staticmethod
    def from_relative_path(
            project_working_directory: str,
            relative_path: str
    ) -> "FauxpyPath":
        """
        Creates an object instance from a relative path.

        Args:
            project_working_directory (str): The root directory of the project.
            relative_path (str): The relative path.

        Returns:
            FauxpyPath: An instance representing the given path.
        """
        return FauxpyPath.__create(project_working_directory, relative_path)

    def get_relative(self) -> str:
        """
        Retrieves the relative path.

        Returns:
            str: The relative path from the project root.
        """
        return self._relative_path

    def get_absolute(self) -> str:
        """
        Retrieves the absolute path.

        Returns:
            str: The absolute path.
        """
        return self._absolute_path

    def exists(self) -> bool:
        """
        Checks if the path exists in the file system.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return os.path.exists(self._absolute_path)
