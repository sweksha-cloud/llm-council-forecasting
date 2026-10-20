"""Fixes from the 2026-10-16 audit of the comparison code (docs/decisions.md, 2026-10-20)."""

import csv
from pathlib import Path

import pytest

from analysis import robustness
from scoring.aggregation import mean_pool
from scoring.report import by_source_table, comparison_table, load, reference, verdict


def test_pool_uses_only_the_members_that_council_saw():
    # c's call failed when the council ran on q1 and was retried later: the council saw a, b only
    probs = {"single:a": {"q1": 0.2, "q2": 0.4}, "single:b": {"q1": 0.4, "q2": 0.6},
             "single:c": {"q1": 0.9, "q2": 0.8}, "council:chair=a": {"q1": 0.3, "q2": 0.5},
             "baseline:mean": {"q1": 0.5, "q2": 0.6}}
    members = {("council:chair=a", "q1"): ["a", "b"], ("council:chair=a", "q2"): ["a", "b", "c"]}
    pool = reference(probs, "council:chair=a", "baseline:mean", members)
    assert pool["q1"] == pytest.approx(mean_pool([0.2, 0.4]))
    assert pool["q2"] == pytest.approx(mean_pool([0.4, 0.6, 0.8]))
    assert reference(probs, "council:chair=a", "baseline:mean") is probs["baseline:mean"]   # no members: as is


def test_no_interval_or_verdict_below_min_n():
    res = {"n": 5, "mean_diff": 0.39, "ci_low": 0.2, "ci_high": 0.5}
    assert verdict(res) == {"n": 5, "mean_diff": 0.39, "verdict": "too few (< 30)"}
    assert verdict({**res, "n": 30})["verdict"] == "council worse"


def _write(path: Path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def test_backtest_market_comes_from_questions_csv(tmp_path):
    q, fc = tmp_path / "q.csv", tmp_path / "f.csv"
    _write(q, [{"question_id": "s", "set": "settled", "outcome": "1", "market_price": "0.7", "resolved_at": ""},
               {"question_id": "l", "set": "live", "outcome": "1", "market_price": "0.5", "resolved_at": ""}])
    _write(fc, [{"question_id": qid, "setup": "single:a", "probability": "0.6", "raw_response": "{}",
                 "prompt_id": "v2", "members": "", "forecast_at": "2026-10-13T00:00:00Z",
                 "market_price_at_forecast": "0.9"} for qid in ("s", "l")])
    _, _, _, market = load([str(q)], [str(fc)], "all")
    assert market == {"s": 0.7, "l": 0.9}   # stale backtest row ignored; live keeps its lock-time price


def test_per_source_best_member_is_that_sources_best():
    # a is best on kalshi, b on polymarket; pooled, b wins
    outcomes = {f"k{i}": 1 for i in range(30)} | {f"p{i}": 1 for i in range(40)}
    strata = {q: ("kalshi" if q[0] == "k" else "polymarket") for q in outcomes}
    a = {q: (0.9 if q[0] == "k" else 0.5) for q in outcomes}
    b = {q: (0.6 if q[0] == "k" else 0.95) for q in outcomes}
    probs = {"single:a": a, "single:b": b, "council:chair=a": {q: 0.7 for q in outcomes}}
    members = {("council:chair=a", q): ["a", "b"] for q in outcomes}
    rows = {(r["source"], r["versus"]): r for r in by_source_table(probs, outcomes, strata, 50, members)}
    council_brier = 0.09   # (1 - 0.7)^2
    assert rows[("kalshi", "baseline:best_single")]["mean_diff"] == pytest.approx(council_brier - 0.01)
    assert rows[("polymarket", "baseline:best_single")]["mean_diff"] == pytest.approx(council_brier - 0.0025)


def test_robustness_intervals_resample_within_source():
    # within each source the difference is constant, so a stratified interval has zero width
    outcomes = {f"k{i}": 1 for i in range(30)} | {f"p{i}": 1 for i in range(30)}
    strata = {q: ("kalshi" if q[0] == "k" else "polymarket") for q in outcomes}
    probs = {"council:chair=a": {q: (0.9 if q[0] == "k" else 0.5) for q in outcomes},
             "market": {q: 0.7 for q in outcomes}}
    cuts = {"all": {q: "all" for q in outcomes}}
    [row] = robustness.tables(probs, outcomes, cuts, 200, strata)[1]
    assert row["ci_low"] == row["ci_high"] == row["mean_diff"]
    [loose] = robustness.tables(probs, outcomes, cuts, 200)[1]
    assert loose["ci_low"] < loose["ci_high"]
