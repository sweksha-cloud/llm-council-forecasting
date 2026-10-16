"""Live outcome sync: the merge rules, and scripts/sync_live.sh end to end in a throwaway clone."""

import csv
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from collect.merge_outcomes import merge

ROOT = Path(__file__).resolve().parent.parent


def test_merge_takes_only_missing_live_outcomes():
    local = [{"question_id": "a", "set": "live", "outcome": "", "resolved_at": "", "market_price": "0.4"},
             {"question_id": "b", "set": "live", "outcome": "1", "resolved_at": "x", "market_price": "0.5"},
             {"question_id": "c", "set": "settled", "outcome": "", "resolved_at": "", "market_price": "0.3"},
             {"question_id": "d", "set": "live", "outcome": "", "resolved_at": "", "market_price": "0.2"}]
    remote = [{"question_id": "a", "set": "live", "outcome": "0", "resolved_at": "2026-10-20", "market_price": "0.9"},
              {"question_id": "b", "set": "live", "outcome": "0", "resolved_at": "y", "market_price": "0.5"},
              {"question_id": "c", "set": "settled", "outcome": "1", "resolved_at": "z", "market_price": "0.3"},
              {"question_id": "d", "set": "live", "outcome": "", "resolved_at": "", "market_price": "0.2"}]
    merged, filled, conflicts = merge(local, remote)
    assert filled == ["a"] and conflicts == ["b"]
    assert merged[0] == {**local[0], "outcome": "0", "resolved_at": "2026-10-20"}   # price NOT taken from spark
    assert merged[1:] == local[1:]


@pytest.mark.skipif(shutil.which("git") is None, reason="git isn't installed")
def test_sync_live_script(tmp_path):
    repo = tmp_path / "repo"
    subprocess.run(["git", "clone", "-q", str(ROOT), str(repo)], check=True)
    # the clone has HEAD's files; overlay the working-tree versions of the files under test
    for f in ("scripts/sync_live.sh", "collect/merge_outcomes.py", "Makefile"):
        shutil.copy(ROOT / f, repo / f)
    run = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True)
    run("config", "user.email", "t@example.com"); run("config", "user.name", "test")
    run("add", "-A"); run("commit", "-q", "-m", "files under test", "--allow-empty")

    with open(repo / "data/questions.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols, rows = reader.fieldnames, list(reader)
    open_live = [r for r in rows if r["set"] == "live" and not r["outcome"]][:3]
    assert len(open_live) == 3
    spark = [dict(r, outcome="1", resolved_at="2026-10-20T00:00:00Z") if r in open_live else r for r in rows]
    with open(tmp_path / "spark_q.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(spark)

    env = {"PATH": "/usr/bin:/bin", "PY": sys.executable, "HOME": str(tmp_path)}
    sh = lambda *a: subprocess.run(["bash", "scripts/sync_live.sh", *a], cwd=repo, env=env,
                                   capture_output=True, text=True)
    dry = sh("--dry-run", "--from", str(tmp_path / "spark_q.csv"))
    assert dry.returncode == 0, dry.stderr
    assert "3 live questions get an outcome" in dry.stdout and "nothing written" in dry.stdout
    assert run("status", "--porcelain", "--", "data").stdout == ""          # dry run changed nothing

    real = sh("--from", str(tmp_path / "spark_q.csv"))
    assert real.returncode == 0, real.stderr + real.stdout
    assert run("rev-parse", "--abbrev-ref", "HEAD").stdout.startswith("data/live-outcomes-")
    assert "3 questions resolved" in run("log", "-1", "--format=%s").stdout
    changed = run("show", "--stat", "--format=", "HEAD").stdout
    assert "data/questions.csv" in changed and "results/live" in changed
    again = sh("--from", str(tmp_path / "spark_q.csv"))                     # nothing new the second time
    assert "No new live outcomes" in again.stdout
