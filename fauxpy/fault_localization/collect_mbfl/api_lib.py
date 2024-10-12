import glob
import os
from typing import List, Tuple, Optional

from fauxpy.fault_localization.collect_mbfl.api_file import CollectMbflApiFileManager
from fauxpy.fault_localization.util.run_lib import CommandRunner


class CollectMbflApi:
    def __init__(self):
        self._api_file_manager = CollectMbflApiFileManager()
        self._command_runner = CommandRunner()

    @staticmethod
    def _clean_project(temp_dir):
        """
        Removes all .pyc files in the project directory.
        This is necessary because after modifying the source code (e.g., through mutation),
        the .pyc files do not automatically update to reflect the changes.
        """

        # https://thispointer.com/python-how-to-remove-files-by-matching-pattern-wildcards-certain-extensions-only/
        pattern = f"{temp_dir}/**/*.pyc"
        file_list = glob.glob(pattern, recursive=True)
        for file_path in file_list:
            if os.path.exists(file_path):
                os.remove(file_path)

    @staticmethod
    def convert_list_to_string(list_obj: List[str]) -> str:
        list_content_as_str = ",".join(list_obj)
        list_string = "[" + list_content_as_str + "]"
        return list_string

    def _run_project(
        self,
        src: str,
        exclude: List[str],
        project_path: str,
        file_or_dir: List[str],
        timeout: Optional[float],
        process_timeout: float = None,
    ):
        self._clean_project(project_path)
        command = (
            ["python", "-m", "pytest"]
            + file_or_dir
            + [
                "--src",
                src,
                "--family",
                "collectmbfl",
                "--exclude",
                self.convert_list_to_string(exclude),
            ]
        )
        if timeout is not None:
            command += ["--timeout", str(timeout)]
            command += ["--timeout_method", "thread"]
        self._command_runner.run_command(command, project_path, process_timeout)

    def run_mbfl_collect_mode(
        self,
        src: str,
        exclude: List[str],
        project_path: str,
        file_or_dir: List[str],
        timeout: float,
        process_timeout: float,
    ) -> Optional[List[Tuple[str, str, str]]]:
        self._run_project(
            src, exclude, project_path, file_or_dir, timeout, process_timeout
        )
        test_case_table = self._api_file_manager.load_test_case_table(project_path)
        return test_case_table
