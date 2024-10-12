from typing import List, Tuple

from fauxpy.fault_localization.sbfl.db_manager import SbflDbManager
from fauxpy.fault_localization.sbfl.metric_dstar import MetricDstar
from fauxpy.fault_localization.sbfl.metric_ochiai import MetricOchiai
from fauxpy.fault_localization.sbfl.metric_tarantula import MetricTarantula

# ToDo: Find better ways to handle the division by zero issue.

"""
eF: Number of failed tests that execute the program element.
eP: Number of passed tests that execute the program element.
nF: Number of failed tests that do not execute the program element.
nP: Number of passed tests that do not execute the program element.
"""


class RankingMetricManager:
    EPSILON = 0.1

    def __init__(self, db_manager: SbflDbManager):
        self._db_manager = db_manager
        self._ranking_metric_list = [
            MetricTarantula(self.EPSILON),
            MetricOchiai(self.EPSILON),
            MetricDstar(self.EPSILON),
        ]

    def _ranking_metric(self, ef, ep, nf, np):
        scores = {}
        for ranking_metric in self._ranking_metric_list:
            metric_score = ranking_metric.compute(ef, ep, nf, np)
            metric_name = ranking_metric.get_metric_name()
            scores[metric_name] = metric_score

        return scores

    def compute_sorted_scores(self, top_n: int) -> List[Tuple[str, int]]:
        entity_list = self._db_manager.select_distinct_executed_entity_list()
        num_all_passed, num_all_failed = self._db_manager.select_number_of_tests()

        for entity in entity_list:
            num_cov_passed, num_cov_failed = (
                self._db_manager.select_number_of_covering_tests(entity)
            )

            assert num_all_passed >= num_cov_passed
            assert num_all_failed >= num_cov_failed

            if num_cov_passed + num_cov_failed == 0:
                # entities covered by xfail, xpass, and not targeted failing tests.
                continue

            ef = num_cov_failed
            ep = num_cov_passed
            nf = num_all_failed - ef
            np = num_all_passed - ep

            scored_entity_list_dict = self._ranking_metric(ef, ep, nf, np)
            self._db_manager.inert_scores(
                entity, ef, ep, nf, np, scored_entity_list_dict
            )

        if top_n == -1:
            score_entity_list = self._db_manager.select_all_ranked_entities()
        elif top_n >= 1:
            score_entity_list = self._db_manager.select_top_n_ranked_entities(top_n)
        else:
            raise Exception(f"TopN {top_n} is not supported.")

        return score_entity_list
