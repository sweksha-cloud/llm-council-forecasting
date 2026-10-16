"""Post-run check: a complete fake spark run passes and merges; a broken one is stopped with a report."""

import csv
import json
import re
from argparse import Namespace
from pathlib import Path

import pytest

from forecast import prompts
from forecast.postrun import QUEUE, malformed, run, validate
from forecast.run_forecasts import COLUMNS

ROOT = Path(__file__).resolve().parent.parent
QCOLS = ["question_id", "source", "question_text", "resolution_criteria", "set", "resolution_date",
         "outcome", "market_price", "price_time"]


def _questions():
    qs = []
    for s, n in (("settled", 4), ("contamination", 2), ("settled-ext", 3)):
        for i in range(n):
            qs.append({"question_id": f"{s}:{i}", "source": "polymarket", "question_text": f"{s} {i}?",
                       "resolution_criteria": "", "set": s, "resolution_date": "2026-03-08T00:00:00Z",
                       "outcome": str(i % 2), "market_price": "0.4", "price_time": "2026-03-01T00:00:00Z"})
    qs[0]["price_time"] = ""   # no price date: skipped by design, never "missing"
    return qs


def _complete_run(qs):
    rows = []
    for q in qs:
        if not q["price_time"]:
            continue
        for setup in QUEUE[q["set"]]:
            members = [m.split(":", 1)[1] for m in QUEUE[q["set"]] if m.startswith("single:") and "deepseek" not in m]
            rows.append({"question_id": q["question_id"], "setup": setup, "model": setup.split(":", 1)[1],
                         "members": json.dumps(members) if setup.startswith("council:") else "",
                         "probability": 0.6, "abstained": False,
                         "raw_response": json.dumps({"reasoning": "x", "probability": 0.6}),
                         "prompt_id": prompts.PROMPT_ID, "forecast_at": "2026-10-17T00:00:00Z",
                         "market_price_at_forecast": q["market_price"], "locked": False, "origin": "this-project"})
    return rows


def _write(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _args(tmp_path, **kw):
    return Namespace(spark=str(tmp_path / "spark.csv"), questions=str(tmp_path / "q.csv"),
                     into=str(tmp_path / "forecasts.csv"), log=str(tmp_path / "cmds.log"), sets=list(QUEUE),
                     max_abstain=0.2, max_malformed=0.05, dry_run=False, no_build=True, **kw)


def test_complete_run_passes_and_merges(tmp_path):
    qs = _questions()
    rows = _complete_run(qs)
    _write(tmp_path / "q.csv", qs, QCOLS)
    _write(tmp_path / "spark.csv", rows, COLUMNS)
    (tmp_path / "cmds.log").write_text("2026-10-17T00:00:00Z queue: --set settled --no-think --models a b\n")
    assert validate(rows, qs, list(QUEUE), tmp_path / "cmds.log")[0] == []
    assert run(_args(tmp_path)) == 0
    assert len(list(csv.DictReader(open(tmp_path / "forecasts.csv")))) == len(rows)
    assert run(_args(tmp_path)) == 0                       # merging again adds nothing
    assert len(list(csv.DictReader(open(tmp_path / "forecasts.csv")))) == len(rows)


def test_broken_run_is_stopped_and_nothing_is_merged(tmp_path, capsys):
    qs = _questions()
    rows = _complete_run(qs)
    # 1. settled-ext unfinished: the qwen3 chair never ran on one question
    rows = [r for r in rows if not (r["question_id"] == "settled-ext:2" and r["setup"] == "council:chair=qwen3:8b")]
    # 2. a failed call with no retry
    for r in rows:
        if r["question_id"] == "contamination:1" and r["setup"] == "single:gemma2:9b":
            r.update(probability="", abstained=True, raw_response="ERROR: timed out")
    # 3. phi3 abstains everywhere on settled, with malformed replies
    for r in rows:
        if r["question_id"].startswith("settled:") and r["setup"] == "single:phi3:medium":
            r.update(probability="", abstained=True, raw_response="I cannot predict the future.")
    # 4. an old prompt version, 5. a stale market price, 6. a question spark has that we don't
    rows.append({**rows[0], "prompt_id": "v1"})
    rows[1]["market_price_at_forecast"] = "0.9"
    rows.append({**rows[2], "question_id": "settled:999"})
    _write(tmp_path / "q.csv", qs, QCOLS)
    _write(tmp_path / "spark.csv", rows, COLUMNS)
    # 7. a seed override in the log
    (tmp_path / "cmds.log").write_text("2026-10-17T00:00:00Z queue: --set settled --seed 7 --models a b\n")
    _write(tmp_path / "forecasts.csv", [], COLUMNS)
    before = (tmp_path / "forecasts.csv").read_text()

    assert run(_args(tmp_path)) == 1
    out = capsys.readouterr().out
    for expected in ("settled-ext: council:chair=qwen3:8b is missing 1 of 3",
                     "contamination: single:gemma2:9b has 1 failed calls",
                     "settled: single:phi3:medium abstained on 100%",
                     "malformed replies",
                     "prompt_id other than",
                     "different market price",
                     "not in data/questions.csv",
                     "seed/temperature override",
                     "nothing was merged"):
        assert expected in out, expected
    assert (tmp_path / "forecasts.csv").read_text() == before   # untouched


def test_retry_after_failure_counts_as_done():
    qs = _questions()
    rows = _complete_run(qs)
    target = next(r for r in rows if r["setup"] == "single:llama3.1:8b")
    rows.insert(0, {**target, "probability": "", "raw_response": "ERROR: connection refused"})
    assert validate(rows, qs, list(QUEUE))[0] == []


def test_skipped_questions_are_not_missing():
    qs = _questions()
    problems, report = validate(_complete_run(qs), qs, ["settled"])
    assert problems == [] and "1 skipped by design" in "\n".join(report)


def test_malformed():
    assert malformed("I cannot help with that.")
    assert not malformed('{"probability": 0.4}') and not malformed("ERROR: x") and not malformed('{"reasoning": "x"}')


def test_queue_matches_spark_script():
    script = (ROOT / "scripts" / "queue_spark.sh").read_text()
    m5 = re.search(r'M5="([^"]+)"', script).group(1).split()
    chairs = re.search(r'CHAIRS="([^"]+)"', script).group(1).split()
    found = {}
    for line in script.splitlines():
        m = re.match(r"step --set (\S+)\s+(.*)", line.strip())
        if not m:
            continue
        s, rest = m.groups()
        models = m5 if "$M5" in rest else re.search(r"--models (\S+)", rest).group(1).split()
        heads = chairs if "$CHAIRS" in rest else []
        found.setdefault(s, set()).update([f"single:{x}" for x in models] + [f"council:chair={c}" for c in heads])
    assert found == {s: set(v) for s, v in QUEUE.items()}
