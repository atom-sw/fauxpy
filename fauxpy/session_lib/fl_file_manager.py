import csv
import json
from pathlib import Path
from typing import List, Tuple

from fauxpy import constants
from fauxpy.session_lib.fauxpy_path import FauxpyPath
from fauxpy.session_lib.fl_type import FlFamily, FlGranularity, MutationStrategy
from fauxpy.session_lib.targeted_failing_tst import TargetedFailingTst


class FlFileManager:
    """Manages file operations of a fault localization session."""
    def __init__(self, report_directory_path: Path):
        """
        Initializes the file manager with a directory path for storing reports.

        Args:
            report_directory_path (Path): Path to the directory where fault localization reports will be saved.
        """
        self._report_directory_path = report_directory_path

    def save_scores_to_file(self, technique: str, scores: List[Tuple[str, int]]):
        """
        Saves fault localization scores to a CSV file.

        Args:
            technique (str): Name of the fault localization technique used.
            scores (List[Tuple[str, int]]): List of tuples containing (entity name, score).
        """
        scores_file_path = self._report_directory_path / f"Scores_{technique}.csv"
        with open(scores_file_path, "w") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(constants.SCORES_CSV_HEADER)
            for score in scores:
                writer.writerow([score[0], score[1]])

    def save_config_to_file(
        self,
        target_src: FauxpyPath,
        exclude_list: List[FauxpyPath],
        fl_family: FlFamily,
        fl_granularity: FlGranularity,
        top_n: int,
        targeted_failing_test_list: List[TargetedFailingTst],
        mutation_strategy: MutationStrategy,
    ):
        """
        Saves the session configuration to a JSON file.

    Args:
        target_src (FauxpyPath): Source code directory to perform fault localization on.
        exclude_list (List[FauxpyPath]): List of files or directories to exclude from fault localization.
        fl_family (FlFamily): Family of the fault localization technique.
        fl_granularity (FlGranularity): Fault localization granularity level.
        top_n (int): Number of top-ranked elements to show in the output.
        targeted_failing_test_list (List[TargetedFailingTst]): List of failing test cases that are the target
            of the current fault localization session.
        mutation_strategy (MutationStrategy): Strategy used for mutation analysis
            (only used by the MBFL family).
        """
        file_path = self._report_directory_path / constants.CONFIG_FILE_NAME_FL_SESSION

        config_dict = {
            "Src": target_src.get_relative(),
            "Exclude": [x.get_relative() for x in exclude_list],
            "Family":  fl_family.name,
            "Granularity": fl_granularity.name,
            "TopN": top_n,
            "TargetedFailingTests": [x.get_relative_test_name() for x in targeted_failing_test_list],
            "MutationStrategy": mutation_strategy.name
        }

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(config_dict, file, indent=4)  # Pretty-print with indentation

    def save_delta_time_to_file(self, delta_time):
        """
        Saves the fault localization session execution time (delta time) to a JSON file.

        Args:
            delta_time (float): Time taken by the fault localization session.
        """
        file_path = self._report_directory_path / constants.TIME_FILE_NAME_FL_SESSION
        delta_time_dict = {
            "DeltaTime": delta_time
        }
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(delta_time_dict, file, indent=4)  # Pretty-print with indentation

    def get_log_file_path(self):
        """
        Returns the absolute path of the log file.

        Returns:
            str: Absolute path to the log file.
        """
        file_path = self._report_directory_path / constants.LOG_FILE_NAME_FL_SESSION
        return str(file_path.absolute().resolve())
