import csv
import subprocess
import sys
from pathlib import Path

import pytest

from forecast.run_forecasts import parse_response

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("text, expected", [
    ('{"probability": 0.7, "reasoning": "x"}', 0.7),
    ('Sure! {"probability": 0.25, "reasoning": "x"} Hope that helps.', 0.25),
    ('<think>long chain of thought {"probability": 0.9}</think>{"probability": 0.1, "reasoning": "x"}', 0.1),
    ('{"probability": 70, "reasoning": "x"}', 0.7),     # percent written as a number
    ('probability: 35%', 0.35),
    ('Probability = 0.4', 0.4),
    ('{"probability": "70%", "reasoning": "x"}', 0.7),   # percent as a string
])
def test_parse_response_finds_probability(text, expected):
    p, _ = parse_response(text)
    assert p == pytest.approx(expected)


@pytest.mark.parametrize("text", [
    "I cannot provide predictions about elections.",   # refusal -> abstain, not a number
    '{"probability": 1.7}',                             # out of range
    "",
    "ERROR: timed out",
])
def test_parse_response_abstains(text):
    p, _ = parse_response(text)
    assert p is None


def _write_questions(path: Path) -> None:
    cols = ["question_id", "source", "question_text", "resolution_criteria", "set",
            "resolution_date", "outcome"]
    rows = [
        {"question_id": f"test:{i}", "source": "test", "question_text": f"Will event {i} happen?",
         "resolution_criteria": "Resolves Yes if it happens.", "set": "live",
         "resolution_date": "2099-01-01T00:00:00Z", "outcome": ""}
        for i in range(3)
    ]
    rows.append({**rows[0], "question_id": "test:closed", "resolution_date": "2000-01-01T00:00:00Z"})
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _run(questions: Path, out: Path) -> None:
    subprocess.run([sys.executable, "-m", "forecast.run_forecasts", "--backend", "fake",
                    "--questions", str(questions), "--out", str(out), "--lock",
                    "--models", "a", "b", "c", "--chairmen", "a", "b"],
                   cwd=ROOT, check=True, capture_output=True)


def test_fake_run_end_to_end_and_resume(tmp_path):
    questions, out = tmp_path / "q.csv", tmp_path / "f.csv"
    _write_questions(questions)
    _run(questions, out)
    rows = list(csv.DictReader(out.open()))
    # 3 open questions x (3 single + 2 council); the closed question is skipped
    assert len(rows) == 15
    assert {r["question_id"] for r in rows} == {"test:0", "test:1", "test:2"}
    assert all(r["locked"] == "True" and r["prompt_id"] for r in rows)
    council = [r for r in rows if r["setup"].startswith("council:")]
    assert all(r["members"] == '["a", "b", "c"]' for r in council)

    _run(questions, out)  # second run must not add or change anything
    assert list(csv.DictReader(out.open())) == rows


def test_settled_questions_use_stored_price_and_date(tmp_path):
    questions, out = tmp_path / "q.csv", tmp_path / "f.csv"
    cols = ["question_id", "source", "question_text", "resolution_criteria", "set",
            "resolution_date", "outcome", "market_price", "price_time"]
    with questions.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerow({"question_id": "test:settled", "source": "test", "question_text": "Did it happen?",
                    "resolution_criteria": "", "set": "settled", "resolution_date": "2026-03-08T00:00:00Z",
                    "outcome": "1", "market_price": "0.42", "price_time": "2026-03-01T00:00:00Z"})
    subprocess.run([sys.executable, "-m", "forecast.run_forecasts", "--backend", "fake", "--set", "settled",
                    "--questions", str(questions), "--out", str(out),
                    "--models", "a", "b", "--chairmen", "a"],
                   cwd=ROOT, check=True, capture_output=True)
    rows = list(csv.DictReader(out.open()))
    assert len(rows) == 3  # resolved settled questions are still forecast
    assert all(r["market_price_at_forecast"] == "0.42" for r in rows)


def test_merge_forecasts_appends_only_new_keys(tmp_path):
    from forecast.merge_forecasts import merge
    from forecast.run_forecasts import append_rows, load_existing
    into, src = tmp_path / "f.csv", tmp_path / "s.csv"
    append_rows(into, [{"question_id": "q0", "setup": "single:a", "prompt_id": "v2", "probability": 0.3}])
    append_rows(src, [{"question_id": "q0", "setup": "single:a", "prompt_id": "v2", "probability": 0.9},
                      {"question_id": "q1", "setup": "single:a", "prompt_id": "v2", "probability": 0.5}])
    assert merge([src], into) == 1
    rows = load_existing(into)
    assert rows[("q0", "single:a", "v2")]["probability"] == "0.3"
    assert ("q1", "single:a", "v2") in rows
    assert merge([src], into) == 0


