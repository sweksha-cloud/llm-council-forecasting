"""
Proper scoring rules for binary forecasts.

Conventions used everywhere in this project:
  - p is the forecast probability that the event happens (0..1)
  - y is the outcome: 1 if it happened, 0 if not
  - lower scores are better for both Brier and log score

Abstentions are never silently turned into a number. Score only the
forecasts that exist, and report `coverage` alongside, or fill abstentions
explicitly with `fill_abstentions` and say so.
"""

import math
from typing import Iterable, List, Optional, Sequence, Tuple

EPS = 1e-6  # keeps log score finite for forecasts of exactly 0 or 1


def _check(p: float, y: int) -> None:
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"probability must be in [0, 1], got {p}")
    if y not in (0, 1):
        raise ValueError(f"outcome must be 0 or 1, got {y}")


def brier(p: float, y: int) -> float:
    """Squared error between forecast and outcome. 0 is perfect, 0.25 is always saying 0.5."""
    _check(p, y)
    return (p - y) ** 2


def log_score(p: float, y: int, eps: float = EPS) -> float:
    """Negative log of the probability given to what happened. Punishes confident misses hard."""
    _check(p, y)
    q = min(max(p, eps), 1 - eps)
    return -math.log(q if y == 1 else 1 - q)


def _mean(xs: Sequence[float]) -> float:
    if not xs:
        raise ValueError("no forecasts to score")
    return sum(xs) / len(xs)


def mean_brier(ps: Sequence[float], ys: Sequence[int]) -> float:
    _same_length(ps, ys)
    return _mean([brier(p, y) for p, y in zip(ps, ys)])


def mean_log_score(ps: Sequence[float], ys: Sequence[int], eps: float = EPS) -> float:
    _same_length(ps, ys)
    return _mean([log_score(p, y, eps) for p, y in zip(ps, ys)])


def brier_skill_score(ps: Sequence[float], ys: Sequence[int], ref_ps: Sequence[float]) -> float:
    """1 - Brier / reference Brier. Positive means better than the reference (e.g. the market)."""
    ref = mean_brier(ref_ps, ys)
    if ref == 0:
        raise ValueError("reference forecasts are perfect; skill is undefined")
    return 1 - mean_brier(ps, ys) / ref


def drop_abstentions(ps: Iterable[Optional[float]], ys: Iterable[int]) -> Tuple[List[float], List[int], float]:
    """Keep only answered forecasts. Returns (probabilities, outcomes, coverage)."""
    pairs = list(zip(ps, ys))
    kept = [(p, y) for p, y in pairs if p is not None]
    coverage = len(kept) / len(pairs) if pairs else 0.0
    return [p for p, _ in kept], [y for _, y in kept], coverage


def fill_abstentions(ps: Iterable[Optional[float]], value: float = 0.5) -> List[float]:
    """Replace abstentions with an explicit value (0.5 = 'no idea')."""
    return [value if p is None else p for p in ps]


def _same_length(a: Sequence, b: Sequence) -> None:
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} forecasts, {len(b)} outcomes")
