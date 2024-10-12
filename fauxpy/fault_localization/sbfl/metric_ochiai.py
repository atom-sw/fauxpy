import math


class MetricOchiai:
    def __init__(self, epsilon: float):
        self._metric_name = "Ochiai"
        self._epsilon = epsilon

    def get_metric_name(self):
        return self._metric_name

    def compute(self, ef, ep, nf, np):
        score = float(ef) / (math.sqrt((ef + nf) * (ef + ep)) + self._epsilon)
        return score
