import json

from fauxpy.fault_localization.collect_ps_run.db_manager import CollectPsRunDbManager


class CollectPsRunReporter:
    def __init__(self, db_manager: CollectPsRunDbManager):
        self._db_manager = db_manager

    # def save_test_cases(self):
    #     test_cases_table = self._db_manager.select_all_test_cases()
    #     json_test_cases_table = json.dumps(test_cases_table)
    #     common.saveInCollectModeTestCaseTable(json_test_cases_table)

    def get_json_test_case_table(self):
        test_cases_table = self._db_manager.select_all_test_cases()
        json_test_cases_table = json.dumps(test_cases_table)
        return json_test_cases_table

    # def save_seen_exception_sequence_table(self):
    #     table = self._db_manager.select_all_seen_exceptions()
    #     json_table = json.dumps(table)
    #     common.saveInCollectModeSeenExceptionSequenceTable(json_table)

    def get_json_seen_exception_sequence_table(self):
        table = self._db_manager.select_all_seen_exceptions()
        json_table = json.dumps(table)
        return json_table
