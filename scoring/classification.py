"""
Ground-truth metrics: each forecast read as a Yes/No call and checked against what happened.

A forecast above 0.5 is a Yes call, below 0.5 a No call, exactly 0.5 is no call (left out
of the confusion matrix, as `accuracy` counts it half). "Positive" means the event happened.

  precision          of the Yes calls, the share that happened
  recall             of the events that happened, the share called Yes
  f1                 harmonic mean of precision and recall
  balanced_accuracy  mean of recall on Yes and recall on No; 0.5 for "always No", whatever the base rate
  mcc                Matthews correlation between calls and outcomes; 0 = no better than chance, 1 = perfect

Plain accuracy rewards saying No when most questions resolve No; balanced accuracy and MCC don't.
"""

import math
from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass
class Confusion:
    tp: int  # called Yes, happened
    fp: int  # called Yes, didn't happen
    tn: int  # called No, didn't happen
    fn: int  # called No, happened
    no_call: int  # forecast exactly 0.5


def confusion(ps: Sequence[float], ys: Sequence[int]) -> Confusion:
    if len(ps) != len(ys):
        raise ValueError(f"length mismatch: {len(ps)} forecasts, {len(ys)} outcomes")
    c = Confusion(0, 0, 0, 0, 0)
    for p, y in zip(ps, ys):
        if p == 0.5:
            c.no_call += 1
        elif p > 0.5:
            c.tp += y == 1
            c.fp += y == 0
        else:
            c.fn += y == 1
            c.tn += y == 0
    return c


def _ratio(a: float, b: float) -> Optional[float]:
    return a / b if b else None


def precision(c: Confusion) -> Optional[float]:
    return _ratio(c.tp, c.tp + c.fp)


def recall(c: Confusion) -> Optional[float]:
    return _ratio(c.tp, c.tp + c.fn)


def f1(c: Confusion) -> Optional[float]:
    return _ratio(2 * c.tp, 2 * c.tp + c.fp + c.fn)


def balanced_accuracy(c: Confusion) -> Optional[float]:
    """None unless both Yes and No outcomes are present among the calls."""
    yes_recall, no_recall = _ratio(c.tp, c.tp + c.fn), _ratio(c.tn, c.tn + c.fp)
    if yes_recall is None or no_recall is None:
        return None
    return (yes_recall + no_recall) / 2


def mcc(c: Confusion) -> Optional[float]:
    """Matthews correlation. 0 when every call is the same (no information), None with no calls."""
    if c.tp + c.fp + c.tn + c.fn == 0:
        return None
    denom = math.sqrt((c.tp + c.fp) * (c.tp + c.fn) * (c.tn + c.fp) * (c.tn + c.fn))
    return (c.tp * c.tn - c.fp * c.fn) / denom if denom else 0.0
