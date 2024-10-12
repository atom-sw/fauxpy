import json
import pathlib

from fauxpy.constants import FileNames


class CollectPsInfoApiFileManager:
    @staticmethod
    def load_predicate_sequence_table(project_path):
        file_path = (
            pathlib.Path(project_path)
            / FileNames.CollectModeDirectoryName
            / FileNames.collectModePredicateSequences
        )
        with open(file_path, "r") as file:
            json_table = file.read()
            table = json.loads(json_table)
        return table
