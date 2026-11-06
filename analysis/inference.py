"""
inference.py
------------
How strong is the evidence behind "no council beats the average"? Three checks on the comparisons
already reported, added 2026-11-06 (docs/decisions.md). None changes a pre-registered estimate.

  inference_family.csv   every council variant vs the mean pool of the same members (the 11 comparisons
                         in the report's chart): mean Brier difference, 95% and 90% bootstrap intervals
                         stratified by source, a two-sided bootstrap p-value, the Holm-adjusted p-value
                         across the family, and an equivalence test (TOST): "equivalent" when the 90%
                         interval lies inside +-MARGIN, the smallest difference the study was powered to
                         detect (docs/power.md). `equivalence_bound` = the smallest margin that would pass.
  inference_extremity.csv  the pre-registered market-certainty cut (analysis/robustness.py) for the two
                         main councils vs the mean pool, with Holm-adjusted p-values across those 6 tests.
  discrimination.csv     can the models forecast at all? AUROC with a 95% interval, and the paired Brier
                         difference vs the constant base-rate forecast, for each single model, the mean
                         pool, each main council and the market.
  inference.md           all three

Negative differences mean the first setup is better.

Usage (from the repo root):
  python3 -m analysis.inference --out results/inference
"""

import argparse
import random
import statistics
from pathlib import Path
from typing import Dict, List, Optional

from analysis.debate import MEAN_R2, add_debate_mean
from analysis.robustness import extremity_group
from scoring.discrimination import auroc
from scoring.proper import brier
from scoring.report import (ROOT, add_baselines, add_reference_baselines, load, load_sources, md_table,
                            reference, resample, write_csv)

MARGIN = 0.013   # Brier; the detectable difference vs the pool in docs/power.md
DATA = ROOT / "data"
MAIN = [str(DATA / "forecasts.csv")]
ABLATION = MAIN + [str(DATA / "ablation" / "forecasts.csv")]
DEBATE = MAIN + [str(DATA / "debate" / "forecasts.csv")]
SCALE = MAIN + [str(DATA / "scale" / "forecasts.csv")]
QUESTIONS = [str(DATA / "questions.csv")]


def boot_diffs(a: Dict[str, Optional[float]], b: Dict[str, Optional[float]], outcomes: Dict[str, int],
               strata: Dict[str, str], n_boot: int, seed: int = 0):
    qs = [q for q in outcomes if a.get(q) is not None and b.get(q) is not None]
    diffs = [brier(a[q], outcomes[q]) - brier(b[q], outcomes[q]) for q in qs]
    rng = random.Random(seed)
    keys = [strata.get(q, "") for q in qs]
    boots = sorted(statistics.fmean(resample(diffs, keys, rng)) for _ in range(n_boot))
    return len(qs), statistics.fmean(diffs), boots


def summarise(setup: str, versus: str, n: int, est: float, boots: List[float]) -> Dict:
    k = len(boots)
    q = lambda p: boots[min(k - 1, max(0, int(p * k)))]
    p_two = min(1.0, 2 * min(sum(b <= 0 for b in boots), sum(b >= 0 for b in boots)) / k)
    lo90, hi90 = q(0.05), q(0.95)
    return {"setup": setup, "versus": versus, "n": n, "mean_diff": round(est, 4),
            "ci95_low": round(q(0.025), 4), "ci95_high": round(boots[int(0.975 * k) - 1], 4),
            "ci90_low": round(lo90, 4), "ci90_high": round(hi90, 4), "p": round(p_two, 4),
            "equivalence_bound": round(max(abs(lo90), abs(hi90)), 4),
            "equivalent_within_margin": "yes" if -MARGIN < lo90 and hi90 < MARGIN else "no"}


def holm(rows: List[Dict]) -> None:
    """Holm-Bonferroni across the rows, in place: p_holm and the verdict at 5% family-wise error."""
    order = sorted(range(len(rows)), key=lambda i: rows[i]["p"])
    running = 0.0
    m = len(rows)
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * rows[i]["p"]))
        rows[i]["p_holm"] = round(running, 4)
    for r in rows:
        r["verdict_holm"] = ("first better" if r["p_holm"] < 0.05 and r["mean_diff"] < 0 else
                             "first worse" if r["p_holm"] < 0.05 and r["mean_diff"] > 0 else "no clear difference")


