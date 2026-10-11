"""
report.py
---------
Turns forecasts + outcomes into the results tables.

For every setup (each single model, each council) and for the baselines built
from the single models (mean, median, logit pool, extremized pool, best
single) plus the market price, it reports:

  scores.csv          Brier and log score; coverage (share answered); scores on the
                      common set of questions every setup answered; skill vs market
  comparisons.csv     paired Brier differences (council vs market / best single / mean)
                      with 95% bootstrap intervals
  decomposition.csv   Murphy decomposition (reliability, resolution, uncertainty)
  reliability.csv     reliability-diagram data (one row per setup × bin)
  disagreement.csv    does member spread predict the council's error?
  report.md           all of the above as readable tables

Only questions with a known outcome are scored. Abstentions are never turned
into numbers silently: "answered" scores use answered questions only, and
`brier_abstain_0.5` shows the effect of counting each abstention as 0.5.

Usage (from the repo root):
  python3 -m scoring.report --set live --out results/live
  python3 -m scoring.report --questions data/imported/aye-2026/questions.csv \\
      --forecasts data/imported/aye-2026/forecasts.csv --id-prefix aye-new: --out results/aye-2026-new
"""

import argparse
import csv
import json
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from scoring.aggregation import extremized_pool, logit_pool, mean_pool, median_pool
from scoring.calibration import murphy_decomposition
from scoring.proper import brier, fill_abstentions, log_score, mean_brier, mean_log_score

ROOT = Path(__file__).resolve().parent.parent

Probs = Dict[str, Dict[str, Optional[float]]]  # setup -> question_id -> probability (None = abstained)


# ── Loading ───────────────────────────────────────────────────────────────────

def _read(paths: Sequence[str]) -> List[Dict[str, str]]:
    rows = []
    for p in paths:
        with open(p, newline="", encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))
    return rows


def _float(x) -> Optional[float]:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(question_files, forecast_files, which_set="all", prompt_id=None, id_prefix=None):
    """Returns (outcomes, probs, members, market)."""
    outcomes, collected_price = {}, {}
    for q in _read(question_files):
        if which_set != "all" and q.get("set") != which_set:
            continue
        if id_prefix and not q["question_id"].startswith(id_prefix):
            continue
        if q.get("outcome") in ("0", "1"):
            outcomes[q["question_id"]] = int(q["outcome"])
            collected_price[q["question_id"]] = _float(q.get("market_price"))

    probs: Probs = defaultdict(dict)
    members: Dict[Tuple[str, str], List[str]] = {}
    forecast_price: Dict[str, float] = {}
    for f in _read(forecast_files):
        qid, setup = f["question_id"], f["setup"]
        if qid not in outcomes or (prompt_id and f.get("prompt_id") != prompt_id):
            continue
        if qid in probs[setup]:
            continue  # first (locked) forecast wins
        probs[setup][qid] = _float(f.get("probability"))
        if f.get("members"):
            members[(setup, qid)] = json.loads(f["members"])
        price = _float(f.get("market_price_at_forecast"))
        if price is not None and qid not in forecast_price:
            forecast_price[qid] = price

    # Market baseline: price at forecast time if recorded, else the price recorded with the question
    market = {qid: forecast_price.get(qid, collected_price.get(qid)) for qid in outcomes}
    if any(p is not None for p in market.values()):
        probs["market"] = market
    return outcomes, dict(probs), members, market


# ── Baselines ─────────────────────────────────────────────────────────────────

def add_baselines(probs: Probs, outcomes: Dict[str, int], a: float = 2.0) -> Dict[str, str]:
    """Adds baseline:* setups built from the single models. Returns notes about them."""
    singles = [s for s in probs if s.startswith("single:")]
    notes = {}
    if len(singles) < 2:
        return notes
    pools = {"baseline:mean": mean_pool, "baseline:median": median_pool,
             "baseline:logit_pool": logit_pool,
             f"baseline:extremized(a={a:g})": lambda ps: extremized_pool(ps, a)}
    for name in pools:
        probs[name] = {}
    for qid in outcomes:
        ps = [probs[s].get(qid) for s in singles]
        ps = [p for p in ps if p is not None]
        for name, fn in pools.items():
            probs[name][qid] = fn(ps) if len(ps) >= 2 else None

    # Only models that answered at least half as many questions as the most-answering
    # model are eligible, so a model that answered 2 easy questions can't "win".
    answered_n = {s: sum(p is not None for p in probs[s].values()) for s in singles}
    min_n = max(answered_n.values()) / 2
    best, best_score = None, None
    for s in singles:
        answered = [(p, outcomes[q]) for q, p in probs[s].items() if p is not None]
        if answered and len(answered) >= min_n:
            score = mean_brier([p for p, _ in answered], [y for _, y in answered])
            if best_score is None or score < best_score:
                best, best_score = s, score
    if best:
        probs["baseline:best_single"] = dict(probs[best])
        notes["baseline:best_single"] = (f"= {best} (lowest Brier on these same questions, "
                                         "so it's chosen in-sample and slightly optimistic)")
    return notes


