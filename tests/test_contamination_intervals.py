"""excess_gap is paired with the market per question and has a source-stratified interval (2026-10-20)."""

from datetime import date

import pytest

from scoring.contamination import gap_interval, split_table


def test_excess_gap_uses_the_same_questions_as_the_market():
    # q3 has no market price: it counts for the model's gap but not for excess_gap
    outcomes = {"q1": 1, "q2": 1, "q3": 1, "q4": 1, "q5": 1, "q6": 1}
    model = {"q1": 0.9, "q2": 0.9, "q3": 0.1, "q4": 0.5, "q5": 0.5, "q6": 0.5}
    market = {"q1": 0.8, "q2": 0.8, "q3": None, "q4": 0.8, "q5": 0.8, "q6": 0.8}
    when = {q: date(2023, 6, 1) for q in ("q1", "q2", "q3")} | {q: date(2025, 6, 1) for q in ("q4", "q5", "q6")}
    [row] = split_table({"single:llama3.1:8b": model, "market": market}, outcomes, when, {}, n_boot=200)
    # before (q1, q2): model 0.01 vs market 0.04 -> -0.03; after: 0.25 vs 0.04 -> +0.21
    assert row["excess_gap"] == pytest.approx(-0.03 - 0.21)
    assert row["excess_ci_low"] == row["excess_ci_high"] == row["excess_gap"]   # no spread within groups


def test_stratified_interval_keeps_the_source_mix():
    # within each source the values are constant, so a stratified interval has no width
    before, after = [0.0] * 10 + [1.0] * 10, [0.5] * 20
    kb, ka = ["kalshi"] * 10 + ["polymarket"] * 10, ["kalshi"] * 20
    assert gap_interval(before, after, 200, keys_before=kb, keys_after=ka) == (0.0, 0.0)
    lo, hi = gap_interval(before, after, 200)
    assert lo < 0 < hi