def family(n_boot: int) -> List[Dict]:
    strata = load_sources(QUESTIONS)
    rows = []
    # Five full-view chairs and the numbers-only / reasoning-only views, on settled-all.
    outcomes, probs, members, _ = load(QUESTIONS, ABLATION, ["settled", "settled-ext"])
    add_baselines(probs, outcomes, members=members)
    for s in sorted(p for p in probs if p.startswith("council:")):
        n, est, boots = boot_diffs(probs[s], reference(probs, s, "baseline:mean", members), outcomes, strata, n_boot)
        rows.append(summarise(s, "baseline:mean", n, est, boots))
    # Debate: the mean of the revised forecasts vs the round-1 mean pool, on settled.
    outcomes, probs, members, _ = load(QUESTIONS, DEBATE, ["settled"])
    add_baselines(probs, outcomes, members=members)
    add_debate_mean(probs, outcomes)
    if MEAN_R2 in probs:
        n, est, boots = boot_diffs(probs[MEAN_R2], probs["baseline:mean"], outcomes, strata, n_boot)
        rows.append(summarise(MEAN_R2, "baseline:mean", n, est, boots))
    # The 70B chair vs the mean pool of its members, on settled.
    outcomes, probs, members, _ = load(QUESTIONS, SCALE, ["settled"])
    add_baselines(probs, outcomes, members=members)
    big = "council:chair=llama3.3:70b"
    if big in probs:
        n, est, boots = boot_diffs(probs[big], reference(probs, big, "baseline:mean", members), outcomes, strata, n_boot)
        rows.append(summarise(big, "baseline:mean", n, est, boots))
    holm(rows)
    return rows


def extremity(n_boot: int) -> List[Dict]:
    strata = load_sources(QUESTIONS)
    outcomes, probs, members, market = load(QUESTIONS, MAIN, ["settled", "settled-ext"])
    add_baselines(probs, outcomes, members=members)
    groups = {q: extremity_group(market.get(q)) for q in outcomes}
    rows = []
    for s in ("council:chair=llama3.1:8b", "council:chair=qwen3:8b"):
        ref = reference(probs, s, "baseline:mean", members)
        for g in ("uncertain", "leaning", "near-certain"):
            outs = {q: y for q, y in outcomes.items() if groups.get(q) == g}
            n, est, boots = boot_diffs(probs[s], ref, outs, strata, n_boot)
            rows.append({"market": g, **summarise(s, "baseline:mean", n, est, boots)})
    holm(rows)
    return rows


def discrimination(n_boot: int, seed: int = 0) -> List[Dict]:
    strata = load_sources(QUESTIONS)
    outcomes, probs, members, _ = load(QUESTIONS, MAIN, ["settled", "settled-ext"])
    add_baselines(probs, outcomes, members=members)
    add_reference_baselines(probs, outcomes)
    members_used = sorted({m for ms in members.values() for m in ms})
    setups = ([f"single:{m}" for m in members_used] + ["baseline:mean", "council:chair=llama3.1:8b",
              "council:chair=qwen3:8b", "market"])
    rows = []
    for s in setups:
        qs = [q for q in outcomes if probs[s].get(q) is not None]
        keys = [strata.get(q, "") for q in qs]
        rng = random.Random(seed)
        boot = sorted(v for v in (auroc([probs[s][q] for q in b], [outcomes[q] for q in b])
                                  for b in (resample(qs, keys, rng) for _ in range(n_boot))) if v is not None)
        n, est, diffs = boot_diffs(probs[s], probs["baseline:base_rate"], outcomes, strata, n_boot)
        rows.append({"setup": s, "n": len(qs), "auroc": round(auroc([probs[s][q] for q in qs], [outcomes[q] for q in qs]), 4),
                     "auroc_ci_low": round(boot[int(0.025 * len(boot))], 4),
                     "auroc_ci_high": round(boot[int(0.975 * len(boot)) - 1], 4),
                     "vs_base_rate": round(est, 4), "vs_base_rate_ci_low": round(diffs[int(0.025 * len(diffs))], 4),
                     "vs_base_rate_ci_high": round(diffs[int(0.975 * len(diffs)) - 1], 4)})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "results" / "inference"))
    ap.add_argument("--bootstrap", type=int, default=2000)
    args = ap.parse_args()
    fam, ext, disc = family(args.bootstrap), extremity(args.bootstrap), discrimination(args.bootstrap)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "inference_family.csv", fam)
    write_csv(out / "inference_extremity.csv", ext)
    write_csv(out / "discrimination.csv", disc)
    (out / "inference.md").write_text("\n".join([
        "# Strength of the evidence (added 2026-11-06)\n",
        f"Brier difference, first setup minus the mean pool of the same members (negative = first better). "
        f"Bootstrap stratified by source, {args.bootstrap} resamples. Holm-adjusted p-values control the "
        f"family-wise error at 5%. Equivalent = the 90% interval lies inside +-{MARGIN} (TOST at 5%), the "
        "difference docs/power.md says the study could detect.\n",
        "## Every council variant vs the members' average\n", md_table(fam),
        "\n## By how certain the market was (pre-registered robustness cut)\n", md_table(ext),
        "\n## Can the models forecast at all?\n",
        "AUROC 0.5 = no better than chance at ranking which questions resolve Yes. `vs_base_rate` = Brier "
        "difference from always forecasting the share of Yes outcomes (negative = better than that constant).\n",
        md_table(disc)]))
    print(f"Saved inference tables to {out}/")


if __name__ == "__main__":
    main()
