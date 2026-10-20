"""
ablation.py
-----------
Is the chair weighing the members' arguments, or averaging their numbers? Scores the chair
ablations (data/ablation/forecasts.csv, from forecast/rechair.py) next to the main councils,
with the same members' answers on every question. Pre-registered in docs/decisions.md (2026-10-20).

  ablation_view.csv     each variant (numbers-only, reasoning-only) vs the full council with the
                        same chair, and every view vs the mean / logit pool of the same members:
                        paired Brier difference with a 95% bootstrap interval stratified by source,
                        pooled and per source
  ablation_chair.csv    the full-view council with each member as chair: Brier on the questions
                        every full-view council answered, the chair's own Brier as a single model
                        there, and the council vs the mean pool and vs its chair alone
  ablation_shift.csv    how far each council moves from the mean pool: mean |council - mean pool|
                        and the share of questions within 0.05 of it (descriptive, no test)
  ablation.md           all three

Negative differences mean the first setup is better.

Usage (from the repo root):
  python3 -m analysis.ablation --set settled settled-ext --out results/ablation
"""

import argparse
import statistics
from pathlib import Path
from typing import Dict, List, Optional

from scoring.proper import mean_brier
from scoring.report import (ROOT, add_baselines, load, load_sources, md_table, paired_brier_diff,
                            spearman, write_csv)

VARIANTS = ("numbers-only", "reasoning-only")
POOLS = ("baseline:mean", "baseline:logit_pool")


def view_and_chair(setup: str):
    """council:chair=m -> ("full", m); council:numbers-only:chair=m -> ("numbers-only", m)."""
    head, chair = setup.split("chair=", 1)
    view = head[len("council:"):].rstrip(":") or "full"
    return view, chair


def _verdict(res: Dict) -> str:
    return ("first better" if res["ci_high"] < 0 else "first worse" if res["ci_low"] > 0 else "no clear difference")


def view_table(probs, outcomes, strata, n_boot) -> List[Dict]:
    councils = sorted(s for s in probs if s.startswith("council:"))
    full = {view_and_chair(s)[1]: s for s in councils if view_and_chair(s)[0] == "full"}
    pairs = []
    for s in councils:
        view, chair = view_and_chair(s)
        if view in VARIANTS and chair in full:
            pairs.append((s, full[chair]))
        pairs += [(s, p) for p in POOLS if p in probs]
    groups = [("all", outcomes)] + [(src, {q: y for q, y in outcomes.items() if strata.get(q) == src})
                                    for src in sorted(set(strata.get(q, "") for q in outcomes))]
    rows = []
    for a, b in pairs:
        for group, outs in groups:
            res = paired_brier_diff(probs[a], probs[b], outs, n_boot, strata=strata)
            if res:
                rows.append({"setup": a, "versus": b, "source": group, **res, "verdict": _verdict(res)})
    return rows


def chair_table(probs, outcomes, strata, n_boot) -> List[Dict]:
    full = sorted(s for s in probs if s.startswith("council:") and view_and_chair(s)[0] == "full")
    if len(full) < 2:
        return []
    common = [q for q in outcomes if all(probs[s].get(q) is not None for s in full)
              and probs.get("baseline:mean", {}).get(q) is not None]
    if len(common) < 2:
        return []
    outs = {q: outcomes[q] for q in common}
    rows = []
    for s in full:
        chair = view_and_chair(s)[1]
        own = probs.get(f"single:{chair}", {})
        row = {"council": s, "chair": chair, "n_common": len(common),
               "council_brier": round(mean_brier([probs[s][q] for q in common], [outs[q] for q in common]), 4)}
        if all(own.get(q) is not None for q in common):
            row["chair_alone_brier"] = round(mean_brier([own[q] for q in common], [outs[q] for q in common]), 4)
        for name, ref in (("vs_mean_pool", probs["baseline:mean"]), ("vs_chair_alone", own)):
            res = paired_brier_diff(probs[s], ref, outs, n_boot, strata=strata)
            if res:
                row.update({f"{name}": res["mean_diff"], f"{name}_ci_low": res["ci_low"],
                            f"{name}_ci_high": res["ci_high"]})
        rows.append(row)
    ranked = [r for r in rows if "chair_alone_brier" in r]
    if len(ranked) >= 3:
        rho = spearman([r["chair_alone_brier"] for r in ranked], [r["council_brier"] for r in ranked])
        for r in rows:
            r["spearman_chair_vs_council"] = "" if rho is None else round(rho, 3)
    return rows


def shift_table(probs, outcomes) -> List[Dict]:
    pool = probs.get("baseline:mean", {})
    rows = []
    for s in sorted(p for p in probs if p.startswith("council:")):
        gaps = [abs(probs[s][q] - pool[q]) for q in outcomes
                if probs[s].get(q) is not None and pool.get(q) is not None]
        if gaps:
            rows.append({"council": s, "n": len(gaps), "mean_abs_shift_from_mean_pool": round(statistics.fmean(gaps), 4),
                         "share_within_0.05": round(sum(g <= 0.05 for g in gaps) / len(gaps), 4)})
    return rows


def run(questions: List[str], forecasts: List[str], sets: List[str], n_boot: int):
    outcomes, probs, members, _ = load(questions, forecasts, sets)
    if not any(s.startswith("council:") and view_and_chair(s)[0] != "full" for s in probs):
        return None
    add_baselines(probs, outcomes, members=members)
    strata = load_sources(questions)
    return view_table(probs, outcomes, strata, n_boot), chair_table(probs, outcomes, strata, n_boot), \
        shift_table(probs, outcomes)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", nargs="+", default=[str(ROOT / "data" / "questions.csv")])
    ap.add_argument("--forecasts", nargs="+",
                    default=[str(ROOT / "data" / "forecasts.csv"), str(ROOT / "data" / "ablation" / "forecasts.csv")])
    ap.add_argument("--set", nargs="+", default=["settled", "settled-ext"])
    ap.add_argument("--out", default=str(ROOT / "results" / "ablation"))
    ap.add_argument("--bootstrap", type=int, default=1000)
    args = ap.parse_args()
    forecasts = [f for f in args.forecasts if Path(f).exists()]
    result = run(args.questions, forecasts, args.set, args.bootstrap)
    if not result:
        print("No chair ablation forecasts to score yet.")
        return
    views, chairs, shifts = result
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "ablation_view.csv", views)
    write_csv(out / "ablation_chair.csv", chairs)
    write_csv(out / "ablation_shift.csv", shifts)
    (out / "ablation.md").write_text("\n".join([
        f"# Chair ablations ({' + '.join(args.set)})\n",
        "Same members' answers on every question; only what the chair sees, or who chairs, changes. "
        "Paired Brier difference, first setup minus second (negative = first better), 95% bootstrap "
        "interval stratified by source.\n",
        "## What the chair sees\n", md_table(views),
        "\n## Who chairs (full view, questions every full-view council answered)\n", md_table(chairs),
        "\n## How far each council moves from the mean pool\n", md_table(shifts)]))
    print(f"Saved ablation tables to {out}/")


if __name__ == "__main__":
    main()
