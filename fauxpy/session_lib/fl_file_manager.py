import csv
import json
from pathlib import Path
from typing import List, Tuple

from fauxpy import constants


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
            writer.writerow(constants.FileNames.ScoresFileNameHeader)
            for score in scores:
                writer.writerow([score[0], score[1]])

    def save_config_to_file(
        self,
        src: str,
        exclude: List[str],
        family: str,
        granularity: str,
        top_n: str,
        targeted_failing_tests: List[str],
        mutation_strategy: str
    ):
        """
        Saves the session configuration to a JSON file.

        Args:
            src (str): Source code directory to perform fault localization on.
            exclude (List[str]): List of files or directories to exclude from fault localization.
            family (str): Family of the fault localization technique.
            granularity (str): Fault localization granularity level.
            top_n (str): Number of top-ranked elements to show in the output.
            targeted_failing_tests (List[str]): List of failing test cases that are the target of current fault localization session.
            mutation_strategy (str): Strategy used for mutation analysis (only used by the MBFL family).
        """
        file_path = self._report_directory_path / constants.SESSION_CONFIG_FILE_NAME

        config_dict = {
            "Src": src,
            "Exclude": exclude,
            "Family":  family,
            "Granularity": granularity,
            "TopN": top_n,
            "TargetedFailingTests": targeted_failing_tests,
            "MutationStrategy": mutation_strategy
        }

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(config_dict, file, indent=4)  # Pretty-print with indentation

    def save_delta_time_to_file(self, delta_time):
        """
        Saves the fault localization session execution time (delta time) to a JSON file.

        Args:
            delta_time (float): Time taken by the fault localization session.
        """
        file_path = self._report_directory_path / constants.SESSION_TIME_FILE_NAME
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
        file_path = self._report_directory_path / constants.SESSION_LOG_FILE_NAME
        return str(file_path.absolute().resolve())
