import json
import pathlib
from typing import Optional, List, Tuple

from fauxpy import constants
from fauxpy.constants import FileNames


class CollectPsRunApiFileManager:
    @staticmethod
    def load_test_case_table(
        project_path: str,
    ) -> Optional[List[Tuple[str, str, str]]]:
        file_path = (
            pathlib.Path(project_path)
            / FileNames.CollectModeDirectoryName
            / FileNames.collectModeTestCases
        )
        if not file_path.exists():
            return None

        with open(file_path, "r") as file:
            json_table = file.read()
            table = json.loads(json_table)
        return table

    @staticmethod
    def load_seen_exception_sequence_table(
        project_path,
    ) -> Optional[List[Tuple[str, str]]]:
        file_path = (
            pathlib.Path(project_path)
            / FileNames.CollectModeDirectoryName
            / FileNames.collectModeSeenExceptions
        )
        if not file_path.exists():
            return None

        with open(file_path, "r") as file:
            json_table = file.read()
            table = json.loads(json_table)
        return table

    @staticmethod
    def save_config_file(project_path: str, predicate_name: str, instance_number: int):
        config_file_name = constants.getCollectModeConfigFileName()
        config_file_path = pathlib.Path(project_path) / pathlib.Path(config_file_name)
        content_dictionary = {
            "PredicateName": predicate_name,
            "InstanceNumber": instance_number,
        }
        json_content = json.dumps(content_dictionary)
        with open(config_file_path, "w") as file:
            file.write(json_content)
