"""
recalibration.py
----------------
Can a fixed transform rescue a setup's forecasts? Two post-hoc recalibrations, each fitted on
one half of the questions and tested on the other half:

  extremizing   p' = sigmoid(a * logit p)             one parameter; a > 1 pushes away from 50%
  Platt         p' = sigmoid(alpha + beta * logit p)  also corrects a constant lean toward Yes or No

The halves are fixed by a seeded hash of the question id, so every setup uses the same split.
Each method is fitted on half A and applied to half B, then fitted on B and applied to A, so
every question gets a recalibrated forecast from a fit that never saw it (2-fold cross-fitting).
Reported: Brier of the raw and recalibrated forecasts on all answered questions, the paired
difference (recalibrated - raw; negative = recalibration helps) with a 95% bootstrap interval,
and the fitted parameters of each half.

Probabilities are clipped to [0.005, 0.995] before taking logits, so 0/1 answers (imported
free-text results) can be fitted; for those, recalibration amounts to choosing two confidence levels.

Usage (from the repo root), same options as scoring.report:
  python3 -m analysis.recalibration --set settled settled-ext --out results/settled-all
"""

import argparse
import hashlib
import math
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from scoring.proper import mean_brier
from scoring.report import (ROOT, MIN_N, add_baselines, load, md_table, paired_brier_diff,
                            _setup_order, write_csv)

CLIP = 0.005
SPLIT_SEED = "recalibration-2026-10-16"


def logit(p: float) -> float:
    p = min(max(p, CLIP), 1 - CLIP)
    return math.log(p / (1 - p))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x)) if x >= 0 else math.exp(x) / (1 + math.exp(x))


def half(question_id: str) -> int:
    return int(hashlib.sha256(f"{SPLIT_SEED}:{question_id}".encode()).hexdigest(), 16) % 2


def fit_extremize(ps: Sequence[float], ys: Sequence[int]) -> float:
    """a minimising Brier of sigmoid(a * logit p), by golden-section search on [0.05, 6]."""
    xs = [logit(p) for p in ps]
    loss = lambda a: sum((sigmoid(a * x) - y) ** 2 for x, y in zip(xs, ys))
    lo, hi, g = 0.05, 6.0, (math.sqrt(5) - 1) / 2
    c, d = hi - g * (hi - lo), lo + g * (hi - lo)
    for _ in range(80):
        if loss(c) < loss(d):
            hi = d
        else:
            lo = c
        c, d = hi - g * (hi - lo), lo + g * (hi - lo)
    return (lo + hi) / 2


def fit_platt(ps: Sequence[float], ys: Sequence[int], ridge: float = 1e-3, iters: int = 50) -> Tuple[float, float]:
    """(alpha, beta) of a logistic regression of y on logit p, by Newton's method on log loss,
    with step halving so each step lowers the loss (plain Newton diverges on 0/1 forecasts).
    A small ridge penalty keeps it finite when the classes separate perfectly."""
    xs = [logit(p) for p in ps]

    def loss(a: float, b: float) -> float:
        total = 0.0
        for x, y in zip(xs, ys):
            z = a + b * x  # log(1 + e^z) - y z, computed stably
            total += (z if z > 0 else 0.0) + math.log1p(math.exp(-abs(z))) - y * z
        return total + ridge / 2 * (a * a + (b - 1) ** 2)

    a, b = 0.0, 1.0
    current = loss(a, b)
    for _ in range(iters):
        ga = gb = haa = hab = hbb = 0.0
        for x, y in zip(xs, ys):
            q = sigmoid(a + b * x)
            w = q * (1 - q)
            ga += q - y
            gb += (q - y) * x
            haa += w
            hab += w * x
            hbb += w * x * x
        ga, gb = ga + ridge * a, gb + ridge * (b - 1)
        haa, hbb = haa + ridge, hbb + ridge
        det = haa * hbb - hab * hab
        if det <= 1e-12:
            break
        da, db = (hbb * ga - hab * gb) / det, (haa * gb - hab * ga) / det
        step = 1.0
        while step > 1e-6 and loss(a - step * da, b - step * db) > current:
            step /= 2
        if step <= 1e-6:
            break
        a, b = a - step * da, b - step * db
        new = loss(a, b)
        if current - new < 1e-10:
            break
        current = new
    return a, b


