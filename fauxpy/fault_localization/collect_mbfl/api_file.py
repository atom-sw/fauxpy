import json
import pathlib
from typing import Optional, List, Tuple

from fauxpy.constants import FileNames


class CollectMbflApiFileManager:
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
