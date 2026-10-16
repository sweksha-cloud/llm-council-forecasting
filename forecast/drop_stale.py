"""
drop_stale.py
-------------
Removes forecasts that no longer match the questions file, so a run can be resumed after
questions were repriced or dropped (docs/decisions.md, 2026-10-17). Standard library only, for spark.

A backtest forecast row is stale when its question is no longer in a backtest set (e.g. tagged
"dropped") or its market_price_at_forecast differs from the question's current market_price
(the price, and so the "as of" date the model was given, changed). Live rows are never touched.
A copy of the original file is kept next to it.

Usage (from the repo root):
  python3 -m forecast.drop_stale                 # data/forecasts.csv against data/questions.csv
  python3 -m forecast.drop_stale --dry-run
"""

import argparse
import csv
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
BACKTEST = ("settled", "settled-ext", "contamination")


def _float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def split(forecasts: List[Dict[str, str]], questions: List[Dict[str, str]]) -> Tuple[List[Dict], List[Dict]]:
    """(kept, stale) rows."""
    by_id = {q["question_id"]: q for q in questions}
    kept, stale = [], []
    for r in forecasts:
        q = by_id.get(r["question_id"])
        if q is None or q.get("set") == "live" or r.get("locked") == "True":
            kept.append(r)
            continue
        if q.get("set") not in BACKTEST:
            stale.append(r)
            continue
        old, new = _float(r.get("market_price_at_forecast")), _float(q.get("market_price"))
        (stale if old is None or new is None or abs(old - new) > 1e-9 else kept).append(r)
    return kept, stale


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--forecasts", default=str(ROOT / "data" / "forecasts.csv"))
    ap.add_argument("--questions", default=str(ROOT / "data" / "questions.csv"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    path = Path(args.forecasts)
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols, forecasts = reader.fieldnames, list(reader)
    with open(args.questions, newline="", encoding="utf-8") as f:
        questions = list(csv.DictReader(f))
    kept, stale = split(forecasts, questions)
    qs = sorted({r["question_id"] for r in stale})
    print(f"{len(stale)} stale rows on {len(qs)} questions; {len(kept)} rows kept")
    if args.dry_run or not stale:
        return
    backup = path.with_name(path.stem + "_before_drop_stale.csv")
    shutil.copy(path, backup)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(kept)
    print(f"Saved {path} (original copied to {backup}). Re-run the queue to forecast those questions again.")


if __name__ == "__main__":
    main()
