import glob
import os
import pathlib
from typing import List, Tuple, Optional

from fauxpy import constants
from fauxpy.fault_localization.collect_ps_info.api_file import (
    CollectPsInfoApiFileManager,
)
from fauxpy.fault_localization.util.run_lib import CommandRunner


class CollectPsInfoApi:
    def __init__(self):
        self._api_file_manager = CollectPsInfoApiFileManager()
        self._command_runner = CommandRunner()

    @staticmethod
    def list_to_csv_row(list_item: List[str]) -> str:
        csv_row = ",".join(list_item)
        return csv_row

    @staticmethod
    def csv_row_to_list(csv_row: str) -> List[str]:
        csv_comps = csv_row.split(",")
        return csv_comps

    def index_predicate_sequence(self, predicate_sequence) -> str:
        pred_count_set = dict()
        pred_seq_list = self.csv_row_to_list(predicate_sequence)
        indexed_pred_seq = []
        for pred in pred_seq_list:
            if pred in pred_count_set.keys():
                pred_count_set[pred] += 1
            else:
                pred_count_set[pred] = 0
            indexed_pred_seq.append(f"{pred}::{pred_count_set[pred]}")

        indexed_pred_seq_str = self.list_to_csv_row(indexed_pred_seq)

        return indexed_pred_seq_str

    def get_index_predicate_sequences(
        self, predicate_sequence_table
    ) -> List[Tuple[str, str, str]]:
        indexed_pred_sequences = []
        for tableRow in predicate_sequence_table:
            test_name, predicate_sequence = tableRow
            ind_pred_seq = self.index_predicate_sequence(predicate_sequence)
            indexed_pred_sequences.append((test_name, predicate_sequence, ind_pred_seq))
        return indexed_pred_sequences

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
                "collectpsinfo",
                "--exclude",
                self.convert_list_to_string(exclude),
            ]
        )
        if timeout is not None:
            command += ["--timeout", str(timeout)]
            command += ["--timeout_method", "thread"]
        self._command_runner.run_command(command, project_path, process_timeout)

    def run_ps_collect_mode_info(
        self,
        src: str,
        exclude: List[str],
        project_path: str,
        file_or_dir: List[str],
        timeout: Optional[float] = None,
    ) -> List[Tuple[str, str, str]]:
        self._run_project(src, exclude, project_path, file_or_dir, timeout)

        predicate_sequence_table = self._api_file_manager.load_predicate_sequence_table(
            project_path
        )
        indexed_predicate_sequences = self.get_index_predicate_sequences(
            predicate_sequence_table
        )

        return indexed_predicate_sequences
