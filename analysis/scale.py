"""
scale.py
--------
Does a 10x larger chair deliberate better? Scores the Llama 3.3 70B scale check
(data/scale/forecasts.csv, from scripts/queue_70b.sh) against the 8B setups on the 359 original
settled questions. Pre-registered in docs/decisions.md (2026-10-20); the 70B council vs the mean and
logit pools of its members (comparison 1) is in ablation.md, built by analysis/ablation.py.

  scale_comparisons.csv   (2) the 70B council vs each 8B-chaired council, (3) 70B alone vs the best
                          8B member and vs the mean pool, and both 70B setups vs the market: paired
                          Brier difference with a 95% bootstrap interval stratified by source,
                          pooled and per source (negative = the 70B setup is better)
  scale_self_preference.csv
                          (4) the 70B chair's weight on its own family's member (llama3.1:8b) minus
                          the mean weight the five 8B full-view chairs put on it, with a 95%
                          bootstrap interval (same fit and resampling as analysis/chair_weights.py)
  scale.md                both

Usage (from the repo root):
  python3 -m analysis.scale --out results/scale
"""

import argparse
import random
import statistics
from pathlib import Path
from typing import Dict, List

from analysis import chair_weights as cw
from scoring.report import (ROOT, add_baselines, load, load_sources, md_table, paired_brier_diff,
                            write_csv)

BIG = "llama3.3:70b"
FAMILY = "llama3.1:8b"   # the council member from the 70B model's own family
COUNCIL = f"council:chair={BIG}"
SINGLE = f"single:{BIG}"


def _verdict(res: Dict) -> str:
    return ("70B better" if res["ci_high"] < 0 else "70B worse" if res["ci_low"] > 0 else "no clear difference")


def comparisons(probs, outcomes, strata, n_boot) -> List[Dict]:
    pairs = [(COUNCIL, c) for c in sorted(probs) if c.startswith("council:chair=") and c != COUNCIL]
    pairs += [(SINGLE, "baseline:best_single"), (SINGLE, "baseline:mean"), (SINGLE, "market"), (COUNCIL, "market")]
    groups = [("all", outcomes)] + [(src, {q: y for q, y in outcomes.items() if strata.get(q) == src})
                                    for src in sorted(set(strata.get(q, "") for q in outcomes))]
    rows = []
    for a, b in pairs:
        if a not in probs or b not in probs:
            continue
        for group, outs in groups:
            res = paired_brier_diff(probs[a], probs[b], outs, n_boot, strata=strata)
            if res:
                rows.append({"setup": a, "versus": b, "source": group, **res, "verdict": _verdict(res)})
    return rows


def self_preference(decisions, sources, n_boot: int = 200, seed: int = 0) -> List[Dict]:
    if COUNCIL not in decisions:
        return []
    others = sorted(s for s in decisions if s.startswith("council:chair=") and s != COUNCIL
                    and FAMILY in decisions[s][0])
    if not others:
        return []
    shared = sorted(set.intersection(*(set(decisions[s][1]) for s in [COUNCIL] + others)))
    if len(shared) < 30:
        return []

    def weight(setup, qs):
        members, rows = decisions[setup]
        return cw.fit([rows[q] for q in qs])[members.index(FAMILY)]

    def diff(qs):
        return weight(COUNCIL, qs) - statistics.fmean(weight(s, qs) for s in others)

    rng = random.Random(seed)
    lo, hi = cw._ci([diff(cw._resample(shared, sources, rng)) for _ in range(n_boot)])
    est = diff(shared)
    return [{"chair": BIG, "own_family_member": FAMILY,
             "versus_chairs": ", ".join(s.split("chair=", 1)[1] for s in others), "n": len(shared),
             "weight": round(weight(COUNCIL, shared), 3), "own_weight_minus_others": round(est, 3),
             "ci_low": lo, "ci_high": hi,
             "verdict": ("favours own family" if lo > 0 else "favours own family less" if hi < 0
                         else "no clear difference")}]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", nargs="+", default=[str(ROOT / "data" / "questions.csv")])
    ap.add_argument("--forecasts", nargs="+",
                    default=[str(ROOT / "data" / f) for f in
                             ("forecasts.csv", "ablation/forecasts.csv", "scale/forecasts.csv")])
    ap.add_argument("--set", nargs="+", default=["settled"])
    ap.add_argument("--out", default=str(ROOT / "results" / "scale"))
    ap.add_argument("--bootstrap", type=int, default=1000)
    args = ap.parse_args()
    forecasts = [f for f in args.forecasts if Path(f).exists()]
    outcomes, probs, members, _ = load(args.questions, forecasts, args.set)
    if SINGLE not in probs and COUNCIL not in probs:
        print("No 70B forecasts to score yet.")
        return
    add_baselines(probs, outcomes, members=members)   # pools use council members only, so 70B alone is left out
    strata = load_sources(args.questions)
    comps = comparisons(probs, outcomes, strata, args.bootstrap)
    decisions, sources = cw.load_decisions(args.questions, forecasts, args.set)
    prefs = self_preference(decisions, sources)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "scale_comparisons.csv", comps)
    write_csv(out / "scale_self_preference.csv", prefs)
    (out / "scale.md").write_text("\n".join([
        f"# Scale check: Llama 3.3 70B ({' + '.join(args.set)})\n",
        "Pre-registered in docs/decisions.md (2026-10-20). Paired Brier difference, 70B setup minus the "
        "other (negative = 70B better), 95% bootstrap interval stratified by source. The 70B council vs "
        "the mean and logit pools of its members is in [ablation.md](ablation.md).\n",
        "## 70B council vs the 8B councils; 70B alone vs the best member, the mean pool and the market\n",
        md_table(comps),
        "\n## Does the 70B chair favour its own family's member?\n",
        md_table(prefs) if prefs else "_no 70B council decisions_\n"]))
    print(f"Saved scale-check tables to {out}/")


if __name__ == "__main__":
    main()
