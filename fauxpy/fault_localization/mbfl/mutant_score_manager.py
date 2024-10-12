from fauxpy.fault_localization.mbfl.metric_metallaxis import MetricMetallaxis
from fauxpy.fault_localization.mbfl.db_manager import MbflDbManager
from fauxpy.fault_localization.mbfl.metric_muse import MetricMuse


class MutantScoreManager:
    EPSILON = 0.01

    def __init__(self, db_manager: MbflDbManager):
        self._db_manager = db_manager
        self._metric_muse = MetricMuse(self.EPSILON)
        self._metric_metallaxis = MetricMetallaxis()

    def compute_mutant_scores_store_db(self):
        (
            total_failed_to_passed,
            total_passed_to_failed,
        ) = self._db_manager.select_total_failed_to_passed_and_passed_to_failed()

        _, num_all_failed = self._db_manager.select_number_of_tests()

        mutants = self._db_manager.select_mutant_score_terms()
        for mutant in mutants:
            (
                mutant_id,
                mutant_failed_to_pass,
                mutant_passed_to_failed,
                mutant_failed_changed,
            ) = mutant

            muse_score = self._metric_muse.compute_mutant_score(
                mutant_failed_to_pass,
                mutant_passed_to_failed,
                total_failed_to_passed,
                total_passed_to_failed,
            )

            metallaxis_score = self._metric_metallaxis.compute_mutant_score(
                mutant_failed_to_pass,
                mutant_failed_changed,
                mutant_passed_to_failed,
                num_all_failed,
            )

            self._db_manager.update_mutant_score_terms(
                mutant_id, muse_score, metallaxis_score
            )
