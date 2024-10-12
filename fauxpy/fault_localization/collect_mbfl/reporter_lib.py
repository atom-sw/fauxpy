import json

from fauxpy.fault_localization.collect_mbfl.db_manager import CollectMbflDBManager


class CollectMbflReporter:
    def __init__(self, db_manager: CollectMbflDBManager):
        self._db_manager = db_manager

    # def save_test_cases(self):
    #     test_cases_table = self._db_manager.select_all_test_cases()
    #     json_test_cases_table = json.dumps(test_cases_table)
    #     common.saveInCollectModeTestCaseTable(json_test_cases_table)

    def get_json_test_case_table(self):
        test_cases_table = self._db_manager.select_all_test_cases()
        json_test_cases_table = json.dumps(test_cases_table)
        return json_test_cases_table
