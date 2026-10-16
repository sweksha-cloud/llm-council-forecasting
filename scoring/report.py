"""
report.py
---------
Turns forecasts + outcomes into the results tables.

For every setup (each single model, each council) and for the baselines built
from the single models (mean, median, logit pool, extremized pool, best
single) plus the market price, it reports:

  scores.csv          Brier and log score, accuracy, ECE, sharpness and AUROC; coverage (share
                      answered); scores on the common set of questions every setup
                      answered; skill vs market (on the common set, and paired on each
                      setup's own answered questions with a 95% bootstrap interval)
  ground_truth.csv    each forecast as a Yes/No call vs the outcome: confusion matrix,
                      precision, recall, F1, balanced accuracy, MCC
  contamination.csv   questions resolved before vs after each model's training cutoff
                      (only when some resolved before; see scoring/contamination.py)
  judge_vs_truth.csv  imported results only: does the LLM-judge score track being right?
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
  python3 -m scoring.report --set settled contamination --out results/backtest
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
from scoring.calibration import expected_calibration_error, murphy_decomposition, sharpness
from scoring.contamination import split_table
from scoring.classification import balanced_accuracy, confusion, f1, mcc, precision, recall
from scoring.discrimination import average_ranks, auroc
from scoring.proper import accuracy, brier, fill_abstentions, log_score, mean_brier, mean_log_score

ROOT = Path(__file__).resolve().parent.parent

Probs = Dict[str, Dict[str, Optional[float]]]  # setup -> question_id -> probability (None = abstained)

# Below this many questions a model can't be "best single", and skill vs market isn't reported:
# with a handful of questions both are noise (a market that was near-certain on 7 questions
# gives skill around -10).
MIN_N = 30


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


def _in_sets(q, which_set) -> bool:
    sets = [which_set] if isinstance(which_set, str) else list(which_set)
    return "all" in sets or q.get("set") in sets


def load(question_files, forecast_files, which_set="all", prompt_id=None, id_prefix=None):
    """Returns (outcomes, probs, members, market)."""
    outcomes, collected_price = {}, {}
    for q in _read(question_files):
        if not _in_sets(q, which_set):
            continue
        if id_prefix and not q["question_id"].startswith(id_prefix):
            continue
        if q.get("outcome") in ("0", "1"):
            outcomes[q["question_id"]] = int(q["outcome"])
            collected_price[q["question_id"]] = _float(q.get("market_price"))

    probs: Probs = defaultdict(dict)
    members: Dict[Tuple[str, str], List[str]] = {}
    forecast_price: Dict[str, float] = {}
    failed = set()  # (setup, qid) whose kept row is a failed call ("ERROR: …"); a retry replaces it
    for f in _read(forecast_files):
        qid, setup = f["question_id"], f["setup"]
        if qid not in outcomes or (prompt_id and f.get("prompt_id") != prompt_id):
            continue
        if qid in probs[setup] and (setup, qid) not in failed:
            continue  # first (locked) forecast wins
        failed.discard((setup, qid))
        if (f.get("raw_response") or "").startswith("ERROR:"):
            failed.add((setup, qid))
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


def load_resolution_dates(question_files, outcomes):
    """question_id -> date it resolved (resolved_at, else the scheduled close), for scored questions."""
    from datetime import date
    dates = {}
    for q in _read(question_files):
        when = (q.get("resolved_at") or q.get("resolution_date") or "")[:10]
        if q["question_id"] in outcomes and when:
            try:
                dates[q["question_id"]] = date.fromisoformat(when)
            except ValueError:
                pass  # e.g. Aye's "2026-28-28"
    return dates


def members_of_setups(probs: Probs, members: Dict[Tuple[str, str], List[str]]) -> Dict[str, List[str]]:
    """Model tags each council and pooled baseline is built from (for the contamination cutoff)."""
    out: Dict[str, List[str]] = {}
    for (setup, _), ms in members.items():
        out.setdefault(setup, [])
        out[setup] += [m for m in ms if m not in out[setup]]
    singles = [s.split(":", 1)[1] for s in probs if s.startswith("single:")]
    for s in probs:
        if s.startswith("baseline:") and s not in ("baseline:always_no", "baseline:base_rate", "baseline:best_single"):
            out[s] = singles
    return out


def load_judge_scores(forecast_files, outcomes, prompt_id=None) -> Dict[Tuple[str, str], float]:
    """(setup, question_id) -> LLM-judge score, for imported results that have one (first forecast wins)."""
    judges, seen = {}, set()
    for f in _read(forecast_files):
        key = (f["setup"], f["question_id"])
        if key[1] not in outcomes or (prompt_id and f.get("prompt_id") != prompt_id) or key in seen:
            continue
        seen.add(key)
        j = _float(f.get("judge_score"))
        if j is not None:
            judges[key] = j
    return judges


# ── Baselines ─────────────────────────────────────────────────────────────────

def add_reference_baselines(probs: Probs, outcomes: Dict[str, int]) -> Dict[str, str]:
    """Forecasts that know nothing about the question: always No, and the base rate."""
    if not outcomes:
        return {}
    rate = sum(outcomes.values()) / len(outcomes)
    probs["baseline:always_no"] = {q: 0.0 for q in outcomes}
    probs["baseline:base_rate"] = {q: rate for q in outcomes}
    return {"baseline:always_no": "= 0% on every question; the accuracy any setup gets just by saying No",
            "baseline:base_rate": (f"= {rate:.3f} (share resolved Yes) on every question; uses the outcomes, "
                                   "so it's slightly optimistic")}


def add_baselines(probs: Probs, outcomes: Dict[str, int], a: float = 2.0, min_n: int = MIN_N) -> Dict[str, str]:
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

    # Only models that answered at least MIN_N questions, and at least half as many as the
    # most-answering model, are eligible, so a model that answered 2 easy questions can't "win".
    answered_n = {s: sum(p is not None for p in probs[s].values()) for s in singles}
    min_n = max(min_n, max(answered_n.values()) / 2)
    best, best_score = None, None
    for s in singles:
        answered = [(p, outcomes[q]) for q, p in probs[s].items() if p is not None]
        if answered and len(answered) >= min_n:
            score = mean_brier([p for p, _ in answered], [y for _, y in answered])
            if best_score is None or score < best_score:
                best, best_score = s, score
    if not best:
        notes["baseline:best_single"] = f"not reported: no single model answered {min_n:g} or more questions"
    if best:
        probs["baseline:best_single"] = dict(probs[best])
        notes["baseline:best_single"] = (f"= {best} (lowest Brier on these same questions, "
                                         "so it's chosen in-sample and slightly optimistic)")
    return notes


# ── Scores ────────────────────────────────────────────────────────────────────

def common_questions(probs: Probs, outcomes: Dict[str, int]) -> List[str]:
    active = [s for s in probs if any(p is not None for p in probs[s].values())]
    return [q for q in outcomes if all(probs[s].get(q) is not None for s in active)]


def _round(x: Optional[float], digits: int = 4):
    return "" if x is None else round(x, digits)


def market_skill(ps: Dict[str, Optional[float]], market: Dict[str, Optional[float]], outcomes: Dict[str, int],
                 n_boot: int = 1000, seed: int = 0, min_n: int = MIN_N) -> Optional[Dict]:
    """Brier skill vs the market, 1 - Brier(setup) / Brier(market), on the questions both answered,
    with a 95% paired bootstrap interval. Positive means better than the market.
    None with fewer than min_n shared questions, or if the market was perfect on them; the interval
    is blank if some resample has a perfect market (the ratio is undefined there)."""
    qs = [q for q in outcomes if ps.get(q) is not None and market.get(q) is not None]
    if len(qs) < min_n:
        return None
    pairs = [(brier(ps[q], outcomes[q]), brier(market[q], outcomes[q])) for q in qs]
    ref = sum(m for _, m in pairs)
    if ref == 0:
        return None
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        sample = rng.choices(pairs, k=len(pairs))
        sample_ref = sum(m for _, m in sample)
        if sample_ref:
            boots.append(1 - sum(s for s, _ in sample) / sample_ref)
    boots.sort()
    row = {"n_vs_market": len(qs), "skill_vs_market_paired": round(1 - sum(s for s, _ in pairs) / ref, 4),
           "skill_ci_low": "", "skill_ci_high": ""}
    if len(boots) == n_boot:  # undefined if any resample had a perfect market, so left blank
        row["skill_ci_low"], row["skill_ci_high"] = round(boots[int(0.025 * n_boot)], 4), round(boots[int(0.975 * n_boot) - 1], 4)
    return row


def score_table(probs: Probs, outcomes: Dict[str, int], n_bins: int = 10, n_boot: int = 1000,
                min_n: int = MIN_N) -> List[Dict]:
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
            row["accuracy"] = round(accuracy(a_ps, a_ys), 4)
            row["ece"] = round(expected_calibration_error(a_ps, a_ys, n_bins), 4)
            row["sharpness"] = round(sharpness(a_ps), 4)
            row["auroc"] = _round(auroc(a_ps, a_ys))
            c = confusion(a_ps, a_ys)
            row["balanced_accuracy"] = _round(balanced_accuracy(c))
            row["mcc"] = _round(mcc(c))
            all_ps = fill_abstentions([ps.get(q) for q in outcomes])
            row["brier_abstain_0.5"] = round(mean_brier(all_ps, [outcomes[q] for q in outcomes]), 4)
        if common:
            c_ys = [outcomes[q] for q in common]
            row["common_n"] = len(common)
            row["brier_common"] = round(mean_brier([ps[q] for q in common], c_ys), 4)
            row["log_common"] = round(mean_log_score([ps[q] for q in common], c_ys), 4)
            row["accuracy_common"] = round(accuracy([ps[q] for q in common], c_ys), 4)
            row["auroc_common"] = _round(auroc([ps[q] for q in common], c_ys))
            if (setup != "market" and market and len(common) >= min_n
                    and all(market.get(q) is not None for q in common)):
                ref = mean_brier([market[q] for q in common], c_ys)
                row["skill_vs_market"] = round(1 - row["brier_common"] / ref, 4) if ref else ""
        if setup != "market" and market:
            row.update(market_skill(ps, market, outcomes, n_boot, min_n=min_n) or {})
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
    refs = [r for r in ("market", "baseline:best_single", "baseline:mean", "baseline:always_no") if r in probs]
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


# ── Ground truth ──────────────────────────────────────────────────────────────

def ground_truth_table(probs: Probs, outcomes: Dict[str, int]) -> List[Dict]:
    rows = []
    for setup in sorted(probs, key=_setup_order):
        answered = [q for q in outcomes if probs[setup].get(q) is not None]
        if not answered:
            continue
        c = confusion([probs[setup][q] for q in answered], [outcomes[q] for q in answered])
        rows.append({"setup": setup, "answered": len(answered), "yes_calls": c.tp + c.fp, "no_calls": c.tn + c.fn,
                     "no_call_0.5": c.no_call, "tp": c.tp, "fp": c.fp, "tn": c.tn, "fn": c.fn,
                     "precision": _round(precision(c)), "recall": _round(recall(c)), "f1": _round(f1(c)),
                     "balanced_accuracy": _round(balanced_accuracy(c)), "mcc": _round(mcc(c))})
    return rows


def judge_table(probs: Probs, judges: Dict[Tuple[str, str], float], outcomes: Dict[str, int]) -> List[Dict]:
    """Per setup: mean LLM-judge score when the answer was right vs wrong, and how well the judge
    score separates right from wrong answers (AUROC, 0.5 = the judge can't tell them apart)."""
    rows = []
    for setup in sorted(probs, key=_setup_order):
        right, wrong = [], []
        for q in outcomes:
            p, j = probs[setup].get(q), judges.get((setup, q))
            if p is None or j is None or p == 0.5:
                continue
            (right if (p > 0.5) == (outcomes[q] == 1) else wrong).append(j)
        if not right and not wrong:
            continue
        rows.append({"setup": setup, "n": len(right) + len(wrong), "right": len(right), "wrong": len(wrong),
                     "judge_mean_right": _round(statistics.fmean(right) if right else None, 3),
                     "judge_mean_wrong": _round(statistics.fmean(wrong) if wrong else None, 3),
                     "judge_auroc_for_right": _round(auroc(right + wrong, [1] * len(right) + [0] * len(wrong)))})
    return rows


# ── Disagreement ──────────────────────────────────────────────────────────────

def spearman(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
    if len(xs) < 3:
        return None
    rx, ry = average_ranks(xs), average_ranks(ys)
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
    notes.update(add_reference_baselines(probs, outcomes))
    scores = score_table(probs, outcomes, args.bins, args.bootstrap)
    truth = ground_truth_table(probs, outcomes)
    judged = judge_table(probs, load_judge_scores(args.forecasts, outcomes, args.prompt_id), outcomes)
    comps = comparison_table(probs, outcomes, args.bootstrap)
    decomp, bins = calibration_tables(probs, outcomes, args.bins)
    disagree = disagreement_table(probs, members, outcomes)
    contam = split_table(probs, outcomes, load_resolution_dates(args.questions, outcomes),
                         members_of_setups(probs, members), args.bootstrap)
    contam = contam if any(r["n_before"] for r in contam) else []

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in (("scores", scores), ("comparisons", comps), ("decomposition", decomp),
                       ("reliability", bins), ("disagreement", disagree), ("ground_truth", truth)):
        write_csv(out / f"{name}.csv", rows)
    if judged:
        write_csv(out / "judge_vs_truth.csv", judged)
    if contam:
        write_csv(out / "contamination.csv", contam)

    md = [f"# Results: {out.name}\n",
          f"Resolved questions scored: **{len(outcomes)}** (set: {' + '.join(args.set)}"
          + (f", prompt {args.prompt_id}" if args.prompt_id else "") + "). Lower Brier/log score is better.\n",
          "## Scores\n",
          "`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, "
          "the fair comparison. `skill_vs_market` > 0 means better than the market. "
          "`accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the "
          "market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. "
          "`sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); "
          "read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. "
          "`auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. "
          "`balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier "
          "on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval "
          "(`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. "
          "For 0/1 answers (imported free-text results) ECE and AUROC carry little information.\n",
          md_table(scores)]
    for k, v in notes.items():
        md.append(f"- `{k}` {v}\n")
    base = sum(outcomes.values()) / len(outcomes)
    md += [f"\n## Ground truth (each forecast as a Yes/No call; {base:.1%} of questions resolved Yes)\n",
           "Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that "
           "happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No "
           "recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.\n",
           md_table(truth)]
    if judged:
        md += ["\n## Does the LLM-judge score track the ground truth?\n",
               "Mean judge score (1–5) for answers that turned out right vs wrong. `judge_auroc_for_right`: "
               "chance a right answer got a higher judge score than a wrong one; 0.5 = the judge can't tell.\n",
               md_table(judged)]
    if contam:
        md += ["\n## Contamination: resolved before vs after each model's training cutoff\n",
               "`gap` = Brier before − Brier after (negative = better on questions the model might remember), "
               "with a 95% bootstrap interval. `excess_gap` subtracts the market's own before−after gap, so it "
               "allows for the older questions being easier; clearly negative points to recall. Cutoffs: "
               "`scoring/contamination.py` (stated cutoff, else release date; councils use their latest member).\n",
               md_table(contam)]
    md += ["\n## Council vs baselines (paired Brier difference, negative = council better)\n", md_table(comps),
           "\n## Murphy decomposition (Brier = reliability − resolution + uncertainty)\n",
           "Each row uses the questions that setup answered (see `n`), so rows with different `n` "
           "aren't directly comparable; compare them on `brier_common` above.\n", md_table(decomp),
           "\n## Does member disagreement predict council error?\n",
           "Positive Spearman = the council does worse when members disagree more.\n", md_table(disagree)]
    (out / "report.md").write_text("\n".join(md))
    print("\n".join(md))
    print(f"\nSaved to {out}/")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", nargs="+", default=[str(ROOT / "data" / "questions.csv")])
    ap.add_argument("--forecasts", nargs="+", default=[str(ROOT / "data" / "forecasts.csv")])
    ap.add_argument("--set", nargs="+", choices=["live", "settled", "contamination", "all"], default=["all"],
                    help="one or more question sets, e.g. --set settled contamination")
    ap.add_argument("--prompt-id", default=None, help="only forecasts made with this prompt version")
    ap.add_argument("--id-prefix", default=None, help="only questions whose id starts with this, e.g. aye-new:")
    ap.add_argument("--out", default=str(ROOT / "results" / "latest"))
    ap.add_argument("--bins", type=int, default=10)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--extremize-a", type=float, default=2.0)
    run(ap.parse_args())


if __name__ == "__main__":
    main()