# ── Audit fixes ───────────────────────────────────────────────────────────────

from forecast.run_forecasts import as_of_date, load_existing


@pytest.mark.parametrize("q, expected", [
    ({"set": "live"}, "2026-10-16"),
    ({"set": "settled", "price_time": "2026-03-01T00:00:00Z", "resolution_date": "2026-03-08T00:00:00Z"}, "2026-03-01"),
    ({"set": "settled", "price_time": "", "resolution_date": "2026-03-08T00:00:00Z"}, None),          # no price date
    ({"set": "contamination", "price_time": "2026-03-09T00:00:00Z",
      "resolution_date": "2026-03-08T00:00:00Z"}, None),                                              # priced after close
])
def test_as_of_date_never_after_close(q, expected):
    assert as_of_date(q, "2026-10-16") == expected


def test_failed_calls_are_retried_not_kept(tmp_path):
    out = tmp_path / "f.csv"
    out.write_text("question_id,setup,prompt_id,raw_response\n"
                   "q1,single:a,v2,ERROR: connection refused\n"
                   'q2,single:a,v2,"{""probability"": 0.3}"\n')
    assert set(load_existing(out)) == {("q2", "single:a", "v2")}


def test_settled_question_priced_after_close_is_skipped(tmp_path):
    questions, out = tmp_path / "q.csv", tmp_path / "f.csv"
    cols = ["question_id", "source", "question_text", "resolution_criteria", "set",
            "resolution_date", "outcome", "market_price", "price_time"]
    with questions.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerow({"question_id": "test:late", "source": "test", "question_text": "Ceasefire by July 31?",
                    "resolution_criteria": "", "set": "settled", "resolution_date": "2026-07-31T23:59:00Z",
                    "outcome": "1", "market_price": "0.83", "price_time": "2026-08-05T18:04:28Z"})
    subprocess.run([sys.executable, "-m", "forecast.run_forecasts", "--backend", "fake", "--set", "settled",
                    "--questions", str(questions), "--out", str(out), "--models", "a", "b", "--chairmen", "a"],
                   cwd=ROOT, check=True, capture_output=True)
    assert not out.exists()


def test_polymarket_settled_price_anchored_before_scheduled_close():
    from collect.collect_settled import polymarket_event_rows
    ev = {"id": 1, "slug": "x", "tags": [], "markets": [{
        "id": "9", "question": "Ceasefire by July 31?", "outcomes": '["Yes", "No"]',
        "outcomePrices": '["1", "0"]', "clobTokenIds": '["t"]', "volumeNum": 1e6, "closed": True,
        "endDate": "2026-07-31T23:59:00Z", "closedTime": "2026-08-12 18:04:28+00"}]}
    row = polymarket_event_rows(ev, 0, set())[0]
    assert row["_close"].isoformat() == "2026-07-31T23:59:00+00:00"   # not the later resolution time
    assert row["resolved_at"] == "2026-08-12T18:04:28Z"


def test_polymarket_market_dates_must_fall_in_the_window():
    from datetime import datetime, timezone
    from collect.collect_settled import polymarket_event_rows
    utc = lambda *a: datetime(*a, tzinfo=timezone.utc)
    market = lambda mid, end, closed: {"id": mid, "question": f"Q{mid}?", "outcomes": '["Yes", "No"]',
                                       "outcomePrices": '["0", "1"]', "clobTokenIds": '["t"]', "volumeNum": 1e6,
                                       "closed": True, "endDate": end, "closedTime": closed}
    ev = {"id": 1, "slug": "x", "tags": [], "markets": [
        market("in", "2025-09-30T00:00:00Z", "2025-10-01 00:00:00+00"),
        market("early", "2025-09-30T00:00:00Z", "2025-02-21 00:00:00+00"),   # resolved before the window
        market("late", "2026-12-31T00:00:00Z", "2026-12-31 00:00:00+00")]}   # closes after the window
    rows = polymarket_event_rows(ev, 0, set(), utc(2025, 7, 1), utc(2026, 6, 30, 23, 59, 59))
    assert [r["question_id"] for r in rows] == ["polymarket:in"]
