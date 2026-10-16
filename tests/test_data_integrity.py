"""Integrity of the committed data files. These run on the real data/questions.csv and data/forecasts.csv,
so a bad collection, repricing or merge fails CI before it reaches main."""

import csv
import io
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from collect.collect_settled import priced_too_late

ROOT = Path(__file__).resolve().parent.parent
SETS = {"live", "settled", "settled-ext", "contamination", "dropped"}
BACKTEST = {"settled", "settled-ext", "contamination"}


def _rows(name):
    with open(ROOT / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


QUESTIONS = _rows("questions.csv")
FORECASTS = _rows("forecasts.csv")
dt = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))


def _bad(rows, check, label="question_id"):
    return [r[label] for r in rows if not check(r)][:10]


def _in_unit(x):
    try:
        return 0.0 <= float(x) <= 1.0
    except ValueError:
        return False


# ── questions.csv ─────────────────────────────────────────────────────────────

def test_question_ids_unique():
    ids = [q["question_id"] for q in QUESTIONS]
    assert len(ids) == len(set(ids)), [i for i in set(ids) if ids.count(i) > 1][:10]


def test_set_tags_valid():
    assert {q["set"] for q in QUESTIONS} <= SETS, {q["set"] for q in QUESTIONS} - SETS


def test_prices_and_outcomes_in_range():
    assert _bad(QUESTIONS, lambda q: q["market_price"] == "" or _in_unit(q["market_price"])) == []
    assert _bad(QUESTIONS, lambda q: q["outcome"] in ("", "0", "1")) == []


def test_backtest_questions_priced_and_resolved():
    bt = [q for q in QUESTIONS if q["set"] in BACKTEST]
    assert _bad(bt, lambda q: q["market_price"] and q["price_time"]) == []          # unpriced ones are tagged dropped
    assert _bad(bt, lambda q: q["outcome"] in ("0", "1") and q["resolved_at"]) == []


def test_backtest_price_before_close_and_resolution():
    bt = [q for q in QUESTIONS if q["set"] in BACKTEST]
    assert _bad(bt, lambda q: dt(q["price_time"]) < dt(q["resolution_date"]) and dt(q["price_time"]) < dt(q["resolved_at"])) == []
    # and at least 7 days before the earlier of the two (the 2026-10-16/17 leak)
    assert _bad(bt, lambda q: not priced_too_late(q, timedelta(days=7))) == []


def test_settled_ext_inside_its_window():
    ext = [q for q in QUESTIONS if q["set"] == "settled-ext"]
    assert ext
    inside = lambda s: "2025-07-01" <= s[:10] <= "2026-06-30"
    assert _bad(ext, lambda q: inside(q["resolution_date"]) and inside(q["resolved_at"])) == []
    assert _bad(ext, lambda q: q["source"] == "polymarket") == []


# ── forecasts.csv ─────────────────────────────────────────────────────────────

def test_forecasts_refer_to_known_questions():
    known = {q["question_id"] for q in QUESTIONS}
    assert _bad(FORECASTS, lambda f: f["question_id"] in known) == []


def test_forecast_probabilities_in_range():
    assert _bad(FORECASTS, lambda f: f["probability"] == "" or _in_unit(f["probability"])) == []
    assert _bad(FORECASTS, lambda f: (f["probability"] == "") == (f["abstained"] == "True")) == []


def test_one_locked_forecast_per_key():
    keys = [(f["question_id"], f["setup"], f["prompt_id"]) for f in FORECASTS if f["locked"] == "True"
            and not f["raw_response"].startswith("ERROR:")]
    assert len(keys) == len(set(keys))


def _main_forecasts():
    for ref in ("origin/main", "main"):
        res = subprocess.run(["git", "show", f"{ref}:data/forecasts.csv"], cwd=ROOT, capture_output=True, text=True)
        if res.returncode == 0:
            return list(csv.DictReader(io.StringIO(res.stdout)))
    return None


def test_locked_rows_unchanged_vs_main():
    base = _main_forecasts()
    if base is None:
        pytest.skip("main isn't available in this checkout")
    now = {(f["question_id"], f["setup"], f["prompt_id"], f["forecast_at"]): f for f in FORECASTS}
    changed = [k for k, f in ((k, f) for f in base if f["locked"] == "True"
                              for k in [(f["question_id"], f["setup"], f["prompt_id"], f["forecast_at"])])
               if now.get(k) != f]
    assert changed == [], f"{len(changed)} locked forecasts were edited or removed, e.g. {changed[:3]}"
