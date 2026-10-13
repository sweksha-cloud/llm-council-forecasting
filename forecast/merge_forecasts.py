"""
merge_forecasts.py
------------------
Appends forecasts from other files (e.g. copied back from spark) to the main
forecasts file, skipping any (question_id, setup, prompt_id) already there.
Existing rows are never changed, so locked forecasts stay as they were.

Usage (from the repo root):
  python3 -m forecast.merge_forecasts spark_forecasts.csv [more.csv ...] [--into data/forecasts.csv]
"""

import argparse
import csv
from pathlib import Path

from forecast.run_forecasts import append_rows, load_existing

ROOT = Path(__file__).resolve().parent.parent


def merge(sources, into: Path) -> int:
    existing = load_existing(into)
    new = []
    for src in sources:
        with open(src, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                key = (r["question_id"], r["setup"], r["prompt_id"])
                if key not in existing:
                    existing[key] = r
                    new.append(r)
    append_rows(into, new)
    return len(new)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--into", default=str(ROOT / "data" / "forecasts.csv"))
    args = ap.parse_args()
    n = merge(args.sources, Path(args.into))
    print(f"{n} new rows appended to {args.into}")


if __name__ == "__main__":
    main()