# ── Scores ────────────────────────────────────────────────────────────────────

def common_questions(probs: Probs, outcomes: Dict[str, int]) -> List[str]:
    active = [s for s in probs if any(p is not None for p in probs[s].values())]
    return [q for q in outcomes if all(probs[s].get(q) is not None for s in active)]


def score_table(probs: Probs, outcomes: Dict[str, int]) -> List[Dict]:
    common = common_questions(probs, outcomes)
    market = probs.get("market", {})
    rows = []
    for setup in sorted(probs, key=_setup_order):
        ps = probs[setup]
        answered = [q for q in outcomes if ps.get(q) is not None]
        row = {"setup": setup, "questions": len(outcomes), "answered": len(answered),
               "coverage": round(len(answered) / len(outcomes), 3) if outcomes else 0}
        if answered:
            a_ps, a_ys = [ps[q] for q in answered], [outcomes[q] for q in answered]
            row["brier"] = round(mean_brier(a_ps, a_ys), 4)
            row["log_score"] = round(mean_log_score(a_ps, a_ys), 4)
            all_ps = fill_abstentions([ps.get(q) for q in outcomes])
            row["brier_abstain_0.5"] = round(mean_brier(all_ps, [outcomes[q] for q in outcomes]), 4)
        if common:
            c_ys = [outcomes[q] for q in common]
            row["common_n"] = len(common)
            row["brier_common"] = round(mean_brier([ps[q] for q in common], c_ys), 4)
            row["log_common"] = round(mean_log_score([ps[q] for q in common], c_ys), 4)
            if setup != "market" and market and all(market.get(q) is not None for q in common):
                ref = mean_brier([market[q] for q in common], c_ys)
                row["skill_vs_market"] = round(1 - row["brier_common"] / ref, 4) if ref else ""
        rows.append(row)
    return rows


def _setup_order(s: str) -> Tuple[int, str]:
    for i, prefix in enumerate(("council:", "single:", "baseline:", "market")):
        if s.startswith(prefix):
            return i, s
    return 9, s


# ── Paired comparisons ────────────────────────────────────────────────────────

def paired_brier_diff(a: Dict[str, Optional[float]], b: Dict[str, Optional[float]],
                      outcomes: Dict[str, int], n_boot: int = 1000, seed: int = 0) -> Optional[Dict]:
    """Mean of Brier(a) - Brier(b) on questions both answered, with a 95% bootstrap interval.
    Negative means `a` is better."""
    qs = [q for q in outcomes if a.get(q) is not None and b.get(q) is not None]
    if len(qs) < 2:
        return None
    diffs = [brier(a[q], outcomes[q]) - brier(b[q], outcomes[q]) for q in qs]
    rng = random.Random(seed)
    boots = sorted(statistics.fmean(rng.choices(diffs, k=len(diffs))) for _ in range(n_boot))
    return {"n": len(qs), "mean_diff": round(statistics.fmean(diffs), 4),
            "ci_low": round(boots[int(0.025 * n_boot)], 4), "ci_high": round(boots[int(0.975 * n_boot) - 1], 4)}


def comparison_table(probs: Probs, outcomes: Dict[str, int], n_boot: int) -> List[Dict]:
    councils = [s for s in probs if s.startswith("council:")]
    refs = [r for r in ("market", "baseline:best_single", "baseline:mean") if r in probs]
    rows = []
    for c in councils:
        for r in refs:
            res = paired_brier_diff(probs[c], probs[r], outcomes, n_boot)
            if res:
                verdict = ("council better" if res["ci_high"] < 0 else
                           "council worse" if res["ci_low"] > 0 else "no clear difference")
                rows.append({"council": c, "versus": r, **res, "verdict": verdict})
    return rows


# ── Calibration ───────────────────────────────────────────────────────────────

def calibration_tables(probs: Probs, outcomes: Dict[str, int], n_bins: int):
    decomp, bins = [], []
    for setup in sorted(probs, key=_setup_order):
        answered = [q for q in outcomes if probs[setup].get(q) is not None]
        if len(answered) < 2:
            continue
        d = murphy_decomposition([probs[setup][q] for q in answered], [outcomes[q] for q in answered], n_bins)
        decomp.append({"setup": setup, "n": len(answered), "reliability": round(d.reliability, 4),
                       "resolution": round(d.resolution, 4), "uncertainty": round(d.uncertainty, 4),
                       "brier": round(d.brier, 4)})
        for b in d.bins:
            bins.append({"setup": setup, "bin": f"{b.lower:.1f}-{b.upper:.1f}", "count": b.count,
                         "mean_forecast": round(b.mean_forecast, 4), "observed_rate": round(b.observed_rate, 4)})
    return decomp, bins


