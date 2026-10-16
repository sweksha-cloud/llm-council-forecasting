"""
Calibration and Murphy decomposition of the Brier score.

  Brier = reliability - resolution + uncertainty

  reliability  - are events given 70% happening about 70% of the time? (lower is better)
  resolution   - does the forecaster move away from the base rate in the right direction? (higher is better)
  uncertainty  - depends only on the questions, not the forecaster: base_rate * (1 - base_rate)

Sharpness is how far forecasts move away from 50%: the mean of |p - 0.5|, from 0 (always 50%)
to 0.5 (always 0% or 100%). ECE alone can look fine for a model that never commits, so the two
are read together: be calibrated, and as sharp as possible. Sharpness ignores outcomes.

Expected calibration error (ECE) summarises the reliability diagram in one number: the average
gap between forecast and observed frequency, weighted by how many forecasts fall in each bin.

The identity is exact when every forecast in a bin is the same value. With
binned continuous forecasts it's approximate; `brier` is reported alongside
so the gap is visible.
"""

from dataclasses import dataclass
from typing import List, Sequence

from .proper import mean_brier


@dataclass
class Bin:
    lower: float
    upper: float
    count: int
    mean_forecast: float
    observed_rate: float


@dataclass
class Decomposition:
    reliability: float
    resolution: float
    uncertainty: float
    brier: float
    bins: List[Bin]


def reliability_bins(ps: Sequence[float], ys: Sequence[int], n_bins: int = 10) -> List[Bin]:
    """Group forecasts into equal-width bins; empty bins are left out. This is the data for a reliability diagram."""
    if len(ps) != len(ys) or not ps:
        raise ValueError("need the same, non-zero number of forecasts and outcomes")
    groups = [[] for _ in range(n_bins)]
    for p, y in zip(ps, ys):
        i = min(int(p * n_bins), n_bins - 1)  # p = 1.0 goes in the top bin
        groups[i].append((p, y))
    bins = []
    for i, g in enumerate(groups):
        if g:
            bins.append(Bin(
                lower=i / n_bins, upper=(i + 1) / n_bins, count=len(g),
                mean_forecast=sum(p for p, _ in g) / len(g),
                observed_rate=sum(y for _, y in g) / len(g),
            ))
    return bins


def murphy_decomposition(ps: Sequence[float], ys: Sequence[int], n_bins: int = 10) -> Decomposition:
    bins = reliability_bins(ps, ys, n_bins)
    n = len(ps)
    base_rate = sum(ys) / n
    rel = sum(b.count * (b.mean_forecast - b.observed_rate) ** 2 for b in bins) / n
    res = sum(b.count * (b.observed_rate - base_rate) ** 2 for b in bins) / n
    unc = base_rate * (1 - base_rate)
    return Decomposition(rel, res, unc, mean_brier(ps, ys), bins)


def sharpness(ps: Sequence[float]) -> float:
    """Mean distance from 50%. 0 = never commits; 0.5 = always says 0% or 100%. Higher is sharper."""
    if not ps:
        raise ValueError("no forecasts")
    return sum(abs(p - 0.5) for p in ps) / len(ps)


def expected_calibration_error(ps: Sequence[float], ys: Sequence[int], n_bins: int = 10) -> float:
    """Count-weighted mean of |mean forecast - observed rate| over equal-width bins. 0 is perfectly calibrated."""
    bins = reliability_bins(ps, ys, n_bins)
    return sum(b.count * abs(b.mean_forecast - b.observed_rate) for b in bins) / len(ps)
