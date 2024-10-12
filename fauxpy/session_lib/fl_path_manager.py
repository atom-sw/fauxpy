import datetime
import shutil
from pathlib import Path

from fauxpy import constants
from fauxpy.command_line.pytest_mode import legacy_input

from fauxpy.session_lib.fl_type import FlFamily, FlGranularity


class FlPathManager:
    def __init__(
        self,
        current_working_directory: Path,
        fl_family: FlFamily,
        fl_granularity: FlGranularity,
    ):
        self._current_working_directory = current_working_directory
        self._fl_family = fl_family
        self._fl_granularity = fl_granularity
        self._report_directory_path = None

    def get_report_directory_path(self) -> Path:
        if self._report_directory_path is None:
            self._report_directory_path = self._create_report_directory()

        return self._report_directory_path

    def _create_report_directory(self):
        current_working_dir_name = self._current_working_directory.name
        current_working_dir_parent_path = self._current_working_directory.parent
        ft = "%Y_%m_%d_%H_%M_%S_%f"
        current_data_time = datetime.datetime.now().strftime(ft)
        report_director_name = (
            f"{constants.FileNames.ReportDirectoryNamePrefix}_"
            f"{current_working_dir_name}_"
            f"{legacy_input.get_family_legacy(self._fl_family)}_"
            f"{legacy_input.get_granularity_legacy(self._fl_granularity)}_"
            f"{current_data_time}"
        )
        report_directory_path = current_working_dir_parent_path / report_director_name

        if self._fl_family in [
            FlFamily.CollectMbfl,
            FlFamily.CollectPsInfo,
            FlFamily.CollectPsRun,
        ]:
            report_directory_path = (
                self._current_working_directory
                / constants.FileNames.CollectModeDirectoryName
            )

        if report_directory_path.exists():
            shutil.rmtree(report_directory_path)  # Remove last reports

        report_directory_path.mkdir()

        return report_directory_path
