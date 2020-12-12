import numpy as np
import pandas as pd
from scipy.stats import chi2
from typing import Tuple

class IncorrectInputDataError(Exception):
    pass

class ChiSquaredNormalCheck:

    def __init__(self, conf_level:float = 0.05, num_parts: int = 6):
        self.conf_level: float = conf_level
        self.num_parts: int = num_parts

    @staticmethod
    def _input_checker(values: np.ndarray) -> np.ndarray:
        if not isinstance(values, np.ndarray) or not len(values):
            raise IncorrectInputDataError
        values: np.array = values
        return values

    @staticmethod
    def _generate_normal(arr, sigm, m):
        return np.exp((-(arr - m) ** 2) / (2 * sigm ** 2)) / (sigm * np.sqrt(2 * np.pi))

    def compute(self, values: np.ndarray) -> Tuple[bool, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]: #h, our_prob, normal_prob, s_sq, X, res
        data: np.ndarray = self._input_checker(values)
        h = (data.max() - data.min()) / self.num_parts
        groups = [(data.min() + x * h, data.min() + x * h + h) for x in range(self.num_parts)]
        freq = np.zeros(self.num_parts)
        for i in data:
            for j in range(len(groups)):
                if i >= groups[j][0] and i < groups[j][1]:
                    freq[j] += 1
        xi = [a + (b - a) / 2 for a, b in groups]
        x_m = (xi * freq).sum() / freq.sum()
        s_sq = ((xi - x_m) ** 2 * freq).sum() / (freq.sum() - 1)
        s = np.sqrt(s_sq)
        our_prob = freq.copy()
        normal_prob = (self._generate_normal(xi, s, x_m) / self._generate_normal(xi, s, x_m).sum()) * len(data)
        X = ((our_prob - normal_prob) ** 2 / normal_prob).sum()
        res = X < chi2.isf(self.conf_level, self.num_parts - 3)
        return (res, h, our_prob, normal_prob, s_sq, X)
