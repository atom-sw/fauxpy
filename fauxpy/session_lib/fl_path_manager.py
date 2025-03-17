import datetime
import shutil
from pathlib import Path

from fauxpy import constants
from fauxpy.command_line.pytest_mode import legacy_input

from .fl_type import FlFamily, FlGranularity, MutationStrategy


class FlPathManager:
    """A class that manages paths for a fault localization session."""

    def __init__(
        self,
        current_working_directory: Path,
        fl_family: FlFamily,
        fl_granularity: FlGranularity,
        mutation_strategy: MutationStrategy
    ):
        """
        Initializes the class instance.

        Args:
            current_working_directory (Path): The directory of the project that is the subject of fault localization.
            fl_family (FlFamily): The fault localization family.
            fl_granularity (FlGranularity): The granularity of fault localization.
            mutation_strategy (MutationStrategy): The mutation strategy used for generating mutations (only used by MBFL).
        """
        self._current_working_directory = current_working_directory
        self._fl_family = fl_family
        self._fl_granularity = fl_granularity
        self._mutation_strategy = mutation_strategy
        self._report_directory_path = None

    def get_report_directory_path(self) -> Path:
        """
        Returns the path to the fault localization report directory.
        If the report directory does not exist, it is created.

        Returns:
            Path: The path to the generated report directory.
        """
        if self._report_directory_path is None:
            self._report_directory_path = self._create_report_directory()

        return self._report_directory_path

    def _create_report_directory(self):
        """
        Creates and returns a new report directory based on the current working directory and other attributes.

        Returns:
            Path: The path to the newly created report directory.
        """
        current_working_dir_name = self._current_working_directory.name
        current_working_dir_parent_path = self._current_working_directory.parent
        ft = "%Y_%m_%d_%H_%M_%S_%f"
        current_data_time = datetime.datetime.now().strftime(ft)
        report_director_name = (
            f"{constants.FileNames.ReportDirectoryNamePrefix}_"
            f"{current_working_dir_name}_"
            f"{legacy_input.get_family_legacy(self._fl_family)}_"
            f"{legacy_input.get_granularity_legacy(self._fl_granularity)}_"
            f"{self._mutation_strategy.name.lower()}_"
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
