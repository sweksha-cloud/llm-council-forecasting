"""In-play sensitivity check: live questions collected less than 24 hours before their market
ended can be left out of scoring with --exclude-in-play (audit, 2026-10-16, problem 2).

Your task: make these tests pass. Run them with
    .venv/bin/python -m pytest -q tests/test_in_play.py
"""

import csv
import subprocess
import sys
from pathlib import Path

from scoring.report import collected_in_play, load

ROOT = Path(__file__).resolve().parent.parent


# ── 1. collected_in_play(q, hours=24) in scoring/report.py ────────────────────

def test_collected_shortly_before_the_end_is_in_play():
    q = {"set": "live", "collected_at": "2026-10-09T12:00:00Z", "resolved_at": "2026-10-09T20:00:00Z"}
    assert collected_in_play(q)                 # 8 hours before it ended


def test_collected_well_before_the_end_is_not():
    q = {"set": "live", "collected_at": "2026-10-09T12:00:00Z", "resolved_at": "2026-10-12T12:00:00Z"}
    assert not collected_in_play(q)             # 3 days before


def test_the_window_can_be_changed():
    q = {"set": "live", "collected_at": "2026-10-09T12:00:00Z", "resolved_at": "2026-10-10T18:00:00Z"}
    assert not collected_in_play(q)             # 30 hours: outside the default 24
    assert collected_in_play(q, hours=48)


def test_only_live_questions_with_both_dates():
    assert not collected_in_play({"set": "settled", "collected_at": "2026-10-09T12:00:00Z",
                                  "resolved_at": "2026-10-09T13:00:00Z"})   # backtests are priced 7 days out
    assert not collected_in_play({"set": "live", "collected_at": "2026-10-09T12:00:00Z", "resolved_at": ""})


# ── 2. load(..., exclude_in_play=True) leaves those questions out entirely ────

def _write(path: Path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _files(tmp_path):
    q, fc = tmp_path / "q.csv", tmp_path / "f.csv"
    _write(q, [{"question_id": "in_play", "set": "live", "outcome": "1", "market_price": "0.9",
                "collected_at": "2026-10-09T12:00:00Z", "resolved_at": "2026-10-09T20:00:00Z"},
               {"question_id": "normal", "set": "live", "outcome": "0", "market_price": "0.4",
                "collected_at": "2026-10-01T12:00:00Z", "resolved_at": "2026-10-20T00:00:00Z"}])
    _write(fc, [{"question_id": qid, "setup": "single:a", "probability": "0.5", "raw_response": "{}",
                 "prompt_id": "v2", "members": "", "forecast_at": "2026-10-09T13:00:00Z",
                 "market_price_at_forecast": ""} for qid in ("in_play", "normal")])
    return q, fc


def test_load_keeps_everything_by_default(tmp_path):
    q, fc = _files(tmp_path)
    outcomes, _, _, _ = load([str(q)], [str(fc)], "live")
    assert set(outcomes) == {"in_play", "normal"}


def test_load_can_leave_in_play_questions_out(tmp_path):
    q, fc = _files(tmp_path)
    outcomes, probs, _, market = load([str(q)], [str(fc)], "live", exclude_in_play=True)
    assert set(outcomes) == {"normal"}
    assert set(probs["single:a"]) == {"normal"} and set(market) == {"normal"}


# ── 3. the report has a flag for it ───────────────────────────────────────────

def test_report_flag(tmp_path):
    q, fc = _files(tmp_path)
    subprocess.run([sys.executable, "-m", "scoring.report", "--questions", str(q), "--forecasts", str(fc),
                    "--set", "live", "--exclude-in-play", "--out", str(tmp_path / "out")],
                   cwd=ROOT, check=True, capture_output=True)
    assert "Resolved questions scored: **1**" in (tmp_path / "out" / "report.md").read_text()
