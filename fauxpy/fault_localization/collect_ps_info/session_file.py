import pathlib
from pathlib import Path
from typing import Optional

from fauxpy import constants
from fauxpy.constants import FileNames


class CollectPsInfoSessionFileManager:
    """
    Manages the saving and loading files during a ps info collect mode session.
    """

    def __init__(self, report_directory_path: Path, project_working_directory: Path):
        """
        Initializes the file manager.

        Args:
            report_directory_path (Path): The path to the directory where report files will be saved.
            project_working_directory (Path): The project's working directory path.
        """
        self._report_directory_path = report_directory_path
        self._project_working_directory = project_working_directory

    def save_predicate_sequence_table(self, json_table: str):
        """
        Saves the provided JSON-formatted predicate sequence table
        to the report directory.

        Args:
            json_table (str): The JSON string representing the predicate
            sequence table to be saved.
        """
        file_path = (
            self._report_directory_path
            / constants.FileNames.collectModePredicateSequences
        )
        with open(file_path, "w") as file:
            file.write(json_table)

    def load_executed_predicate_sequence_and_remove_file(self) -> Optional[str]:
        """
        Loads the predicate sequence file created by the
        instrumentation library for the current execution,
        deletes the file, and returns its content.

        Returns:
            Optional[str]: The content of the predicate sequence
            file if available; returns None if the file is missing
            or cannot be accessed.
        """

        file_path = self._project_working_directory / pathlib.Path(
            FileNames.instrumentationCollectModeExecutedPredicateSequenceFileName
        )
        try:
            with open(file_path, "r") as file:
                pred_sequence = file.read()
                if pred_sequence[-1] == ",":
                    pred_sequence = pred_sequence[0:-1]
                return pred_sequence
        except:
            return None
        finally:
            if file_path.exists():
                file_path.unlink()
