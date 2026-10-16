"""
merge_outcomes.py
-----------------
Brings live outcomes from spark's copy of data/questions.csv (kept current there by the
update_outcomes cron job) into the laptop's copy, without taking anything else from it.

Only `outcome` and `resolved_at` are copied, only for live questions, and only where the
laptop's value is empty. A question whose outcome differs between the two copies is reported
and left alone. Every other column and every non-live row stays exactly as on the laptop
(which has the repricing, the new sets, etc.).

Usage (from the repo root):
  python3 -m collect.merge_outcomes data/tmp/spark_questions.csv            # writes data/questions.csv
  python3 -m collect.merge_outcomes data/tmp/spark_questions.csv --dry-run
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent


def merge(local: List[Dict[str, str]], remote: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[str], List[str]]:
    """(merged rows, ids that got an outcome, ids whose outcomes disagree)."""
    theirs = {r["question_id"]: r for r in remote}
    filled, conflicts, out = [], [], []
    for r in local:
        r = dict(r)
        t = theirs.get(r["question_id"])
        if r.get("set") == "live" and t and t.get("outcome") in ("0", "1"):
            if r.get("outcome") in ("", None):
                r["outcome"], r["resolved_at"] = t["outcome"], t.get("resolved_at", "")
                filled.append(r["question_id"])
            elif r["outcome"] != t["outcome"]:
                conflicts.append(r["question_id"])
        out.append(r)
    return out, filled, conflicts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spark_questions")
    ap.add_argument("--into", default=str(ROOT / "data" / "questions.csv"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with open(args.into, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols, local = reader.fieldnames, list(reader)
    with open(args.spark_questions, newline="", encoding="utf-8") as f:
        remote = list(csv.DictReader(f))
    merged, filled, conflicts = merge(local, remote)
    print(f"{len(filled)} live questions get an outcome from spark")
    for qid in filled:
        print(f"  {qid}")
    if conflicts:
        print(f"{len(conflicts)} outcomes differ between laptop and spark (left as on the laptop): {conflicts}")
    if args.dry_run or not filled:
        sys.exit(0)
    with open(args.into, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(merged)
    print(f"Saved {args.into}")


if __name__ == "__main__":
    main()
