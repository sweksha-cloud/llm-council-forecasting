"""Contamination split, checked on fake rows with values worked out by hand."""

import csv
import json
from argparse import Namespace
from datetime import date

import pytest

from dashboard.build import build_dataset
from scoring.contamination import setup_cutoff, split_table
from scoring.report import run

approx = lambda x: pytest.approx(x, abs=1e-4)

# llama3.1 cutoff 2023-12-31, qwen3 2025-04-29. Two questions resolve in 2023, two in 2026.
OUTCOMES = {"q1": 1, "q2": 0, "q3": 1, "q4": 0}
RESOLVED = {"q1": date(2023, 6, 1), "q2": date(2023, 7, 1), "q3": date(2026, 8, 1), "q4": date(2026, 8, 2)}
PROBS = {
    "single:llama3.1:8b": {"q1": 0.9, "q2": 0.2, "q3": 0.6, "q4": 0.5},
    "single:qwen3:8b": {"q1": 0.5, "q2": 0.5, "q3": 0.5, "q4": 0.5},
    "council:chair=llama3.1:8b": {"q1": 0.8, "q2": 0.2, "q3": 0.7, "q4": 0.3},
    "market": {"q1": 0.6, "q2": 0.3, "q3": 0.7, "q4": 0.4},
}


def test_cutoffs():
    assert setup_cutoff("single:llama3.1:8b") == (date(2023, 12, 31), "stated cutoff")
    assert setup_cutoff("single:unknown:1b") is None
    assert setup_cutoff("market") is None
    # a council can know whatever its latest-trained member knows
    assert setup_cutoff("council:chair=x", ["llama3.1:8b", "qwen3:8b"])[0] == date(2025, 4, 29)
    assert setup_cutoff("council:chair=x", ["llama3.1:8b", "unknown:1b"]) is None


def test_split_by_hand():
    rows = {r["setup"]: r for r in split_table(
        PROBS, OUTCOMES, RESOLVED, {"council:chair=llama3.1:8b": ["llama3.1:8b", "qwen3:8b"]}, n_boot=200)}
    assert "market" not in rows
    llama = rows["single:llama3.1:8b"]
    assert (llama["n_before"], llama["n_after"]) == (2, 2)
    assert llama["brier_before"] == approx(0.025)        # (0.01 + 0.04) / 2
    assert llama["brier_after"] == approx(0.205)         # (0.16 + 0.25) / 2
    assert llama["accuracy_after"] == approx(0.75)       # right, then 0.5 counts half
    assert llama["gap"] == approx(-0.18)
    assert llama["market_brier_before"] == approx(0.125) # (0.16 + 0.09) / 2
    assert llama["market_brier_after"] == approx(0.125)  # (0.09 + 0.16) / 2
    assert llama["excess_gap"] == approx(-0.18)          # the market found both groups equally hard
    assert llama["gap_ci_low"] <= llama["gap"] <= llama["gap_ci_high"]
    assert rows["single:qwen3:8b"]["gap"] == approx(0.0)
    assert rows["council:chair=llama3.1:8b"]["basis"] == "latest member (release date)"


def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


@pytest.fixture
def fake_files(tmp_path):
    sets = {"q1": "contamination", "q2": "contamination", "q3": "settled", "q4": "settled"}
    _write(tmp_path / "q.csv", [
        {"question_id": q, "source": "polymarket", "question_text": f"Fake {q}?", "url": "", "topic": "World",
         "set": sets[q], "outcome": OUTCOMES[q], "market_price": PROBS["market"][q],
         "resolution_date": RESOLVED[q].isoformat() + "T00:00:00Z", "resolved_at": RESOLVED[q].isoformat() + "T00:00:00Z"}
        for q in OUTCOMES])
    _write(tmp_path / "f.csv", [
        {"question_id": q, "setup": s, "probability": p[q], "raw_response": json.dumps({"probability": p[q]}),
         "members": json.dumps(["llama3.1:8b", "qwen3:8b"]) if s.startswith("council:") else "",
         "prompt_id": "v2", "market_price_at_forecast": "", "origin": "this-project"}
        for s, p in PROBS.items() if s != "market" for q in OUTCOMES])
    return tmp_path


def _args(tmp_path, sets, out):
    return Namespace(questions=[str(tmp_path / "q.csv")], forecasts=[str(tmp_path / "f.csv")], set=sets,
                     prompt_id=None, id_prefix=None, out=str(tmp_path / out), bins=10, bootstrap=200, extremize_a=2.0)


def test_report_on_fake_backtest(fake_files):
    run(_args(fake_files, ["settled", "contamination"], "backtest"))
    rows = {r["setup"]: r for r in csv.DictReader(open(fake_files / "backtest" / "contamination.csv"))}
    assert float(rows["single:llama3.1:8b"]["gap"]) == approx(-0.18)
    assert "Contamination" in (fake_files / "backtest" / "report.md").read_text()

    run(_args(fake_files, ["settled"], "settled"))   # one set alone: nothing before any cutoff, no split table
    scores = {r["setup"]: r for r in csv.DictReader(open(fake_files / "settled" / "scores.csv"))}
    assert scores["market"]["answered"] == "2"
    assert not (fake_files / "settled" / "contamination.csv").exists()


def test_dashboard_builds_fake_sets(fake_files):
    for key in ("settled", "contamination"):
        ds = build_dataset({"key": key, "label": key, "who": "", "note": "", "set": key, "prefix": None,
                            "questions": str(fake_files / "q.csv"), "forecasts": str(fake_files / "f.csv")})
        assert len(ds["questions"]) == 2
        assert all(q["market"] is not None for q in ds["questions"])
        assert {s["id"] for s in ds["setups"]} == {s for s in PROBS if s != "market"}
