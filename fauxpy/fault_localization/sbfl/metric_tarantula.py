class MetricTarantula:
    def __init__(self, epsilon: float):
        self._metric_name = "Tarantula"
        self._epsilon = epsilon

    def get_metric_name(self):
        return self._metric_name

    def compute(self, ef, ep, nf, np):
        numerator = float(ef) / (ef + nf + self._epsilon)
        denominator = (float(ef) / (ef + nf + self._epsilon)) + (
            float(ep) / (ep + np + self._epsilon)
        )
        score = numerator / denominator + self._epsilon
        return score
