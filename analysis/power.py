"""
power.py
--------
What Brier difference can the settled set detect?

For a paired comparison (council vs market, council vs best single) on n questions, the
smallest true mean Brier difference found 80% of the time at two-sided alpha = 0.05 is

    MDE = (1.96 + 0.84) * sd(d) / sqrt(n),   d = Brier(a) - Brier(b) per question

so everything depends on sd(d), the spread of per-question differences. Two sources:

  1. Aye's results (paired council vs market / mean / always-No). Her answers are 0 or 1,
     so Brier per question is 0 or 1 and sd(d) is as large as it gets: a pessimistic bound.
  2. Simulation on the real settled set (its market prices and outcomes). A model's forecast
     is the market price plus noise in log-odds (sd `sigma`); a council is a second, correlated
     draw. This is what probability forecasts look like, so it's the realistic case.

Questions aren't fully independent (e.g. several "ceasefire by <date>?" markets), so the
effective n is smaller than the count; the design effect at the end allows for that.

Usage (from the repo root):
  python3 -m analysis.power
"""

import csv
import math
import random
import statistics
from pathlib import Path
from typing import Dict, List, Tuple

from scoring.proper import brier
from scoring.report import add_baselines, add_reference_baselines, load

ROOT = Path(__file__).resolve().parent.parent
Z = 1.96 + 0.8416  # two-sided alpha 0.05, power 0.80


def mde(sd: float, n: int, design_effect: float = 1.0) -> float:
    return Z * sd * math.sqrt(design_effect / n)


def n_needed(sd: float, diff: float, design_effect: float = 1.0) -> int:
    return math.ceil((Z * sd / diff) ** 2 * design_effect)


def paired_sd(a: Dict[str, float], b: Dict[str, float], outcomes: Dict[str, int]) -> Tuple[int, float]:
    qs = [q for q in outcomes if a.get(q) is not None and b.get(q) is not None]
    d = [brier(a[q], outcomes[q]) - brier(b[q], outcomes[q]) for q in qs]
    return len(d), statistics.stdev(d)


def aye_sds() -> List[Tuple[str, int, float]]:
    out = []
    for prefix in ("aye-new:",):
        outcomes, probs, _, _ = load([str(ROOT / "data/imported/aye-2026/questions.csv")],
                                     [str(ROOT / "data/imported/aye-2026/forecasts.csv")], id_prefix=prefix)
        add_baselines(probs, outcomes)
        add_reference_baselines(probs, outcomes)
        for ref in ("market", "baseline:mean", "baseline:always_no"):
            for c in sorted(s for s in probs if s.startswith("council:")):
                n, sd = paired_sd(probs[c], probs[ref], outcomes)
                out.append((f"Aye: {c.split('=')[1].split(':')[0]} council vs {ref.replace('baseline:', '')}", n, sd))
    return out


def settled_market() -> Tuple[List[float], List[int]]:
    ps, ys = [], []
    with (ROOT / "data/questions.csv").open(newline="", encoding="utf-8") as f:
        for q in csv.DictReader(f):
            if q["set"] == "settled" and q["outcome"] in ("0", "1") and q["market_price"]:
                ps.append(float(q["market_price"]))
                ys.append(int(q["outcome"]))
    return ps, ys


def logit(p: float) -> float:
    p = min(max(p, 0.005), 0.995)
    return math.log(p / (1 - p))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def simulated_sds(ps: List[float], ys: List[int], sigma: float, rho: float = 0.7,
                  reps: int = 200, seed: int = 0) -> Dict[str, float]:
    """Median sd(d) over `reps` simulated runs. Model = market + N(0, sigma) in log-odds; the
    council's noise has correlation `rho` with the model's (it's built from the same members)."""
    rng = random.Random(seed)
    vs_market, vs_member, model_brier = [], [], []
    for _ in range(reps):
        d_m, d_c, b = [], [], []
        for p, y in zip(ps, ys):
            e1 = rng.gauss(0, sigma)
            e2 = rho * e1 + math.sqrt(1 - rho ** 2) * rng.gauss(0, sigma)
            model, council = sigmoid(logit(p) + e1), sigmoid(logit(p) + e2)
            d_m.append(brier(council, y) - brier(p, y))
            d_c.append(brier(council, y) - brier(model, y))
            b.append(brier(model, y))
        model_brier.append(statistics.fmean(b))
        vs_market.append(statistics.stdev(d_m))
        vs_member.append(statistics.stdev(d_c))
    return {"vs_market": statistics.median(vs_market), "vs_member": statistics.median(vs_member),
            "model_brier": statistics.median(model_brier)}


def main() -> None:
    ps, ys = settled_market()
    n = len(ps)
    print(f"Settled set: {n} questions with a market price and an outcome "
          f"(market Brier {statistics.fmean(brier(p, y) for p, y in zip(ps, ys)):.3f}, "
          f"{sum(ys) / n:.1%} resolved Yes)\n")

    rows = [(label, n_pairs, sd) for label, n_pairs, sd in aye_sds()]
    for sigma in (0.5, 1.0, 1.5, 2.0):
        sds = simulated_sds(ps, ys, sigma)
        print(f"Simulated forecaster with σ={sigma}: Brier {sds['model_brier']:.3f}")
        rows.append((f"Sim σ={sigma}: council vs market", n, sds["vs_market"]))
        rows.append((f"Sim σ={sigma}: council vs a member (ρ=0.7)", n, sds["vs_member"]))

    print(f"| Comparison | sd(d) | MDE, n={n} | MDE, n={n}, design effect 1.5 | n for 0.01 | n for 0.02 | n for 0.05 |")
    print("|---|---|---|---|---|---|---|")
    for label, _, sd in rows:
        print(f"| {label} | {sd:.3f} | {mde(sd, n):.3f} | {mde(sd, n, 1.5):.3f} | "
              f"{n_needed(sd, 0.01):,} | {n_needed(sd, 0.02):,} | {n_needed(sd, 0.05):,} |")

    # Contamination split: two independent groups (153 older vs n settled questions).
    # Raw Brier per question, or Brier minus the market's on the same question (the excess_gap
    # design: removes question difficulty, so the spread is smaller).
    n_old = 153
    print()
    for sigma in (0.5, 1.0, 1.5, 2.0):
        rng = random.Random(1)
        model = [sigmoid(logit(p) + rng.gauss(0, sigma)) for p in ps]
        raw = statistics.stdev([brier(m, y) for m, y in zip(model, ys)])
        excess = statistics.stdev([brier(m, y) - brier(p, y) for m, p, y in zip(model, ps, ys)])
        k = Z * math.sqrt(1 / n_old + 1 / n)
        print(f"Contamination gap, σ={sigma}, {n_old} vs {n} questions: MDE {k * raw:.3f} on raw Brier, "
              f"{k * excess:.3f} on Brier minus market")


if __name__ == "__main__":
    main()
