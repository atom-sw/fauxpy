import glob
import os
import pathlib
from typing import List, Optional

from fauxpy import constants
from fauxpy.fault_localization.collect_ps_run.api_file import CollectPsRunApiFileManager
from fauxpy.fault_localization.collect_ps_run.result_type import CollectPsRunResult
from fauxpy.fault_localization.util.run_lib import CommandRunner


class CollectPsRunApi:
    def __init__(self):
        self._api_file_manager = CollectPsRunApiFileManager()
        self._command_runner = CommandRunner()

    @staticmethod
    def _clean_project(temp_dir):
        """
        Removes all .pyc files in the project directory.
        This is necessary because after modifying the source code (e.g., through mutation),
        the .pyc files do not automatically update to reflect the changes.
        It also removed the file made by the instrumentation library (just in case,
        since it should not exist at the first run, and the mode generating this
        file is only executed ones during the predicate switching method).
        """

        # https://thispointer.com/python-how-to-remove-files-by-matching-pattern-wildcards-certain-extensions-only/
        pattern = f"{temp_dir}/**/*.pyc"
        file_list = glob.glob(pattern, recursive=True)
        for filePath in file_list:
            if os.path.exists(filePath):
                os.remove(filePath)

        file_name_pred_sequence = pathlib.Path(
            constants.getCollectModeExecutedPredicateSequenceFileName()
        )
        if file_name_pred_sequence.exists():
            file_name_pred_sequence.unlink()

        file_name_evaluation_counter = pathlib.Path(
            constants.getCollectModeEvaluationCounterFileName()
        )
        if file_name_evaluation_counter.exists():
            file_name_evaluation_counter.unlink()

        file_name_exception_seen = pathlib.Path(constants.getExceptionSeenFileName())
        if file_name_exception_seen.exists():
            file_name_exception_seen.unlink()

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
                "collectpsrun",
                "--exclude",
                self.convert_list_to_string(exclude),
            ]
        )
        if timeout is not None:
            command += ["--timeout", str(timeout)]
            command += ["--timeout_method", "thread"]
        self._command_runner.run_command(command, project_path, process_timeout)

    def run_ps_collect_mode_run(
        self,
        src: str,
        exclude: List[str],
        project_path: str,
        file_or_dir: List[str],
        predicate_name: str,
        instance_number: int,
        timeout: Optional[float] = None,
    ) -> CollectPsRunResult:
        self._api_file_manager.save_config_file(
            project_path, predicate_name, instance_number
        )
        self._run_project(src, exclude, project_path, file_or_dir, timeout)

        test_case_table = self._api_file_manager.load_test_case_table(project_path)
        seen_exception_list = self._api_file_manager.load_seen_exception_sequence_table(
            project_path
        )
        result = CollectPsRunResult(test_case_table, seen_exception_list)

        return result
