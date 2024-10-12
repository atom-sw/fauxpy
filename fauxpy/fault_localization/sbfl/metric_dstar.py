import math


class MetricDstar:
    def __init__(self, epsilon: float):
        self._metric_name = "Dstar"
        self._epsilon = epsilon

    def get_metric_name(self):
        return self._metric_name

    def compute(self, ef, ep, nf, np):
        score = float(math.pow(ef, 2)) / (ep + nf + self._epsilon)
        return score
