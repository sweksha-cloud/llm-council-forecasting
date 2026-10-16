"""Spark status report on a fake repo: progress, failed calls, pace, ETA."""

import csv
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from forecast import prompts
from forecast.postrun import QUEUE
from forecast.run_forecasts import COLUMNS
from forecast.status import STEPS, pace, report

ROOT = Path(__file__).resolve().parent.parent
T0 = datetime(2026, 10, 17, tzinfo=timezone.utc)


def _write(path, rows, cols):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)


def _repo(tmp_path, answered=10, failures=2):
    qcols = ["question_id", "set", "resolution_date", "price_time", "market_price", "outcome"]
    qs = [{"question_id": f"{s}:{i}", "set": s, "resolution_date": "2026-03-08T00:00:00Z",
           "price_time": "2026-03-01T00:00:00Z", "market_price": "0.4", "outcome": "1"}
          for s, n in (("settled", 10), ("contamination", 4), ("settled-ext", 6)) for i in range(n)]
    rows, t = [], T0
    for qid in [f"settled:{i}" for i in range(answered)]:
        for setup in STEPS[0][1]:
            t += timedelta(seconds=10)
            rows.append({"question_id": qid, "setup": setup, "probability": 0.5, "raw_response": json.dumps({"probability": 0.5}),
                         "prompt_id": prompts.PROMPT_ID, "forecast_at": t.strftime("%Y-%m-%dT%H:%M:%SZ")})
    for i in range(failures):   # failed calls on contamination, never retried
        rows.append({"question_id": f"contamination:{i}", "setup": "single:gemma2:9b", "probability": "",
                     "raw_response": "ERROR: timed out", "prompt_id": prompts.PROMPT_ID, "forecast_at": ""})
    _write(tmp_path / "data/questions.csv", qs, qcols)
    _write(tmp_path / "data/forecasts.csv", rows, COLUMNS)
    return tmp_path


def test_report_progress_failures_and_eta(tmp_path):
    out = report(_repo(tmp_path, answered=5), now=T0)
    assert "1. settled: 10 eligible questions, 35 calls left" in out        # 5 of 10 done x 7 setups
    assert re.search(r"single:llama3\.1:8b\s+5/10\s", out)
    assert "2 failed, not yet retried" in out
    assert "Pace: 10 s per call" in out
    # remaining: settled 35 + contamination 28 + ext 42 calls at 10 s, DeepSeek 14 questions at 110 s
    assert "~0.7 h" in out.split("ETA for the whole queue: ")[1][:6]        # (105*10 + 14*110) s = 0.72 h
    assert "Variance seed 1: not started" in out


def test_finished_queue(tmp_path):
    root = _repo(tmp_path, answered=10, failures=0)
    rows = list(csv.DictReader(open(root / "data/forecasts.csv")))
    t = T0
    for s, setups in STEPS[1:]:
        for i in range({"contamination": 4, "settled-ext": 6, "settled": 10}[s]):
            for st in setups:
                t += timedelta(seconds=10)
                rows.append({**rows[0], "question_id": f"{s}:{i}", "setup": st, "forecast_at": t.strftime("%Y-%m-%dT%H:%M:%SZ")})
    _write(root / "data/forecasts.csv", rows, COLUMNS)
    assert "(finished)" in report(root, now=t)


def test_pace_ignores_long_gaps():
    rows = [{"setup": "single:a", "forecast_at": (T0 + timedelta(seconds=s)).strftime("%Y-%m-%dT%H:%M:%SZ")}
            for s in (0, 10, 20, 30, 40, 50, 7200, 7210)]
    assert pace(rows, False) == 10.0
    assert pace(rows, True) is None


def test_steps_match_the_queue():
    steps = {}
    for s, setups in STEPS:
        steps.setdefault(s, set()).update(setups)
    assert steps == {s: set(v) for s, v in QUEUE.items()}


def test_status_script_is_read_only(tmp_path):
    before = {p: p.stat().st_mtime_ns for p in (ROOT / "data").rglob("*.csv")}
    res = subprocess.run(["bash", "scripts/status_spark.sh"], cwd=ROOT, capture_output=True, text=True)
    assert res.returncode == 0 and "Spark queue status" in res.stdout
    assert {p: p.stat().st_mtime_ns for p in (ROOT / "data").rglob("*.csv")} == before
