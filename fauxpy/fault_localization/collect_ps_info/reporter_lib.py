import json

from fauxpy.fault_localization.collect_ps_info.db_manager import CollectPsInfoDbManager


class CollectPsInfoReporter:
    def __init__(self, db_manager: CollectPsInfoDbManager):
        self._db_manager = db_manager

    # def save_test_predicate_sequence_table(self):
    #     table = self._db_manager.select_all_predicate_sequences()
    #     json_table = json.dumps(table)
    #     common.saveInCollectModePredicateSequenceTable(json_table)

    def get_json_test_predicate_sequence_table(self):
        table = self._db_manager.select_all_predicate_sequences()
        json_table = json.dumps(table)
        return json_table
