import pathlib
import shutil
import tempfile
import time


class TempManager:
    def __init__(self, project_working_directory: pathlib.Path):
        self._project_working_directory = project_working_directory

    @staticmethod
    def _get_unique_temporary_directory_path() -> str:
        tmp = tempfile.gettempdir()
        current_time_int = time.time()
        tmp_dir = pathlib.Path(tmp) / str(current_time_int)
        tmp_dir = str(tmp_dir.resolve())
        return tmp_dir

    @staticmethod
    def _copy_dir(source: str, destination: str):
        shutil.copytree(source, destination, symlinks=True)

    def make_project_copy_in_temp(self) -> str:
        temp_dir = self._get_unique_temporary_directory_path()
        project_dir = str(self._project_working_directory.absolute().resolve())
        self._copy_dir(project_dir, temp_dir)

        return temp_dir
