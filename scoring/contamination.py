"""
Contamination check: do models score better on questions that resolved before their
training cutoff (when they might remember the answer) than on questions after it?

A raw before/after gap isn't enough: the older questions may just be easier. So the
market is scored on the same two groups, and `excess_gap` is the model's gap minus the
market's. Clearly negative excess_gap (the model gains more on old questions than the
market does) points to recall rather than forecasting.

Cutoffs come from docs/models.md. Where no cutoff is published, the release date is used:
a model can't have seen anything after it was released, so it's a safe upper bound.
A council or pooled baseline can know whatever any member knows, so it gets the latest
cutoff among its members.
"""

import random
import statistics
from datetime import date
from typing import Dict, List, Optional, Sequence, Tuple

from scoring.proper import accuracy, brier, mean_brier

# Ollama tag prefix -> (cutoff, basis). Keep in step with docs/models.md.
MODEL_CUTOFFS: Dict[str, Tuple[date, str]] = {
    "llama3.1": (date(2023, 12, 31), "stated cutoff"),
    "phi3": (date(2023, 10, 31), "stated cutoff"),
    "mistral": (date(2024, 5, 22), "release date"),
    "gemma2": (date(2024, 6, 27), "release date"),
    "qwen3": (date(2025, 4, 29), "release date"),
    # The tag has meant a Llama-based (Jan 2025) and a Qwen3-based (May 2025) distill; the later is the safe bound.
    "deepseek-r1": (date(2025, 5, 28), "release date"),
}


def model_cutoff(tag: str) -> Optional[Tuple[date, str]]:
    return MODEL_CUTOFFS.get(tag.split(":")[0])


def setup_cutoff(setup: str, members: Sequence[str] = ()) -> Optional[Tuple[date, str]]:
    """Cutoff for a setup. single:<tag> uses its model; council/baseline setups use the latest
    cutoff among `members` (model tags). None if any member's cutoff is unknown, or for the market."""
    if setup.startswith("single:"):
        return model_cutoff(setup.split(":", 1)[1])
    if setup == "market" or not members:
        return None
    cutoffs = [model_cutoff(m) for m in members]
    if any(c is None for c in cutoffs):
        return None
    latest = max(cutoffs, key=lambda c: c[0])
    return latest[0], f"latest member ({latest[1]})"


def _draw(values: List[float], keys: List[str], rng: random.Random) -> List[float]:
    """Resample with replacement within each stratum (source), keeping each stratum's size."""
    groups: Dict[str, List[float]] = {}
    for v, k in zip(values, keys):
        groups.setdefault(k, []).append(v)
    return [x for k in sorted(groups) for x in rng.choices(groups[k], k=len(groups[k]))]


def gap_interval(before: List[float], after: List[float], n_boot: int = 1000, seed: int = 0,
                 keys_before: Optional[List[str]] = None, keys_after: Optional[List[str]] = None) -> Tuple[float, float]:
    """95% bootstrap interval for mean(before) - mean(after) (two independent groups), resampling
    within source inside each group when keys are given."""
    rng = random.Random(seed)
    kb, ka = keys_before or [""] * len(before), keys_after or [""] * len(after)
    boots = sorted(statistics.fmean(_draw(before, kb, rng)) - statistics.fmean(_draw(after, ka, rng))
                   for _ in range(n_boot))
    return boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot) - 1]


def split_table(probs: Dict[str, Dict[str, Optional[float]]], outcomes: Dict[str, int],
                resolved_on: Dict[str, date], members_of: Dict[str, List[str]],
                n_boot: int = 1000, strata: Optional[Dict[str, str]] = None) -> List[Dict]:
    """One row per setup with a known cutoff: scores on questions resolved before vs after it.
    `members_of` maps council/baseline setups to the model tags they're built from; `strata`
    (question -> source) makes every interval resample within source.

    excess_gap is computed per question on the questions with a market price: the mean of
    Brier(setup) - Brier(market) before the cutoff minus the same after it, so the model and the
    market are compared on exactly the same questions. Negative = the setup gains more on old
    questions than the market does."""
    keys = lambda qs: [(strata or {}).get(q, "") for q in qs]
    market = probs.get("market", {})
    rows = []
    for setup in probs:
        cut = setup_cutoff(setup, members_of.get(setup, ()))
        if cut is None:
            continue
        cutoff, basis = cut
        answered = [q for q in outcomes if probs[setup].get(q) is not None and q in resolved_on]
        groups = {"before": [q for q in answered if resolved_on[q] <= cutoff],
                  "after": [q for q in answered if resolved_on[q] > cutoff]}
        row = {"setup": setup, "cutoff": cutoff.isoformat(), "basis": basis}
        for name, qs in groups.items():
            row[f"n_{name}"] = len(qs)
            if qs:
                ps, ys = [probs[setup][q] for q in qs], [outcomes[q] for q in qs]
                row[f"brier_{name}"] = round(mean_brier(ps, ys), 4)
                row[f"accuracy_{name}"] = round(accuracy(ps, ys), 4)
                priced = [q for q in qs if market.get(q) is not None]
                if priced:
                    row[f"market_brier_{name}"] = round(mean_brier([market[q] for q in priced],
                                                                   [outcomes[q] for q in priced]), 4)
        before, after = groups["before"], groups["after"]
        if len(before) >= 2 and len(after) >= 2:
            b = [brier(probs[setup][q], outcomes[q]) for q in before]
            a = [brier(probs[setup][q], outcomes[q]) for q in after]
            row["gap"] = round(statistics.fmean(b) - statistics.fmean(a), 4)
            lo, hi = gap_interval(b, a, n_boot, keys_before=keys(before), keys_after=keys(after))
            row["gap_ci_low"], row["gap_ci_high"] = round(lo, 4), round(hi, 4)
        pb, pa = ([q for q in qs if market.get(q) is not None] for qs in (before, after))
        if len(pb) >= 2 and len(pa) >= 2:
            d = lambda qs: [brier(probs[setup][q], outcomes[q]) - brier(market[q], outcomes[q]) for q in qs]
            db, da = d(pb), d(pa)
            row["excess_gap"] = round(statistics.fmean(db) - statistics.fmean(da), 4)
            lo, hi = gap_interval(db, da, n_boot, keys_before=keys(pb), keys_after=keys(pa))
            row["excess_ci_low"], row["excess_ci_high"] = round(lo, 4), round(hi, 4)
        rows.append(row)
    return rows
