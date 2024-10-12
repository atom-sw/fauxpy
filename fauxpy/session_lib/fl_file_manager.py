import csv
from pathlib import Path
from typing import List, Tuple

from fauxpy import constants


class FlFileManager:
    def __init__(self, report_directory_path: Path):
        self._report_directory_path = report_directory_path

    def save_scores_to_file(self, technique: str, scores: List[Tuple[str, int]]):
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
        target_failing_tests: List[str],
    ):
        file_path = self._report_directory_path / constants.FileNames.ConfigFileName
        with open(file_path, "w") as file:
            file.write(f"Src = {src}\r\n")
            file.write(f"Exclude = {exclude}\r\n")
            file.write(f"Family = {family}\r\n")
            file.write(f"Granularity = {granularity}\r\n")
            file.write(f"TopN = {top_n}\r\n")
            file.write(f"TargetFailingTests = {target_failing_tests}\r\n")

    def save_delta_time_to_file(self, delta_time):
        file_path = self._report_directory_path / constants.FileNames.DeltaTimeFileName
        with open(file_path, "w") as file:
            file.write(f"DeltaTime = {delta_time}")

    def get_log_file_path(self):
        file_path = self._report_directory_path / constants.FileNames.LogFilePath
        return str(file_path.absolute().resolve())
