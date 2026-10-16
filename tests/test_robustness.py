"""Robustness cuts, checked on fake rows."""

import csv
import json
from argparse import Namespace
from datetime import datetime, timezone

import pytest

from analysis.robustness import extremity_group, horizon_group, question_groups, run

approx = lambda x: pytest.approx(x, abs=1e-4)
utc = lambda *a: datetime(*a, tzinfo=timezone.utc)


def test_groups():
    assert horizon_group(utc(2026, 7, 1), utc(2026, 7, 8)) == "<=7 days"
    assert horizon_group(utc(2026, 7, 1), utc(2026, 7, 20)) == "8-30 days"
    assert horizon_group(utc(2026, 7, 1), utc(2026, 9, 1)) == ">30 days"
    assert horizon_group(None, utc(2026, 7, 1)) is None
    assert [extremity_group(p) for p in (0.03, 0.97, 0.10, 0.85, 0.5, 0.79)] == \
        ["near-certain", "near-certain", "leaning", "leaning", "uncertain", "uncertain"]
    assert extremity_group(None) is None


def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


@pytest.fixture
def fake(tmp_path):
    # 40 Polymarket "Sports" + 40 Kalshi "Mentions" questions; Kalshi topic is common enough to keep,
    # plus 5 "Weather" questions that must fold into Other. Outcomes alternate.
    qs, fs = [], []
    for i in range(85):
        src, topic = ("polymarket", "Sports") if i < 40 else ("kalshi", "Mentions") if i < 80 else ("kalshi", "Weather")
        y = i % 2
        qs.append({"question_id": f"q{i}", "source": src, "topic": topic, "set": "settled", "outcome": y,
                   "market_price": 0.97 if y else 0.03, "price_time": "2026-07-01T00:00:00Z",
                   "resolution_date": "2026-07-08T00:00:00Z", "resolved_at": "2026-07-08T00:00:00Z"})
        # members a, b: a always 0.6/0.4 (Brier .16), b always right-ish 0.8/0.2 (.04); council 0.7/0.3 (.09)
        for setup, p in (("single:a", 0.6), ("single:b", 0.8), ("council:chair=a", 0.7)):
            fs.append({"question_id": f"q{i}", "setup": setup, "probability": p if y else 1 - p,
                       "members": json.dumps(["a", "b"]) if setup.startswith("council") else "",
                       "prompt_id": "v2", "market_price_at_forecast": "", "forecast_at": "2026-07-01T00:00:00Z"})
    _write(tmp_path / "q.csv", qs)
    _write(tmp_path / "f.csv", fs)
    return tmp_path


def test_topic_folding_and_cuts(fake):
    outcomes = {f"q{i}": i % 2 for i in range(85)}
    market = {f"q{i}": (0.97 if i % 2 else 0.03) for i in range(85)}
    cuts = question_groups([str(fake / "q.csv")], outcomes, market, [str(fake / "f.csv")])
    assert cuts["topic"]["q81"] == "Other" and cuts["topic"]["q0"] == "Sports"
    assert set(cuts["source"].values()) == {"polymarket", "kalshi"}
    assert set(cuts["horizon"].values()) == {"<=7 days"}
    assert set(cuts["extremity"].values()) == {"near-certain"}


def test_run_by_hand(fake):
    run(Namespace(questions=[str(fake / "q.csv")], forecasts=[str(fake / "f.csv")], set=["settled"],
                  prompt_id=None, id_prefix=None, out=str(fake / "out"), bootstrap=200))
    scores = {(r["cut"], r["group"], r["setup"]): r for r in csv.DictReader(open(fake / "out" / "robustness.csv"))}
    assert float(scores[("source", "kalshi", "council:chair=a")]["brier"]) == approx(0.09)
    # market Brier .0009 everywhere -> council skill 1 - .09/.0009 = -99
    assert float(scores[("source", "polymarket", "council:chair=a")]["skill_vs_market"]) == approx(-99)
    paired = {(r["cut"], r["group"], r["versus"]): r for r in csv.DictReader(open(fake / "out" / "robustness_paired.csv"))}
    # council .09 vs mean pool of a,b (0.7/0.3 -> .09): exactly 0 ; vs best single b (.04): +.05
    assert float(paired[("source", "kalshi", "baseline:mean")]["mean_diff"]) == approx(0.0)
    assert float(paired[("source", "kalshi", "baseline:best_single")]["mean_diff"]) == approx(0.05)
    assert paired[("topic", "Other", "market")]["verdict"] == "too few (< 30)"   # 5 Weather questions
