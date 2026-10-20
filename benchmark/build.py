"""
build.py
--------
Builds the released benchmark from data/questions.csv: every backtest question (settled,
settled-ext, contamination) with its outcome, the market price, and the date the price was taken,
which is the "as of" date a forecaster should be given. Questions dropped by the data checks
(set = dropped) are left out.

  benchmark/questions_v1.csv     the benchmark
  benchmark/SHA256SUMS           checksum, so a copy can be verified

Run from the repo root:  python3 benchmark/build.py
"""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "questions.csv"
OUT = ROOT / "benchmark" / "questions_v1.csv"
SPLITS = {"settled": "settled", "settled-ext": "settled", "contamination": "contamination"}
COLUMNS = ["question_id", "split", "subset", "source", "topic", "question_text", "resolution_criteria",
           "url", "as_of", "market_price", "scheduled_close", "resolved_at", "outcome"]


def rows():
    with SRC.open(newline="", encoding="utf-8") as f:
        for q in csv.DictReader(f):
            if q.get("set") not in SPLITS:
                continue
            yield {"question_id": q["question_id"], "split": SPLITS[q["set"]], "subset": q["set"],
                   "source": q["source"], "topic": q.get("topic") or "", "question_text": q["question_text"],
                   "resolution_criteria": q.get("resolution_criteria") or "", "url": q.get("url") or "",
                   "as_of": q["price_time"], "market_price": q["market_price"],
                   "scheduled_close": q["resolution_date"], "resolved_at": q.get("resolved_at") or "",
                   "outcome": q["outcome"]}


def build() -> Path:
    out = sorted(rows(), key=lambda r: (r["split"], r["subset"], r["question_id"]))
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    (OUT.parent / "SHA256SUMS").write_text(f"{digest}  {OUT.name}\n")
    print(f"{len(out)} questions → {OUT.relative_to(ROOT)} (sha256 {digest[:12]}…)")
    return OUT


if __name__ == "__main__":
    build()
