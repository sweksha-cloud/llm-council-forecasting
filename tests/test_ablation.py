"""Chair ablations (forecast/rechair.py, analysis/ablation.py; docs/decisions.md 2026-10-20)."""

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from analysis import ablation
from forecast import prompts, rechair
from forecast.run_forecasts import FakeBackend

ROOT = Path(__file__).resolve().parent.parent
MODELS = ["a", "b", "c"]


@pytest.mark.parametrize("text, expected", [
    ("I put it at 0.7.", "I put it at [number withheld]."),
    ("About 70% likely, maybe 70 percent.", "About [number withheld] likely, maybe [number withheld]."),
    ("odds of .35, or 1.0", "odds of [number withheld], or [number withheld]"),
    ("3.5 million voters in 2026 after 3 debates", "3.5 million voters in 2026 after 3 debates"),  # not probabilities
    ("Polls show 52.5% support", "Polls show [number withheld] support"),
])
def test_redact_numbers(text, expected):
    assert prompts.redact_numbers(text) == expected


def test_views_show_only_their_half():
    answers = [(0.31, "Base rate is low, about 0.3."), (0.8, "Strong momentum.")]
    numbers = prompts.member_numbers_text(answers)
    assert numbers == "Panelist A: probability 0.31.\nPanelist B: probability 0.80."
    reasoning = prompts.member_reasoning_text(answers)
    assert "0.31" not in reasoning and "0.80" not in reasoning and "0.3" not in reasoning
    assert reasoning == "Panelist A: Base rate is low, about [number withheld].\nPanelist B: Strong momentum."
    assert prompts.member_reasoning_text([(0.5, ""), (0.4, " ")]).count("(no reasoning given)") == 2


def test_view_and_chair():
    assert ablation.view_and_chair("council:chair=llama3.1:8b") == ("full", "llama3.1:8b")
    assert ablation.view_and_chair("council:numbers-only:chair=qwen3:8b") == ("numbers-only", "qwen3:8b")
    assert rechair.setup_name("full", "x") == "council:chair=x"
    assert rechair.setup_name("reasoning-only", "x") == "council:reasoning-only:chair=x"


# ── End to end, with the fake backend ─────────────────────────────────────────

def _write_questions(path: Path) -> None:
    cols = ["question_id", "source", "question_text", "resolution_criteria", "set", "resolution_date",
            "price_time", "market_price", "outcome"]
    rows = [{"question_id": f"test:{i}", "source": "polymarket" if i % 2 else "kalshi",
             "question_text": f"Will event {i} happen?", "resolution_criteria": "Resolves Yes if it happens.",
             "set": "settled", "resolution_date": "2026-08-10T00:00:00Z", "price_time": "2026-08-03T00:00:00Z",
             "market_price": "0.3", "outcome": str(i % 2)} for i in range(6)]
    rows.append({**rows[0], "question_id": "test:live", "set": "live", "resolution_date": "2099-01-01T00:00:00Z"})
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _main_run(questions: Path, out: Path, limit: int = 0) -> None:
    cmd = [sys.executable, "-m", "forecast.run_forecasts", "--backend", "fake", "--set", "settled",
           "--questions", str(questions), "--out", str(out), "--models", *MODELS, "--chairmen", "a"]
    subprocess.run(cmd + (["--limit", str(limit)] if limit else []), cwd=ROOT, check=True, capture_output=True)


def _rechair(questions: Path, members: Path, out: Path) -> None:
    subprocess.run([sys.executable, "-m", "forecast.rechair", "--backend", "fake", "--set", "settled",
                    "--questions", str(questions), "--members-from", str(members), "--out", str(out),
                    "--chairmen", "a", "--full-chairmen", "b"],
                   cwd=ROOT, check=True, capture_output=True)


def _rows(path: Path):
    return list(csv.DictReader(path.open(newline="", encoding="utf-8")))


@pytest.fixture
def run_files(tmp_path):
    q, main, abl = tmp_path / "questions.csv", tmp_path / "forecasts.csv", tmp_path / "ablation.csv"
    _write_questions(q)
    _main_run(q, main, limit=4)   # questions 4 and 5 have no main council yet
    _rechair(q, main, abl)
    return q, main, abl


