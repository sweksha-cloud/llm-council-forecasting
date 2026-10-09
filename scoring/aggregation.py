"""
Simple ways to combine several models' probabilities for one question.
These are the baselines a council has to beat: if a plain average does as
well, the deliberation isn't what's producing the gain.
"""

import math
import statistics
from typing import Sequence

EPS = 1e-6


def _clip(p: float) -> float:
    return min(max(p, EPS), 1 - EPS)


def logit(p: float) -> float:
    p = _clip(p)
    return math.log(p / (1 - p))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def mean_pool(ps: Sequence[float]) -> float:
    return statistics.fmean(ps)


def median_pool(ps: Sequence[float]) -> float:
    return statistics.median(ps)


def logit_pool(ps: Sequence[float]) -> float:
    """Average in log-odds space, then convert back (a geometric mean of odds)."""
    return sigmoid(statistics.fmean([logit(p) for p in ps]))


def extremize(p: float, a: float) -> float:
    """Push a probability away from 0.5: odds are raised to the power a (a > 1 extremizes)."""
    return sigmoid(a * logit(p))


def extremized_pool(ps: Sequence[float], a: float = 2.0) -> float:
    """Logit pool, then extremize. Known to beat plain averaging when forecasters see different evidence."""
    return extremize(logit_pool(ps), a)


def best_single(model_scores: dict) -> str:
    """Name of the model with the lowest (best) score, e.g. mean Brier on a training split."""
    if not model_scores:
        raise ValueError("no models given")
    return min(model_scores, key=model_scores.get)
