"""
Discrimination: does the forecaster give higher probabilities to events that happen?

AUROC is the chance that a randomly chosen question that resolved Yes got a higher
forecast than a randomly chosen one that resolved No (ties count half). 0.5 is no
better than chance, 1.0 is perfect ranking. It ignores calibration entirely: a model
that says 0.55 for every Yes and 0.52 for every No has AUROC 1.0 but poor Brier.
"""

from typing import List, Optional, Sequence


def average_ranks(xs: Sequence[float]) -> List[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1  # ties share the average rank
        i = j + 1
    return ranks


def auroc(ps: Sequence[float], ys: Sequence[int]) -> Optional[float]:
    """Area under the ROC curve (Mann-Whitney form). None if every outcome is the same."""
    if len(ps) != len(ys):
        raise ValueError(f"length mismatch: {len(ps)} forecasts, {len(ys)} outcomes")
    n_pos = sum(1 for y in ys if y == 1)
    n_neg = len(ys) - n_pos
    if n_pos == 0 or n_neg == 0:
        return None
    ranks = average_ranks(ps)
    pos_rank_sum = sum(r for r, y in zip(ranks, ys) if y == 1)
    return (pos_rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)
