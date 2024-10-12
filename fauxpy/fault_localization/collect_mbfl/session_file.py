from pathlib import Path

from fauxpy import constants


class CollectMbflSessionFileManager:
    def __init__(self, report_directory_path: Path):
        self._report_directory_path = report_directory_path

    def save_in_collect_mode_test_case_table(self, json_table: str):
        temp = self._report_directory_path
        file_path = temp / constants.FileNames.collectModeTestCases
        with open(file_path, "w") as file:
            file.write(json_table)