# ── Disagreement ──────────────────────────────────────────────────────────────

def _ranks(xs: Sequence[float]) -> List[float]:
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


def spearman(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
    if len(xs) < 3:
        return None
    rx, ry = _ranks(xs), _ranks(ys)
    if statistics.pstdev(rx) == 0 or statistics.pstdev(ry) == 0:
        return None
    return statistics.correlation(rx, ry)


def disagreement_table(probs: Probs, members: Dict[Tuple[str, str], List[str]],
                       outcomes: Dict[str, int]) -> List[Dict]:
    rows = []
    for c in (s for s in probs if s.startswith("council:")):
        spreads, errors = [], []
        for q in outcomes:
            if probs[c].get(q) is None:
                continue
            ps = [probs.get(f"single:{m}", {}).get(q) for m in members.get((c, q), [])]
            ps = [p for p in ps if p is not None]
            if len(ps) >= 2:
                spreads.append(statistics.pstdev(ps))
                errors.append(brier(probs[c][q], outcomes[q]))
        if len(spreads) < 3:
            continue
        row = {"council": c, "n": len(spreads), "spearman_spread_vs_brier": spearman(spreads, errors)}
        order = sorted(range(len(spreads)), key=lambda i: spreads[i])
        thirds = [order[: len(order) // 3], order[len(order) // 3: 2 * len(order) // 3], order[2 * len(order) // 3:]]
        for name, idx in zip(("low", "mid", "high"), thirds):
            row[f"brier_{name}_spread"] = round(statistics.fmean(errors[i] for i in idx), 4) if idx else ""
        if row["spearman_spread_vs_brier"] is not None:
            row["spearman_spread_vs_brier"] = round(row["spearman_spread_vs_brier"], 4)
        rows.append(row)
    return rows


# ── Output ────────────────────────────────────────────────────────────────────

def write_csv(path: Path, rows: List[Dict]) -> None:
    if not rows:
        path.write_text("")
        return
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def md_table(rows: List[Dict]) -> str:
    if not rows:
        return "_none_\n"
    cols = list(dict.fromkeys(k for r in rows for k in r))
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows]
    return "\n".join(out) + "\n"


def run(args) -> None:
    outcomes, probs, members, _ = load(args.questions, args.forecasts, args.set, args.prompt_id, args.id_prefix)
    if not outcomes:
        print("No resolved questions to score yet.")
        return
    notes = add_baselines(probs, outcomes, args.extremize_a)
    scores = score_table(probs, outcomes)
    comps = comparison_table(probs, outcomes, args.bootstrap)
    decomp, bins = calibration_tables(probs, outcomes, args.bins)
    disagree = disagreement_table(probs, members, outcomes)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in (("scores", scores), ("comparisons", comps), ("decomposition", decomp),
                       ("reliability", bins), ("disagreement", disagree)):
        write_csv(out / f"{name}.csv", rows)

    md = [f"# Results: {out.name}\n",
          f"Resolved questions scored: **{len(outcomes)}** (set: {args.set}"
          + (f", prompt {args.prompt_id}" if args.prompt_id else "") + "). Lower Brier/log score is better.\n",
          "## Scores\n",
          "`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, "
          "the fair comparison. `skill_vs_market` > 0 means better than the market.\n",
          md_table(scores)]
    for k, v in notes.items():
        md.append(f"- `{k}` {v}\n")
    md += ["\n## Council vs baselines (paired Brier difference, negative = council better)\n", md_table(comps),
           "\n## Murphy decomposition (Brier = reliability − resolution + uncertainty)\n", md_table(decomp),
           "\n## Does member disagreement predict council error?\n",
           "Positive Spearman = the council does worse when members disagree more.\n", md_table(disagree)]
    (out / "report.md").write_text("\n".join(md))
    print("\n".join(md))
    print(f"\nSaved to {out}/")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", nargs="+", default=[str(ROOT / "data" / "questions.csv")])
    ap.add_argument("--forecasts", nargs="+", default=[str(ROOT / "data" / "forecasts.csv")])
    ap.add_argument("--set", choices=["live", "settled", "contamination", "all"], default="all")
    ap.add_argument("--prompt-id", default=None, help="only forecasts made with this prompt version")
    ap.add_argument("--id-prefix", default=None, help="only questions whose id starts with this, e.g. aye-new:")
    ap.add_argument("--out", default=str(ROOT / "results" / "latest"))
    ap.add_argument("--bins", type=int, default=10)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--extremize-a", type=float, default=2.0)
    run(ap.parse_args())


if __name__ == "__main__":
    main()