def test_rechair_reuses_the_main_councils_members(run_files):
    _, main, abl = run_files
    main_rows, rows = _rows(main), _rows(abl)
    councils = {r["question_id"]: r for r in main_rows if r["setup"] == "council:chair=a"}
    assert {r["setup"] for r in rows} == {"council:numbers-only:chair=a", "council:reasoning-only:chair=a",
                                          "council:chair=b"}
    assert {r["question_id"] for r in rows} == set(councils) == {f"test:{i}" for i in range(4)}
    for r in rows:
        c = councils[r["question_id"]]
        assert r["members"] == c["members"]
        assert r["market_price_at_forecast"] == c["market_price_at_forecast"]
        assert r["prompt_id"] == prompts.PROMPT_ID and r["model"] == "council" and r["probability"]
    assert not any(r["setup"].startswith("council:") and "only" in r["setup"] for r in main_rows)  # main file untouched


def test_rechair_resumes_without_duplicates(run_files):
    q, main, abl = run_files
    before = _rows(abl)
    _rechair(q, main, abl)
    assert len(_rows(abl)) == len(before)
    _main_run(q, main)            # the main run reaches questions 4 and 5
    _rechair(q, main, abl)
    assert len(_rows(abl)) == len(before) + 2 * 3


def test_chair_sees_only_its_view(tmp_path, monkeypatch):
    q, main = tmp_path / "questions.csv", tmp_path / "forecasts.csv"
    _write_questions(q)
    _main_run(q, main, limit=1)
    seen = {}

    def ask(self, model, system, user):
        seen[system] = user
        return json.dumps({"probability": 0.5, "reasoning": "x"})

    monkeypatch.setattr(FakeBackend, "ask", ask)
    monkeypatch.setattr(sys, "argv", ["rechair", "--backend", "fake", "--set", "settled", "--questions", str(q),
                                      "--members-from", str(main), "--out", str(tmp_path / "abl.csv"),
                                      "--chairmen", "a", "--full-chairmen", "b"])
    rechair.main()
    member = next(r for r in _rows(main) if r["setup"] == "single:a")
    p = float(member["probability"])
    numbers, reasoning, full = (seen[prompts.CHAIRMAN_NUMBERS_SYSTEM], seen[prompts.CHAIRMAN_REASONING_SYSTEM],
                                seen[prompts.CHAIRMAN_SYSTEM])
    assert f"probability {p:.2f}" in numbers and "fake answer" not in numbers
    assert "fake answer from a" in reasoning and f"{p:.2f}" not in reasoning
    assert f"probability {p:.2f}. fake answer from a" in full
    assert "Today's date: 2026-08-03" in numbers   # asked as of the price date, like the members


# ── Analysis ──────────────────────────────────────────────────────────────────

def test_analysis_tables(run_files):
    q, main, abl = run_files
    views, chairs, shifts = ablation.run([str(q)], [str(main), str(abl)], ["settled"], n_boot=50)
    pairs = {(r["setup"], r["versus"]) for r in views if r["source"] == "all"}
    assert ("council:numbers-only:chair=a", "council:chair=a") in pairs
    assert ("council:reasoning-only:chair=a", "council:chair=a") in pairs
    assert ("council:chair=b", "baseline:mean") in pairs
    assert {r["source"] for r in views} == {"all", "kalshi", "polymarket"}
    assert {r["chair"] for r in chairs} == {"a", "b"} and all(r["n_common"] == 4 for r in chairs)
    assert {r["council"] for r in shifts} == {"council:chair=a", "council:chair=b",
                                              "council:numbers-only:chair=a", "council:reasoning-only:chair=a"}


def test_shift_table_by_hand():
    probs = {"baseline:mean": {"q1": 0.4, "q2": 0.6, "q3": 0.5},
             "council:numbers-only:chair=a": {"q1": 0.42, "q2": 0.9, "q3": None}}
    [row] = ablation.shift_table(probs, {"q1": 0, "q2": 1, "q3": 1})
    assert row["n"] == 2
    assert row["mean_abs_shift_from_mean_pool"] == pytest.approx((0.02 + 0.3) / 2)
    assert row["share_within_0.05"] == 0.5


def test_no_ablation_rows_means_no_tables(run_files):
    q, main, _ = run_files
    assert ablation.run([str(q)], [str(main)], ["settled"], n_boot=10) is None
