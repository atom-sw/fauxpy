from pathlib import Path


class FauxpyPath:
    def __init__(self, project_working_directory: str, relative_path: str):
        self._project_working_directory = Path(project_working_directory)
        self._relative_path = Path(relative_path)

    def __str__(self):
        return self.get_absolute()

    @staticmethod
    def from_absolute_path(
        project_working_directory: str, absolute_path: str
    ) -> "FauxpyPath":
        relative_path = Path(absolute_path).relative_to(project_working_directory)
        return FauxpyPath(project_working_directory, str(relative_path))

    @staticmethod
    def from_relative_path(
        project_working_directory: str, relative_path: str
    ) -> "FauxpyPath":
        return FauxpyPath(project_working_directory, relative_path)

    def get_relative(self) -> str:
        return str(self._relative_path)

    def get_absolute(self) -> str:
        return str(self._project_working_directory / self._relative_path)

    def exists(self) -> bool:
        item_path = self._project_working_directory / self._relative_path
        return item_path.exists()


class PythonPath:
    def __init__(self, working_directory: Path, path_str_relative: str):
        self._working_directory = working_directory
        self._path_str_relative = path_str_relative

    def exists(self) -> bool:
        item_path = self._working_directory / self._path_str_relative
        return item_path.exists()

    def get_relative_path(self) -> str:
        return self._path_str_relative

    def _pretty_representation(self) -> str:
        return str((self._working_directory / self._path_str_relative).absolute())

    def __str__(self):
        return self._pretty_representation()

    def __repr__(self) -> str:
        return self._pretty_representation()
