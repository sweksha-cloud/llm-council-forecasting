"""The variance subset is fixed (docs/decisions.md, 2026-10-16); this fails if it, or the questions it was drawn from, change."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_variance_subset_is_200_priced_settled_questions():
    subset = list(csv.DictReader(open(ROOT / "data/variance/questions_200.csv", encoding="utf-8")))
    ids = [r["question_id"] for r in subset]
    assert len(ids) == 200 == len(set(ids))
    main = {r["question_id"]: r for r in csv.DictReader(open(ROOT / "data/questions.csv", encoding="utf-8"))}
    for r in subset:
        assert r == main[r["question_id"]]   # same row as in the main file
        # settled and priced, or dropped by the 2026-10-17 repricing (no trade 7 days before close)
        assert (r["set"] == "settled" and r["market_price"] and r["outcome"] in ("0", "1")) or r["set"] == "dropped"
    assert sum(r["set"] == "dropped" for r in subset) == 1
