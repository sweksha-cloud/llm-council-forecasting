"""Debate round 2 (forecast/debate.py, analysis/debate.py; docs/decisions.md 2026-10-20)."""

import csv
import json
import sys
from pathlib import Path

import pytest

from analysis import debate as analysis
from forecast import debate, prompts
from forecast.run_forecasts import FakeBackend
from tests.test_ablation import MODELS, _main_run, _rows, _write_questions


def _debate(q, main, out, monkeypatch=None):
    sys_argv = ["debate", "--backend", "fake", "--set", "settled", "--questions", str(q),
                "--members-from", str(main), "--out", str(out)]
    if monkeypatch:
        monkeypatch.setattr(sys, "argv", sys_argv)
        debate.main()
    else:
        import subprocess
        subprocess.run([sys.executable, "-m", "forecast.debate", *sys_argv[1:]],
                       cwd=Path(__file__).resolve().parent.parent, check=True, capture_output=True)


@pytest.fixture
def files(tmp_path):
    q, main, out = tmp_path / "questions.csv", tmp_path / "forecasts.csv", tmp_path / "debate.csv"
    _write_questions(q)
    _main_run(q, main, limit=4)
    _debate(q, main, out)
    return q, main, out


def test_every_member_revises_once_on_the_councils_questions(files):
    _, main, out = files
    rows = _rows(out)
    councils = {r["question_id"]: r for r in _rows(main) if r["setup"] == "council:chair=a"}
    assert {r["setup"] for r in rows} == {f"debate-r2:{m}" for m in MODELS}
    assert {r["question_id"] for r in rows} == set(councils)
    assert len(rows) == len(councils) * len(MODELS)
    for r in rows:
        assert r["model"] == r["setup"].split(":", 1)[1]
        assert r["members"] == councils[r["question_id"]]["members"]
        assert r["market_price_at_forecast"] == councils[r["question_id"]]["market_price_at_forecast"]


def test_resumes_without_duplicates(files):
    q, main, out = files
    before = len(_rows(out))
    _debate(q, main, out)
    assert len(_rows(out)) == before


def test_member_sees_itself_and_only_the_others(tmp_path, monkeypatch):
    q, main = tmp_path / "questions.csv", tmp_path / "forecasts.csv"
    _write_questions(q)
    _main_run(q, main, limit=1)
    seen = {}

    def ask(self, model, system, user):
        seen[model] = user
        return json.dumps({"probability": 0.5, "reasoning": "x"})

    monkeypatch.setattr(FakeBackend, "ask", ask)
    _debate(q, main, tmp_path / "d.csv", monkeypatch)
    singles = {r["setup"].split(":", 1)[1]: float(r["probability"]) for r in _rows(main) if r["setup"].startswith("single:")}
    a = seen["a"]
    assert f"Your earlier forecast: probability {singles['a']:.2f}. fake answer from a" in a
    assert "fake answer from b" in a and "fake answer from c" in a
    assert a.count("Panelist") == len(MODELS) - 1          # the others only
    assert "Today's date: 2026-08-03" in a                   # as of the price date, like round 1


def test_analysis_tables(files):
    q, main, out = files
    comps, moves = analysis.run([str(q)], [str(main), str(out)], ["settled"], n_boot=50)
    pairs = {(r["setup"], r["versus"]) for r in comps}
    assert ("debate:mean-r2", "baseline:mean") in pairs
    assert ("debate:mean-r2", "market") in pairs
    assert ("debate:mean-r2", "council:chair=a") in pairs
    assert {r["model"] for r in moves} == set(MODELS)


def test_moves_by_hand():
    probs = {"single:a": {"q1": 0.2, "q2": 0.8}, "debate-r2:a": {"q1": 0.4, "q2": 0.9}}
    [row] = analysis.moves_table(probs, {"q1": 0, "q2": 1})
    assert row["n"] == 2
    assert row["mean_abs_change"] == pytest.approx(0.15)
    assert row["brier_r1"] == pytest.approx((0.04 + 0.04) / 2)
    assert row["brier_r2"] == pytest.approx((0.16 + 0.01) / 2)
    assert row["share_moved_toward_outcome"] == 0.5