def cross_fit(ps: Dict[str, float], outcomes: Dict[str, int]):
    """Out-of-sample recalibrated forecasts for every question in `ps`, plus the parameters per half."""
    halves = {0: [q for q in ps if half(q) == 0], 1: [q for q in ps if half(q) == 1]}
    ext, platt, params = {}, {}, {}
    for train, test in ((0, 1), (1, 0)):
        tr, te = halves[train], halves[test]
        if not tr or not te:
            return None
        a = fit_extremize([ps[q] for q in tr], [outcomes[q] for q in tr])
        alpha, beta = fit_platt([ps[q] for q in tr], [outcomes[q] for q in tr])
        params[train] = (a, alpha, beta)
        for q in te:
            ext[q] = sigmoid(a * logit(ps[q]))
            platt[q] = sigmoid(alpha + beta * logit(ps[q]))
    return ext, platt, params


def table(probs, outcomes, n_boot: int = 1000) -> List[Dict]:
    rows = []
    for setup in sorted(probs, key=_setup_order):
        ps = {q: p for q, p in probs[setup].items() if p is not None and q in outcomes}
        if len(ps) < 2 * MIN_N:  # each half needs enough questions to fit on
            continue
        res = cross_fit(ps, outcomes)
        if res is None:
            continue
        ext, platt, params = res
        qs = list(ps)
        ys = [outcomes[q] for q in qs]
        row = {"setup": setup, "n": len(qs), "brier_raw": round(mean_brier([ps[q] for q in qs], ys), 4),
               "brier_extremized": round(mean_brier([ext[q] for q in qs], ys), 4),
               "brier_platt": round(mean_brier([platt[q] for q in qs], ys), 4)}
        for name, rec in (("extremized", ext), ("platt", platt)):
            d = paired_brier_diff(rec, ps, {q: outcomes[q] for q in qs}, n_boot)
            row[f"{name}_minus_raw"], row[f"{name}_ci_low"], row[f"{name}_ci_high"] = d["mean_diff"], d["ci_low"], d["ci_high"]
        row["a_half0"], row["a_half1"] = round(params[0][0], 3), round(params[1][0], 3)
        row["platt_alpha_beta_half0"] = f"{params[0][1]:.3f}, {params[0][2]:.3f}"
        row["platt_alpha_beta_half1"] = f"{params[1][1]:.3f}, {params[1][2]:.3f}"
        rows.append(row)
    return rows


def run(args) -> None:
    outcomes, probs, members, _ = load(args.questions, args.forecasts, args.set, args.prompt_id, args.id_prefix)
    if not outcomes:
        print("No resolved questions to score yet.")
        return
    add_baselines(probs, outcomes, members=members)
    rows = table(probs, outcomes, args.bootstrap)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "recalibration.csv", rows)
    md = [f"# Post-hoc recalibration: {out.name}\n",
          "Each method is fitted on one half of the questions and tested on the other (2-fold, fixed split), "
          "so every Brier here is out of sample. `*_minus_raw` < 0 means recalibration helps, with a 95% "
          f"bootstrap interval. `a` > 1 means the setup was underconfident. Setups with fewer than {2 * MIN_N} "
          "answered questions are left out.\n", md_table(rows)]
    (out / "recalibration.md").write_text("\n".join(md))
    print(f"Saved recalibration tables to {out}/")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", nargs="+", default=[str(ROOT / "data" / "questions.csv")])
    ap.add_argument("--forecasts", nargs="+", default=[str(ROOT / "data" / "forecasts.csv")])
    ap.add_argument("--set", nargs="+", default=["all"])
    ap.add_argument("--prompt-id", default=None)
    ap.add_argument("--id-prefix", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bootstrap", type=int, default=1000)
    run(ap.parse_args())


if __name__ == "__main__":
    main()
