"""
chair_weights.py
----------------
How does the chair combine its members? For each council setup, fits the weights w (w_m >= 0,
summing to 1) that best reproduce the chair's forecast as a weighted average of the members'
forecasts in log-odds:

    logit(chair_p) ≈ Σ_m w_m · logit(p_m)

Equal weights (1/k each) mean the chair behaves like the logit pool of its members; a large weight
on one model means it mostly follows that model. Descriptive, and needs no outcomes, so it also
runs on the live set.

  chair_weights.csv      setup × member: fitted weight with a 95% bootstrap interval (resampling
                         questions within source)
  chair_fit.csv          per setup: n, RMSE of the fitted weights and of equal weights (log-odds),
                         share of questions where the chair is closest to each member
  self_preference.csv    for a model that both chairs and sits on the panel: its weight under its own
                         chair minus its mean weight under the other chairs, with a paired interval
                         (> 0 = the chair favours its own model's answer)
  chair_weights.md       all three

Only questions where the chair and every member gave a probability are used. Probabilities are
clipped to [0.01, 0.99] before taking log-odds.

Usage (from the repo root):
  python3 -m analysis.chair_weights --set live --out results/live
  python3 -m analysis.chair_weights --set settled settled-ext \\
      --forecasts data/forecasts.csv data/ablation/forecasts.csv --out results/ablation
"""

import argparse
import csv
import json
import math
import random
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from scoring.report import ROOT, md_table, write_csv

EPS = 0.01
STEPS = 3000


def logit(p: float) -> float:
    p = min(max(p, EPS), 1 - EPS)
    return math.log(p / (1 - p))


def _float(x) -> Optional[float]:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_decisions(question_files: Sequence[str], forecast_files: Sequence[str], sets: Sequence[str]):
    """setup -> (members, {question: (chair_logit, [member logits])}), plus question -> source.
    First forecast per (question, setup) wins, as in scoring."""
    sources, keep = {}, set()
    for path in question_files:
        with open(path, newline="", encoding="utf-8") as f:
            for q in csv.DictReader(f):
                if "all" in sets or q.get("set") in sets:
                    keep.add(q["question_id"])
                    sources[q["question_id"]] = q.get("source") or ""
    first: Dict[Tuple[str, str], Dict] = {}
    for path in forecast_files:
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["question_id"] in keep and not (r.get("raw_response") or "").startswith("ERROR:"):
                    first.setdefault((r["question_id"], r["setup"]), r)
    out: Dict[str, Tuple[List[str], Dict[str, Tuple[float, List[float]]]]] = {}
    for (qid, setup), r in first.items():
        if not (setup.startswith("council:") and "chair=" in setup) or not r.get("members"):
            continue
        members = json.loads(r["members"])
        chair_p = _float(r.get("probability"))
        ps = [_float(first.get((qid, f"single:{m}"), {}).get("probability")) for m in members]
        if chair_p is None or None in ps:
            continue
        known, rows = out.setdefault(setup, (sorted(members), {}))
        if sorted(members) != known:
            continue  # a question where a member was missing at council time
        by_member = dict(zip(members, ps))
        rows[qid] = (logit(chair_p), [logit(by_member[m]) for m in known])
    return out, sources


def fit(rows: Sequence[Tuple[float, List[float]]]) -> List[float]:
    """Weights on the simplex minimising mean squared error, by exponentiated gradient on the
    k×k Gram matrix (so each step costs O(k²), whatever the number of questions)."""
    k, n = len(rows[0][1]), len(rows)
    gram = [[sum(x[i] * x[j] for _, x in rows) / n for j in range(k)] for i in range(k)]
    b = [sum(y * x[i] for y, x in rows) / n for i in range(k)]
    scale = max(max(abs(v) for v in row) for row in gram) or 1.0
    w = [1 / k] * k
    for _ in range(STEPS):
        g = [2 * (sum(gram[i][j] * w[j] for j in range(k)) - b[i]) for i in range(k)]
        w = [wi * math.exp(-0.5 * gi / scale) for wi, gi in zip(w, g)]
        total = sum(w)
        w = [wi / total for wi in w]
    return w


def rmse(rows, w) -> float:
    return math.sqrt(statistics.fmean((y - sum(a * b for a, b in zip(w, x))) ** 2 for y, x in rows))


def _resample(qids: List[str], sources: Dict[str, str], rng: random.Random) -> List[str]:
    groups: Dict[str, List[str]] = {}
    for q in qids:
        groups.setdefault(sources.get(q, ""), []).append(q)
    return [q for key in sorted(groups) for q in rng.choices(groups[key], k=len(groups[key]))]


