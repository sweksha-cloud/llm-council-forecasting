"""
debate.py
---------
Does deliberating help the members themselves? Scores the round-2 forecasts from
forecast/debate.py (data/debate/forecasts.csv) next to round 1, on the same questions.
Pre-registered in docs/decisions.md (2026-10-20).

  debate_comparisons.csv   the mean of the members' revised forecasts ("debate:mean-r2") vs the mean
                           pool of their round-1 forecasts, each council, the best member and the
                           market: paired Brier difference with a 95% bootstrap interval stratified by
                           source, pooled and per source (negative = debate better)
  debate_moves.csv         per member: how much it changed (mean |r2 - r1|), Brier before and after,
                           share of questions where it moved toward the outcome, and how far the
                           members' spread shrank
  debate.md                both

Usage (from the repo root):
  python3 -m analysis.debate --set settled --out results/debate
"""

import argparse
import statistics
from pathlib import Path
from typing import Dict, List

from scoring.aggregation import mean_pool
from scoring.proper import brier, mean_brier
from scoring.report import (ROOT, add_baselines, load, load_sources, md_table, paired_brier_diff, write_csv)

MEAN_R2 = "debate:mean-r2"


def add_debate_mean(probs, outcomes) -> None:
    r2 = [s for s in probs if s.startswith("debate-r2:")]
    if len(r2) < 2:
        return
    probs[MEAN_R2] = {}
    for q in outcomes:
        ps = [probs[s].get(q) for s in r2]
        ps = [p for p in ps if p is not None]
        probs[MEAN_R2][q] = mean_pool(ps) if len(ps) >= 2 else None


def comparison_rows(probs, outcomes, strata, n_boot) -> List[Dict]:
    refs = ["baseline:mean", "baseline:best_single", "market"] + sorted(s for s in probs if s.startswith("council:"))
    groups = [("all", outcomes)] + [(src, {q: y for q, y in outcomes.items() if strata.get(q) == src})
                                    for src in sorted(set(strata.get(q, "") for q in outcomes))]
    rows = []
    for ref in (r for r in refs if r in probs):
        for group, outs in groups:
            res = paired_brier_diff(probs[MEAN_R2], probs[ref], outs, n_boot, strata=strata)
            if res:
                rows.append({"setup": MEAN_R2, "versus": ref, "source": group, **res,
                             "verdict": ("debate better" if res["ci_high"] < 0 else
                                         "debate worse" if res["ci_low"] > 0 else "no clear difference")})
    return rows


def moves_table(probs, outcomes) -> List[Dict]:
    rows = []
    for s in sorted(p for p in probs if p.startswith("debate-r2:")):
        m = s.split(":", 1)[1]
        r1 = probs.get(f"single:{m}", {})
        qs = [q for q in outcomes if probs[s].get(q) is not None and r1.get(q) is not None]
        if not qs:
            continue
        toward = [abs(probs[s][q] - outcomes[q]) < abs(r1[q] - outcomes[q]) for q in qs
                  if probs[s][q] != r1[q]]
        rows.append({"model": m, "n": len(qs),
                     "mean_abs_change": round(statistics.fmean(abs(probs[s][q] - r1[q]) for q in qs), 4),
                     "share_changed": round(len(toward) / len(qs), 4),
                     "share_moved_toward_outcome": round(sum(toward) / len(toward), 4) if toward else "",
                     "brier_r1": round(mean_brier([r1[q] for q in qs], [outcomes[q] for q in qs]), 4),
                     "brier_r2": round(mean_brier([probs[s][q] for q in qs], [outcomes[q] for q in qs]), 4)})
    return rows


def spread_row(probs, outcomes) -> Dict:
    r2 = [s for s in probs if s.startswith("debate-r2:")]
    r1 = [f"single:{s.split(':', 1)[1]}" for s in r2]
    sd = lambda setups, q: statistics.pstdev([probs[s][q] for s in setups])
    qs = [q for q in outcomes if all(probs.get(s, {}).get(q) is not None for s in r1 + r2)]
    if not qs:
        return {}
    return {"n": len(qs), "member_sd_r1": round(statistics.fmean(sd(r1, q) for q in qs), 4),
            "member_sd_r2": round(statistics.fmean(sd(r2, q) for q in qs), 4)}


def run(questions: List[str], forecasts: List[str], sets: List[str], n_boot: int):
    outcomes, probs, members, _ = load(questions, forecasts, sets)
    if not any(s.startswith("debate-r2:") for s in probs):
        return None
    add_baselines(probs, outcomes, members=members)
    add_debate_mean(probs, outcomes)
    return comparison_rows(probs, outcomes, load_sources(questions), n_boot), moves_table(probs, outcomes)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", nargs="+", default=[str(ROOT / "data" / "questions.csv")])
    ap.add_argument("--forecasts", nargs="+",
                    default=[str(ROOT / "data" / "forecasts.csv"), str(ROOT / "data" / "debate" / "forecasts.csv")])
    ap.add_argument("--set", nargs="+", default=["settled"])
    ap.add_argument("--out", default=str(ROOT / "results" / "debate"))
    ap.add_argument("--bootstrap", type=int, default=1000)
    args = ap.parse_args()
    forecasts = [f for f in args.forecasts if Path(f).exists()]
    result = run(args.questions, forecasts, args.set, args.bootstrap)
    if not result:
        print("No debate forecasts to score yet.")
        return
    comps, moves = result
    outcomes, probs, _, _ = load(args.questions, forecasts, args.set)
    spread = spread_row(probs, outcomes)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "debate_comparisons.csv", comps)
    write_csv(out / "debate_moves.csv", moves)
    (out / "debate.md").write_text("\n".join([
        f"# Debate, round 2 ({' + '.join(args.set)})\n",
        "Each member saw the others' first answers and could revise once. `debate:mean-r2` is the mean of the "
        "revised forecasts. Paired Brier difference, debate minus reference (negative = debate better), 95% "
        "bootstrap interval stratified by source.\n",
        "## Debate vs references\n", md_table(comps), "\n## How each member moved\n", md_table(moves),
        "\n## Spread between members, before and after\n", md_table([spread]) if spread else "_none_\n"]))
    print(f"Saved debate tables to {out}/")


if __name__ == "__main__":
    main()
