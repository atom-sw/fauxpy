import math


class MetricMetallaxis:
    def __init__(self):
        self._metric_name = "Metallaxis"

    def get_metric_name(self):
        return self._metric_name

    @staticmethod
    def compute_mutant_score(
        mutant_failed_to_pass: int,
        mutant_failed_changed: int,
        mutant_passed_to_failed: int,
        num_all_failed,
    ):
        numerator = mutant_failed_to_pass + mutant_failed_changed
        tmp_term = num_all_failed * (
            mutant_failed_to_pass + mutant_failed_changed + mutant_passed_to_failed
        )
        if tmp_term == 0:
            score = 0
        else:
            denominator = math.sqrt(tmp_term)
            score = numerator / denominator

        return score

    @staticmethod
    def compute_entity_score(mutant_score_list):
        entity_score = max(mutant_score_list)
        return entity_score
