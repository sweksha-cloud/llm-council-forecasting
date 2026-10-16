"""
robustness.py
-------------
Do the main comparisons hold across kinds of question? Splits the scored questions four ways
and re-scores every setup, and the paired council comparisons, inside each group:

  source     polymarket / kalshi
  topic      the market's own category; topics with fewer than MIN_GROUP questions go in "Other"
  horizon    days from when the forecast was made (or the price was taken) to when the question
             resolved: <=7, 8-30, >30. Settled questions are asked 7 days before close, so most
             fall in "<=7"; the other groups hold questions that resolved late or were asked early.
  extremity  how sure the market was: "near-certain" (price <=5% or >=95%), "leaning" (5-20% or
             80-95%), "uncertain" (20-80%). Near-certain questions make everyone look good.

Outputs, next to the main results:
  robustness.csv            setup x cut x group: n, Brier, accuracy, skill vs market
  robustness_paired.csv     council vs mean pool / logit pool / best single / market / always No,
                            paired Brier difference with 95% bootstrap interval, per group
  robustness.md             both as tables

Groups with fewer than MIN_GROUP questions are reported with their n but without an interval.

Usage (from the repo root), with the same question/forecast/set options as scoring.report:
  python3 -m analysis.robustness --set settled settled-ext --out results/settled-all
"""

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

from scoring.proper import accuracy, mean_brier
from scoring.report import (ROOT, _read, add_baselines, add_reference_baselines, load,
                            md_table, paired_brier_diff, write_csv)

MIN_GROUP = 30
REFERENCES = ("baseline:mean", "baseline:logit_pool", "baseline:best_single", "market", "baseline:always_no")


def _date(s: str) -> Optional[datetime]:
    """Parse a date or datetime; one without a time zone (e.g. "2026-07-15") is taken as UTC."""
    try:
        dt = datetime.fromisoformat((s or "").replace("Z", "+00:00")[:25]) if s else None
    except ValueError:
        return None  # e.g. Aye's "2026-28-28"
    return dt.replace(tzinfo=timezone.utc) if dt and dt.tzinfo is None else dt


def horizon_group(asked: Optional[datetime], resolved: Optional[datetime]) -> Optional[str]:
    if not asked or not resolved:
        return None
    days = (resolved - asked).total_seconds() / 86400
    return "<=7 days" if days <= 7 else "8-30 days" if days <= 30 else ">30 days"


def extremity_group(price: Optional[float]) -> Optional[str]:
    if price is None:
        return None
    d = abs(price - 0.5)
    return "near-certain" if d >= 0.45 else "leaning" if d >= 0.30 else "uncertain"


def question_groups(question_files, outcomes: Dict[str, int], market: Dict[str, Optional[float]],
                    forecast_files) -> Dict[str, Dict[str, str]]:
    """cut -> question_id -> group label."""
    asked: Dict[str, datetime] = {}
    for f in _read(forecast_files):  # live questions: when our forecast was made
        when = _date(f.get("forecast_at"))
        if f["question_id"] in outcomes and when and f["question_id"] not in asked:
            asked[f["question_id"]] = when
    cuts: Dict[str, Dict[str, str]] = {"source": {}, "topic": {}, "horizon": {}, "extremity": {}}
    for q in _read(question_files):
        qid = q["question_id"]
        if qid not in outcomes:
            continue
        cuts["source"][qid] = q.get("source") or "unknown"
        cuts["topic"][qid] = q.get("topic") or "Uncategorized"
        # backtests are asked as of the price date; live questions when the forecast was made
        start = _date(q.get("price_time")) if q.get("set") != "live" else asked.get(qid)
        h = horizon_group(start or asked.get(qid), _date(q.get("resolved_at")) or _date(q.get("resolution_date")))
        if h:
            cuts["horizon"][qid] = h
        e = extremity_group(market.get(qid))
        if e:
            cuts["extremity"][qid] = e
    sizes: Dict[str, int] = {}
    for t in cuts["topic"].values():
        sizes[t] = sizes.get(t, 0) + 1
    cuts["topic"] = {q: (t if sizes[t] >= MIN_GROUP else "Other") for q, t in cuts["topic"].items()}
    return cuts


def tables(probs, outcomes, cuts, n_boot: int = 1000):
    scores, paired = [], []
    market = probs.get("market", {})
    councils = [s for s in probs if s.startswith("council:")]
    for cut, groups in cuts.items():
        for group in sorted(set(groups.values())):
            qs = {q for q, g in groups.items() if g == group}
            sub = {q: y for q, y in outcomes.items() if q in qs}
            for setup in sorted(probs):
                answered = [q for q in sub if probs[setup].get(q) is not None]
                if not answered:
                    continue
                ps, ys = [probs[setup][q] for q in answered], [sub[q] for q in answered]
                row = {"cut": cut, "group": group, "setup": setup, "n": len(answered),
                       "brier": round(mean_brier(ps, ys), 4), "accuracy": round(accuracy(ps, ys), 4)}
                both = [q for q in answered if market.get(q) is not None]
                if setup != "market" and len(both) >= MIN_GROUP:
                    ref = mean_brier([market[q] for q in both], [sub[q] for q in both])
                    if ref:
                        row["skill_vs_market"] = round(
                            1 - mean_brier([probs[setup][q] for q in both], [sub[q] for q in both]) / ref, 4)
                scores.append(row)
            for c in councils:
                for ref in REFERENCES:
                    if ref not in probs:
                        continue
                    shared = [q for q in sub if probs[c].get(q) is not None and probs[ref].get(q) is not None]
                    row = {"cut": cut, "group": group, "council": c, "versus": ref, "n": len(shared)}
                    if len(shared) >= MIN_GROUP:
                        res = paired_brier_diff(probs[c], probs[ref], sub, n_boot)
                        row.update({k: res[k] for k in ("mean_diff", "ci_low", "ci_high")})
                        row["verdict"] = ("council better" if res["ci_high"] < 0 else
                                          "council worse" if res["ci_low"] > 0 else "no clear difference")
                    elif shared:
                        row["verdict"] = f"too few (< {MIN_GROUP})"
                    paired.append(row)
    return scores, paired


def run(args) -> None:
    outcomes, probs, members, market = load(args.questions, args.forecasts, args.set, args.prompt_id, args.id_prefix)
    if not outcomes:
        print("No resolved questions to score yet.")
        return
    add_baselines(probs, outcomes, members=members)
    add_reference_baselines(probs, outcomes)
    cuts = question_groups(args.questions, outcomes, market, args.forecasts)
    scores, paired = tables(probs, outcomes, cuts, args.bootstrap)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "robustness.csv", scores)
    write_csv(out / "robustness_paired.csv", paired)
    md = [f"# Robustness: {out.name}\n",
          f"Each cut splits the {len(outcomes)} scored questions into groups and re-scores inside each. "
          f"Paired rows: council minus reference on the questions both answered (negative = council better), "
          f"95% bootstrap interval; groups under {MIN_GROUP} questions get no interval. "
          f"Topics with fewer than {MIN_GROUP} questions are grouped as Other.\n",
          "## Council vs references, by group\n", md_table(paired),
          "\n## Every setup, by group\n", md_table(scores)]
    (out / "robustness.md").write_text("\n".join(md))
    print(f"Saved robustness tables to {out}/")


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
