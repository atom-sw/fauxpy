class MetricMuse:
    def __init__(self, epsilon: float):
        self._metric_name = "Muse"
        self._epsilon = epsilon

    def get_metric_name(self):
        return self._metric_name

    def compute_mutant_score(
        self,
        mutant_failed_to_pass: int,
        mutant_passed_to_failed: int,
        total_failed_to_passed: int,
        total_passed_to_failed: int,
    ) -> float:
        # ToDo: find a better way to solve the problem (i.e., totalPassedToFailed = 0).
        fraction = float(total_failed_to_passed) / (
            total_passed_to_failed + self._epsilon
        )
        score = mutant_failed_to_pass - fraction * mutant_passed_to_failed

        return score

    @staticmethod
    def compute_entity_score(mutant_score_list):
        entity_score = float(sum(mutant_score_list)) / len(mutant_score_list)
        return entity_score
