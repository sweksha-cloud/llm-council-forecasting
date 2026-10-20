"""benchmark/questions_v1.csv matches data/questions.csv and its checksum."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "benchmark" / "questions_v1.csv"


def test_benchmark_matches_the_data():
    q = {r["question_id"]: r for r in csv.DictReader(open(ROOT / "data" / "questions.csv", encoding="utf-8"))}
    rows = list(csv.DictReader(open(BENCH, encoding="utf-8")))
    assert len(rows) == len({r["question_id"] for r in rows}) == 1185
    assert sum(r["split"] == "settled" for r in rows) == 1039
    for r in rows:
        src = q[r["question_id"]]
        assert src["set"] == r["subset"] != "dropped"
        assert (r["market_price"], r["as_of"], r["outcome"]) == (src["market_price"], src["price_time"], src["outcome"])
        assert r["outcome"] in ("0", "1") and r["as_of"] < (r["resolved_at"] or "9999")


def test_checksum():
    digest, name = (ROOT / "benchmark" / "SHA256SUMS").read_text().split()
    assert name == BENCH.name and hashlib.sha256(BENCH.read_bytes()).hexdigest() == digest
