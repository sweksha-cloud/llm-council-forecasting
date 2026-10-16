"""
variance.py
-----------
Do the results survive resampling? Scores the variance runs (data/variance/seed*.csv: the same
models and councils on the fixed 200-question subset, temperature 0.7, one file per seed) next to
the main temperature-0 run on the same questions, using the same code as scoring/report.py.

  variance_setups.csv     each setup's Brier on the subset, per run, with the mean and spread across seeds
  variance_paired.csv     each pre-registered council comparison (mean pool, logit pool, best member,
                          market, always No): the paired Brier difference per run, and in how many
                          seeds its sign matches the temperature-0 run

Usage (from the repo root):
  python3 -m analysis.variance --out results/variance
"""

import argparse
import statistics
from pathlib import Path
from typing import Dict, List, Optional

from scoring.proper import mean_brier
from scoring.report import (ROOT, add_baselines, add_reference_baselines, comparison_table, load,
                            md_table, write_csv)

SUBSET = ROOT / "data" / "variance" / "questions_200.csv"
ORDER = ["baseline:mean", "baseline:logit_pool", "baseline:best_single", "market", "baseline:always_no"]


def score_run(questions: Path, forecasts: List[Path], n_boot: int):
    outcomes, probs, members, _ = load([str(questions)], [str(f) for f in forecasts], which_set=["settled"])
    if not outcomes or not any(s.startswith("council:") for s in probs):
        return None
    add_baselines(probs, outcomes, members=members)
    add_reference_baselines(probs, outcomes)
    briers = {}
    for s, ps in probs.items():
        qs = [q for q in outcomes if ps.get(q) is not None]
        if qs:
            briers[s] = mean_brier([ps[q] for q in qs], [outcomes[q] for q in qs])
    comps = {(r["council"], r["versus"]): r["mean_diff"] for r in comparison_table(probs, outcomes, n_boot)}
    return briers, comps


def tables(runs: Dict[str, Optional[tuple]]):
    """runs: label -> score_run result; "T=0" is the main run, the others are seeds."""
    runs = {k: v for k, v in runs.items() if v}
    seeds = [k for k in runs if k != "T=0"]
    setups, paired = [], []
    for s in sorted({s for b, _ in runs.values() for s in b}):
        row = {"setup": s, **{k: round(v[0][s], 4) for k, v in runs.items() if s in v[0]}}
        vals = [runs[k][0][s] for k in seeds if s in runs[k][0]]
        if len(vals) >= 2:
            row["seed_mean"], row["seed_sd"] = round(statistics.fmean(vals), 4), round(statistics.stdev(vals), 4)
        setups.append(row)
    keys = sorted({k for _, c in runs.values() for k in c}, key=lambda k: (k[0], ORDER.index(k[1]) if k[1] in ORDER else 9))
    for council, ref in keys:
        row = {"council": council, "versus": ref, **{k: v[1][(council, ref)] for k, v in runs.items() if (council, ref) in v[1]}}
        base = row.get("T=0")
        vals = [row[k] for k in seeds if k in row]
        if vals:
            row["seed_mean"] = round(statistics.fmean(vals), 4)
            if base is not None:
                row["same_sign_as_T0"] = f"{sum((v < 0) == (base < 0) for v in vals)} of {len(vals)}"
        paired.append(row)
    return setups, paired


def collect_runs(main_forecasts: Path, variance_dir: Path, n_boot: int):
    runs = {"T=0": score_run(SUBSET, [main_forecasts], n_boot) if main_forecasts.exists() else None}
    for f in sorted(variance_dir.glob("seed*.csv")):
        runs[f"seed {f.stem[4:]}"] = score_run(SUBSET, [f], n_boot)
    return runs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--forecasts", default=str(ROOT / "data" / "forecasts.csv"), help="the main (temperature 0) run")
    ap.add_argument("--variance-dir", default=str(ROOT / "data" / "variance"))
    ap.add_argument("--out", default=str(ROOT / "results" / "variance"))
    ap.add_argument("--bootstrap", type=int, default=200)
    args = ap.parse_args()
    setups, paired = tables(collect_runs(Path(args.forecasts), Path(args.variance_dir), args.bootstrap))
    if not paired:
        print("No variance runs to score yet.")
        return
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "variance_setups.csv", setups)
    write_csv(out / "variance_paired.csv", paired)
    (out / "variance.md").write_text("\n".join([
        "# Variance across seeds (temperature 0.7, fixed 200-question subset)\n",
        "`T=0` is the main run on the same questions. Paired rows: council minus reference (negative = council better).\n",
        "## Council comparisons per run\n", md_table(paired), "\n## Brier per setup and run\n", md_table(setups)]))
    print(f"Saved variance tables to {out}/")


if __name__ == "__main__":
    main()