def _ci(values: List[float]) -> Tuple[float, float]:
    v = sorted(values)
    return round(v[int(0.025 * len(v))], 3), round(v[int(0.975 * len(v)) - 1], 3)


def tables(decisions, sources, n_boot: int = 200, seed: int = 0):
    rng = random.Random(seed)
    weights, fits, prefs = [], [], []
    fitted: Dict[str, Dict[str, float]] = {}
    for setup in sorted(decisions):
        members, rows = decisions[setup]
        if len(rows) < 30:
            continue
        qids = sorted(rows)
        w = fit([rows[q] for q in qids])
        boots = [fit([rows[q] for q in _resample(qids, sources, rng)]) for _ in range(n_boot)]
        fitted[setup] = dict(zip(members, w))
        for i, m in enumerate(members):
            lo, hi = _ci([b[i] for b in boots])
            weights.append({"setup": setup, "member": m, "n": len(qids), "weight": round(w[i], 3),
                            "ci_low": lo, "ci_high": hi, "equal_weight": round(1 / len(members), 3)})
        nearest = [min(range(len(members)), key=lambda i: abs(rows[q][1][i] - rows[q][0])) for q in qids]
        fits.append({"setup": setup, "n": len(qids),
                     "rmse_fitted": round(rmse(rows.values(), w), 3),
                     "rmse_equal_weights": round(rmse(rows.values(), [1 / len(members)] * len(members)), 3),
                     **{f"nearest_{m}": round(nearest.count(i) / len(qids), 3) for i, m in enumerate(members)}})

    # Self-preference: paired on the questions every full-view chair answered
    full = {s.split("chair=", 1)[1]: s for s in fitted if s.startswith("council:chair=")}
    for chair, setup in sorted(full.items()):
        others = [s for c, s in full.items() if c != chair]
        members = decisions[setup][0]
        if chair not in members or not others:
            continue
        shared = sorted(set.intersection(*(set(decisions[s][1]) for s in [setup] + others)))
        if len(shared) < 30:
            continue
        i = members.index(chair)

        def diff(qs):
            own = fit([decisions[setup][1][q] for q in qs])[i]
            return own - statistics.fmean(fit([decisions[s][1][q] for q in qs])[i] for s in others)

        est = diff(shared)
        lo, hi = _ci([diff(_resample(shared, sources, rng)) for _ in range(n_boot)])
        prefs.append({"chair": chair, "versus_chairs": ", ".join(sorted(c for c in full if c != chair)),
                      "n": len(shared), "own_weight_minus_others": round(est, 3), "ci_low": lo, "ci_high": hi,
                      "verdict": ("favours own model" if lo > 0 else "favours own model less" if hi < 0
                                  else "no clear difference")})
    return weights, fits, prefs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", nargs="+", default=[str(ROOT / "data" / "questions.csv")])
    ap.add_argument("--forecasts", nargs="+", default=[str(ROOT / "data" / "forecasts.csv")])
    ap.add_argument("--set", nargs="+", default=["live"])
    ap.add_argument("--out", default=str(ROOT / "results" / "live"))
    ap.add_argument("--bootstrap", type=int, default=200)
    args = ap.parse_args()
    decisions, sources = load_decisions(args.questions, [f for f in args.forecasts if Path(f).exists()], args.set)
    weights, fits, prefs = tables(decisions, sources, args.bootstrap)
    if not weights:
        print("No council decisions to fit yet.")
        return
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "chair_weights.csv", weights)
    write_csv(out / "chair_fit.csv", fits)
    write_csv(out / "self_preference.csv", prefs)
    (out / "chair_weights.md").write_text("\n".join([
        f"# How the chair combines its members ({' + '.join(args.set)})\n",
        "Weights (≥ 0, sum 1) that best reproduce the chair's forecast as a weighted average of the members' "
        "forecasts in log-odds; equal weights = the logit pool. 95% bootstrap intervals resample questions "
        "within source. Descriptive; uses no outcomes.\n",
        "## Weights\n", md_table(weights), "\n## Fit, and which member the chair lands closest to\n", md_table(fits),
        "\n## Does a chair favour its own model?\n", md_table(prefs) if prefs else "_needs a model that both chairs and sits on the panel, and another chair_\n"]))
    print(f"Saved chair weights to {out}/")


if __name__ == "__main__":
    main()
